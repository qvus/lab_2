.PHONY: test run

PYTHON ?= python3

test:
	$(PYTHON) -m unittest discover -s tests -v

run:
	$(PYTHON) main.py
