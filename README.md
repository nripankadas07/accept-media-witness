# accept-media-witness

Parse a bounded Accept media-range subset and assign each offered representation its most-specific matching quality, with range-index evidence and a deterministic server-order tie policy.

Built for http api maintainers debugging a representation selection. An explicit q=0 exclusion can be accidentally replaced by a broader high-quality wildcard; parameters also change precedence.

## Quickstart

Python 3.10+; no runtime dependencies. The build uses setuptools from the official Python registry. This repository is the install source; no external registry release is claimed.

```sh
git clone https://github.com/nripankadas07/accept-media-witness.git
cd accept-media-witness
python -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/accept-media-witness example.json
```

On Windows, use `.venv\Scripts\python` and `.venv\Scripts\accept-media-witness`. Windows behavior has not been exercised; Linux CI is configured to verify Python 3.10, 3.12 and 3.14. An input filename or `-` for standard input is required. Valid analysis returns exit 0, including negative findings; malformed or unsupported input returns exit 2 and a JSON error on stderr. Input is bounded to 1 MiB; duplicate JSON keys and nonfinite numbers fail.

The runnable [example](example.json) uses synthetic data. Run `python accept_media_witness.py example.json` directly for a source-only demo. Import `analyze(data)` for the Python API; unsupported input raises an exception. The tool makes no network request or operational write.

## Input and output contract

Top level accept is a header string or null for absence; offers is a media-type string array. Supports token/quoted parameter values, quoted-pair escapes, three-decimal q weights, type/* and */*. Duplicate parameters, invalid/partial wildcards, invalid weights and control characters fail. selected is null if no offered representation has positive quality.

The example's installed behavior is asserted in [test_installed_cli.py](test_installed_cli.py). [Unit cases](test_behavior.py) cover positive decisions and meaningful failure cases. The report records actual captured evidence; absence of a finding does not certify an operational environment.

## Limits

Accept media types only, not language/encoding/charset negotiation, MIME shorthand or a web server. No structured suffix wildcards or obsolete Accept extensions after q. Conflicting equal-specificity qualities fail as ambiguous rather than select a silent policy. Parameter values compare case-sensitively; type/name tokens compare case-insensitively. Missing header accepts all; an explicitly empty header accepts none. Header <=8192 chars, 128 ranges/offers.

## Validation and research

Run `python -m unittest -v` and `python -m compileall -q accept_media_witness.py`. [Validation](VALIDATION.md) records exercised configurations. [Research and candidate brief](RESEARCH.md) compares current alternatives and states the inferred demand. No customer adoption or measured performance advantage is claimed.

## Contributing and support

[Contribution guide](CONTRIBUTING.md) · [Support](SUPPORT.md) · [Security](SECURITY.md) · [MIT license](LICENSE)

Original implementation developed with AI assistance and reviewed through acceptance tests. No competitor source, branding or prose was copied. Primary specifications informed the explicitly supported semantics.
