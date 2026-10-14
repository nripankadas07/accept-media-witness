# Candidate brief and comparison — 14 October 2026

**User:** HTTP API maintainers debugging a representation selection. **Painful task:** An explicit q=0 exclusion can be accidentally replaced by a broader high-quality wildcard; parameters also change precedence.

**Smallest useful capability:** Parse a bounded Accept media-range subset and assign each offered representation its most-specific matching quality, with range-index evidence and a deterministic server-order tie policy.

**Acceptance:** the supplied synthetic example must produce the documented installed result; core edge cases and invalid-input paths must pass; a wheel installed outside the checkout must run the CLI and reject malformed input. The public default commit, remote matrix CI and rendered documentation must be verified before LIVE.

**Demand evidence:** inferred from the workflow and relevant accessible documentation/issues, not a verified customer request. **Discovery path:** descriptive repository topics, a runnable example, searchable edge-case documentation and the user's chronological portfolio index. No unsolicited promotion is performed.

**Distinctness:** http-range-witness handles byte ranges and cache-header-contract validates caching; neither negotiates media representations. mimedb/mimedet detect media identity, not preference precedence. Each problem has a different contract and input.

## Current comparables

willdurand/Negotiation is the highest-star relevant result found in the content negotiation star-sorted query. Queries were executed live on GitHub with Sort by Most stars. Search result coverage is bounded to visible first pages, then relevant established repositories; stars inform discovery, not quality or performance.

| Repository | Stars observed | Latest push observed UTC | License metadata | Observation UTC |
| --- | ---: | --- | --- | --- |
| [willdurand/Negotiation](https://github.com/willdurand/Negotiation) | 1421 | 2023-08-03T17:52:44Z | MIT | 2026-10-14T06:09:41.665Z |
| [jshttp/accepts](https://github.com/jshttp/accepts) | 266 | 2026-04-02T16:03:36Z | MIT | 2026-10-14T06:09:41.679Z |
| [jshttp/negotiator](https://github.com/jshttp/negotiator) | 384 | 2026-08-20T16:44:00Z | MIT | 2026-10-14T06:09:41.365Z |

Negotiation supplies standalone PHP negotiation; accepts offers higher-level Node conveniences; negotiator supplies Node content negotiation. Use them in servers. This MVP is an explanatory offline receipt, with a strict smaller grammar and no server integration.

Comparables' current READMEs, installation examples and accessible issues were inspected. Established tools supply broader integration, docs and community support; this project's support consists of reproducible GitHub reports, source tests and explicit bounded semantics. Its clean install has no runtime dependencies, but that alone establishes no time-to-first-result or reliability advantage. Comparator install success and benchmark performance were not measured. License metadata marked NOASSERTION is unresolved metadata, not a permissive-reuse claim. No reuse was needed.

[Primary behavior reference](https://www.rfc-editor.org/rfc/rfc9110.html#section-12.5.1). Competitor README blob hashes, exact star query URLs and source observations are retained in the dated profile research receipt. A local success proves our example, not absence of the behavior in a competitor. Negative results and unsupported configurations remain visible; no superiority claim is made.
