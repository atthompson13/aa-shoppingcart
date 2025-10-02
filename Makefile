.PHONY: help clean dev test

help:
	@echo "Available targets:"
	@echo "  dev    - Install development dependencies"
	@echo "  clean  - Remove build artifacts"
	@echo "  test   - Run tests"

clean:
	rm -rf dist build *.egg-info

dev:
	pip install -e .[test]

test:
	tox
