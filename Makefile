.PHONY: install format lint test-python test-go test parity validate \
	validate-translations experiments docs docs-en docs-fa serve serve-en serve-fa check test-blender-integration

PYTHON ?= python3
GOCACHE ?= /tmp/tahmures-go-cache

install:
	$(PYTHON) -m pip install -e ".[dev,docs]"

format:
	$(PYTHON) -m ruff format examples/python scripts
	$(PYTHON) -m ruff check --fix examples/python scripts
	gofmt -w examples/go

lint:
	$(PYTHON) -m ruff check examples/python scripts
	$(PYTHON) -m ruff format --check examples/python scripts
	test -z "$$(gofmt -l examples/go)"

test-python:
	$(PYTHON) -m pytest

test-go:
	GOCACHE=$(GOCACHE) go test ./...

test: test-python test-go

# The controller tests stub privileged/network commands; bridge tests use only
# ephemeral loopback fixtures. No live controller activation is performed.
test-blender-integration:
	$(PYTHON) -m ruff check integrations/blender-mcp
	$(PYTHON) -m ruff format --check integrations/blender-mcp
	bash -n integrations/blender-mcp/scripts/cloudflare-proxy.sh
	bash -n integrations/blender-mcp/scripts/run-bridge.sh
	bash -n integrations/blender-mcp/scripts/check-bridge.sh
	$(PYTHON) -m unittest discover -s integrations/blender-mcp/tests -v

parity:
	$(PYTHON) scripts/check_parity.py

validate:
	$(PYTHON) scripts/validate_chapters.py
	$(PYTHON) scripts/validate_continuity.py

validate-translations:
	$(PYTHON) scripts/validate_translations.py

experiments:
	$(PYTHON) scripts/run_all_experiments.py

docs: docs-en docs-fa

docs-en:
	$(PYTHON) -m mkdocs build --strict

docs-fa:
	$(PYTHON) -m mkdocs build -f mkdocs.fa.yml --strict

serve: docs
	$(PYTHON) -m http.server --bind 127.0.0.1 --directory site 8000

serve-en:
	$(PYTHON) -m mkdocs serve

serve-fa:
	$(PYTHON) -m mkdocs serve -f mkdocs.fa.yml

check: lint test test-blender-integration validate validate-translations editorial-check experiments parity docs

-include editorial.mk
