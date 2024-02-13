RUNNER=docker-compose run --rm python

_install:
	$(RUNNER) pip install -r requirements.txt
.PHONY: _install

run: _install
	$(RUNNER) python main.py
.PHONY: run

tests: _install
	$(RUNNER) python -m unittest -v
.PHONY: tests