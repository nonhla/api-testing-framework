# API Testing Framework

A pytest-based API test automation framework demonstrating data-driven testing, fixture design, auth handling, and CI integration. Runs against [Restful-Booker](https://restful-booker.herokuapp.com) — a public API built specifically for practicing API test automation.

## Why this project

This isn't a toy script — it's structured the way a real test framework should be:
- **Separation of concerns**: API client logic is separate from test logic
- **Auth handling**: token-based authentication (via `POST /auth`) for protected endpoints, cached per session
- **Fixtures** for setup/teardown, shared config, and reusable test data
- **Parametrized tests** for data-driven coverage
- **CI pipeline** that runs the suite on every push

## Structure

```
api-testing-framework/
├── api_client.py          # Thin wrapper around requests, incl. auth handling
├── config.py               # Base URL, timeouts, credentials
├── conftest.py              # Shared pytest fixtures (client, payloads, created records)
├── tests/
│   ├── test_booking.py        # CRUD tests for the /booking endpoint
│   └── test_negative_cases.py # Auth enforcement, invalid input, filtering
├── requirements.txt
└── .github/workflows/tests.yml  # CI pipeline
```

## Running locally

```bash
pip install -r requirements.txt
pytest -v
```

## Running with HTML report

```bash
pytest --html=report.html --self-contained-html
```

## What this demonstrates

- API test design (positive + negative cases, including auth enforcement)
- Token-based auth handled once in the client, not repeated in every test
- Reusable, maintainable framework architecture (not copy-pasted scripts)
- CI/CD integration — tests run automatically via GitHub Actions on every push
- Clear documentation, because untested code that no one can run isn't useful to anyone

## A note on the demo API

Restful-Booker is a shared public instance that **resets every 10 minutes** back to its default seeded data. The test suite is written defensively around that — creating its own booking records rather than assuming specific IDs exist — but a reset mid-run could occasionally cause a rare flake. That's a realistic constraint of testing against any shared, non-isolated environment.
