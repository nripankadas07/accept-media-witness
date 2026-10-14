import unittest
from accept_media_witness import analyze

def result(header,*offers):return analyze({'accept':header,'offers':list(offers)})
class Behavior(unittest.TestCase):
    def test_explicit_zero(self):self.assertEqual(result('text/*;q=1,text/html;q=0','text/html','text/plain')['selected'],'text/plain')
    def test_specific_quality(self):self.assertEqual(result('text/*;q=1,text/html;q=0.2,application/json;q=0.5','text/html','application/json')['selected'],'application/json')
    def test_parameter_precedence(self):self.assertEqual(result('text/plain;q=0.1,text/plain;format=flowed;q=0.9','text/plain;format=flowed')['offers'][0]['quality_millis'],900)
    def test_quoted_comma(self):self.assertEqual(result('text/plain;label="a,b"','text/plain;label="a,b"')['selected'],'text/plain;label="a,b"')
    def test_parameter_case(self):self.assertIsNone(result('text/plain;x=A','text/plain;x=a')['selected'])
    def test_type_case(self):self.assertEqual(result('TEXT/HTML','text/html')['selected'],'text/html')
    def test_missing_header(self):self.assertEqual(result(None,'text/plain')['selected'],'text/plain')
    def test_empty_header(self):self.assertTrue(result('','text/plain')['not_acceptable'])
    def test_server_tie(self):self.assertEqual(result('*/*','application/json','text/plain')['selected'],'application/json')
    def test_bad_quality(self):
        with self.assertRaises(ValueError):result('*/*;q=1.1','text/plain')
    def test_equal_specificity_conflict(self):
        with self.assertRaises(ValueError):result('text/plain;q=0,text/plain;q=1','text/plain')
    def test_bad_quote(self):
        with self.assertRaises(ValueError):result('text/plain;x="oops','text/plain')
    def test_control(self):
        with self.assertRaises(ValueError):result('text/plain\r\nx:y','text/plain')
    def test_partial_type_wildcard_rejected(self):
        with self.assertRaises(ValueError):result('te*xt/*','text/plain')
    def test_embedded_unescaped_quote_rejected(self):
        with self.assertRaises(ValueError):result('text/plain;x="a""b"','text/plain')

if __name__=="__main__":unittest.main()
