.PHONY: run test typecheck lint

run:
	./scripts/run.sh

test:
	. .venv/bin/activate && pytest

typecheck:
	. .venv/bin/activate && mypy app

lint:
	@echo "(linting not yet configured)"
