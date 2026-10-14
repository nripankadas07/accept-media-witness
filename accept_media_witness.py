"""Offline bounded accept-media-witness analyzer. No operational writes."""

import re
TOKEN=re.compile(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+\Z")
QUALITY=re.compile(r'(?:0(?:\.[0-9]{0,3})?|1(?:\.0{0,3})?)\Z')

def split(s,sep):
    parts=[];start=0;quoted=False;escaped=False
    for i,c in enumerate(s):
        if ord(c)<32 and c!='\t' or ord(c)==127:raise ValueError('control character')
        if escaped:escaped=False;continue
        if quoted and c=='\\':escaped=True;continue
        if c=='"':quoted=not quoted
        if c==sep and not quoted:parts.append(s[start:i].strip());start=i+1
    if quoted or escaped:raise ValueError('unterminated quoted value')
    parts.append(s[start:].strip());return parts

def value(s):
    if TOKEN.fullmatch(s):return s
    if len(s)>=2 and s[0]==s[-1]=='"':
        result=[];escaped=False
        for c in s[1:-1]:
            if escaped:result.append(c);escaped=False
            elif c=='\\':escaped=True
            elif c=='"':raise ValueError('unescaped quote in parameter')
            else:result.append(c)
        if escaped:raise ValueError('trailing quoted escape')
        return ''.join(result)
    raise ValueError('invalid parameter value')

def media(s,accept):
    pieces=split(s,';');typ=pieces[0].lower().split('/')
    if len(typ)!=2 or any(not TOKEN.fullmatch(x) for x in typ):raise ValueError('invalid media type')
    a,b=typ
    if '*' in a+b and (not accept or not ((a,b)==('*','*') or '*' not in a and b=='*')):raise ValueError('unsupported wildcard')
    params={};q=1000
    for part in pieces[1:]:
        if '=' not in part:raise ValueError('parameter requires value')
        key,v=part.split('=',1);key=key.strip().lower();v=v.strip()
        if not TOKEN.fullmatch(key) or key in params:raise ValueError('invalid/duplicate parameter')
        if key=='q':
            if not accept or not QUALITY.fullmatch(v):raise ValueError('invalid q weight')
            whole,_,fraction=v.partition('.');q=int(whole)*1000+int((fraction or '').ljust(3,'0'));params[key]=v
        else:
            if 'q' in params:raise ValueError('parameters after q unsupported')
            params[key]=value(v)
    params.pop('q',None)
    return a,b,params,q

def analyze(d):
    if not isinstance(d,dict) or set(d)!={'accept','offers'}:raise ValueError('expected accept and offers')
    header=d['accept'];offers=d['offers']
    if header is not None and (not isinstance(header,str) or len(header)>8192):raise ValueError('invalid/oversized Accept')
    if not isinstance(offers,list) or len(offers)>128:raise ValueError('at most 128 offers')
    ranges=[('*','*',{},1000)] if header is None else [media(x,True) for x in split(header,',') if x]
    if len(ranges)>128:raise ValueError('at most 128 ranges')
    rows=[]
    for i,s in enumerate(offers):
        if not isinstance(s,str):raise ValueError('offer must be string')
        a,b,p,_=media(s,False);matches=[]
        for j,(ra,rb,rp,q) in enumerate(ranges):
            if ra not in ('*',a) or rb not in ('*',b) or any(p.get(k)!=v for k,v in rp.items()):continue
            specificity=(0 if ra=='*' else 1 if rb=='*' else 2,len(rp))
            matches.append((specificity,j,q))
        if matches:
            best=max(x[0] for x in matches);top=[x for x in matches if x[0]==best]
            if len({x[2] for x in top})>1:raise ValueError('conflicting equal-specificity weights are ambiguous')
            _,j,q=top[0]
        else:best=(-1,0);j=None;q=0
        rows.append({'offer':s,'quality_millis':q,'range_index':j,'specificity':list(best),'acceptable':q>0})
    eligible=[(x['quality_millis'],-i,x['offer']) for i,x in enumerate(rows) if x['acceptable']]
    return {'selected':max(eligible)[2] if eligible else None,'offers':rows,'tie_policy':'server offer order','not_acceptable':not bool(eligible)}

def _pairs(pairs):
    result={}
    for key,val in pairs:
        if key in result:raise ValueError('duplicate JSON key: '+key)
        result[key]=val
    return result

def main():
    import argparse,json,sys
    from pathlib import Path
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',help='JSON input path; - for stdin')
    args=parser.parse_args()
    try:
        raw=sys.stdin.buffer.read(1048577) if args.input=='-' else Path(args.input).open('rb').read(1048577)
        if len(raw)>1048576:raise ValueError('input exceeds 1 MiB')
        data=json.loads(raw,object_pairs_hook=_pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON number')))
        print(json.dumps(analyze(data),ensure_ascii=True,indent=2));return 0
    except (ValueError,TypeError,KeyError,OverflowError,RecursionError,OSError) as exc:
        print(json.dumps({'error':str(exc)}),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
