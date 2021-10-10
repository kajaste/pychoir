all: test doctest isort lint typecheck docs

##
# <all>

test:
	pytest --cov=pychoir/ tests/
.PHONY: test

test_clean:
	rm -f .coverage
	rm -rf .pytest_cache
.PHONY: test_clean

doctest:
	python -m doctest pychoir/[!_]*.py
.PHONY: doctest

isort:
	isort pychoir/ tests/
.PHONY: isort

lint:
	flake8 pychoir/ tests/
.PHONY: lint

typecheck:
	mypy pychoir/ tests/
.PHONY: typecheck

typecheck_clean:
	rm -rf .mypy_cache/
.PHONY: typecheck_clean

docs:
	make -C docs/ html
.PHONY: docs

docs_clean:
	make -C docs/ clean
.PHONY: docs_clean

# </all>
##


##
# These are not needed that often

tox:
	tox
.PHONY: tox

tox_clean: package_clean typecheck_clean test_clean
	rm -rf .tox/*
.PHONY: tox_clean

package: package_clean
	python setup.py sdist bdist_wheel
.PHONY: package

package_clean:
	rm -rf build/
	rm -rf dist/
	rm -rf pychoir.egg-info/
	rm -f pychoir/_version.py
.PHONY: package_clean

upload:
	twine upload dist/*
.PHONY: upload

clean: test_clean typecheck_clean docs_clean package_clean
