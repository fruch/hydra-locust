---
description: 'Cross-cutting lessons learned in hydra-locust development'
applyTo: '**/*'
---

# General Memory

> Cross-cutting lessons learned in hydra-locust development.

## gevent monkey-patching must come first

When using Locust, `gevent.monkey.patch_all()` must be called before any other imports. This is why `locustfile.py` and `dynamodb_case1.py` have `# noqa: E402` comments — imports after `patch_all()` are intentional and required.

## report_timings is a decorator factory

`report_timings(request_type)` returns a decorator. Use `report_timings_cql` and `report_timings_dynamodb` as convenience aliases. The decorator reports function execution timings to Locust's event system.
