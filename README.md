# API Testing Framework

A pytest-based API test automation framework demonstrating data-driven testing, fixture design, and CI integration. Runs against the free [ReqRes](https://reqres.in) public API as a live example.

## Why this project

This isn't a toy script — it's structured the way a real test framework should be:
- **Separation of concerns**: API client logic is separate from test logic
- **Fixtures** for setup/teardown and shared config
- **Parametrized tests** for data-driven coverage
- **CI pipeline** that runs the suite on every push

## Structure

```
api-testing-framework/
├── api_client.py          # Thin wrapper around requests for the API under test
├── config.py               # Base URL, timeouts, env config
├── conftest.py              # Shared pytest fixtures
├── tests/
│   ├── test_users.py        # CRUD tests for the users endpoint
│   └── test_negative_cases.py  # Error handling / invalid input tests
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

- API test design (positive + negative cases)
- Reusable, maintainable framework architecture (not copy-pasted scripts)
- CI/CD integration — tests run automatically via GitHub Actions on every push
- Clear documentation, because untested code that no one can run isn't useful to anyone
