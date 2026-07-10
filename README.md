# childnajia

HIDAYAH: A Clinical Danger Detection Engine for Paediatric Emergency Triage

_Status: Needs triage (portfolio registry)._

## Testing

The danger-detection engine ships with an embedded test suite (the in-page
"Run Tests" button). To run it headlessly from the repo root:

```
node test_smoke.js
```

This extracts the inline engine from `hidayah-v1.3.0.html`, runs it in a Node
`vm` sandbox with DOM stubs, and executes the embedded `TESTS` array plus an
engine sanity check. Requires Node.js; no third-party dependencies. Exit code 0
and `SMOKE OK` indicate success.
