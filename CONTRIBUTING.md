# Contributing

Thanks for helping improve the JWT Playground.

This project is meant to be a **teaching tool**, so code and UX should aim for
clarity over cleverness. Prefer small, focused changes that make JWT concepts
easier to explain in workshops.

## Local development

```bash
# Clone and set up a virtualenv
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt pytest mypy httpx

# Run the app
make run  # or ./scripts/run.sh

# Run tests and type checks
make test
make typecheck
```

## Style and testing

- Keep FastAPI routes and templates simple and explicit.
- Add tests for new scenarios and behaviour under `tests/`.
- Run `pytest` and `mypy app` before opening a pull request.
- If you add new external dependencies, keep them minimal and document why.

## Scenarios

When adding a scenario, think about:

- **Learning objective** – what JWT concept should someone understand better
  after using this scenario?
- **Threat model** – what historical bug or class of bug are we trying to
  make tangible?
- **Talking points** – add short explanations or hints in the UI and README
  that a facilitator can use.

