XARGS := xargs -0 $(shell test $$(uname) = Linux && echo -r)
GREP_T_FLAG := $(shell test $$(uname) = Linux && echo -T)
export PYFLAKES_BUILTINS=_

all:
	@echo "\nThere is no default Makefile target right now. Try:\n"
	@echo "make clean - reset the project and remove auto-generated assets."
	@echo "make pyflakes - run the PyFlakes code checker."
	@echo "make pep8 - run the PEP8 style checker."
	@echo "make test - run the test suite."
	@echo "make coverage - view a report on test coverage."
	@echo "make check - run all the checkers and tests."
	@echo "make dist - make a dist/wheel for the project."
	@echo "make publish-test - publish the project to PyPI test instance."
	@echo "make publish-live - publish the project to PyPI production."
	@echo "make docs - run sphinx to create project documentation."
	@echo "make translate - create a new messages.pot file for Mu related strings."
	@echo "make translateall - as with translate but also containing all API strings.\n"

clean:
	rm -rf build
	rm -rf dist
	rm -rf mu_editor.egg-info
	rm -rf .coverage
	rm -rf docs/_build
	find . \( -name '*.py[co]' -o -name dropin.cache \) -delete
	find . \( -name '*.bak' -o -name dropin.cache \) -delete
	find . \( -name '*.tgz' -o -name dropin.cache \) -delete
	find . | grep -E "(__pycache__)" | xargs rm -rf

pyflakes:
	find . \( -name _build -o -name var -o -path ./docs -o -path ./mu/contrib -o -path ./utils \) -type d -prune -o -name '*.py' -print0 | $(XARGS) pyflakes

pycodestyle:
	find . \( -name _build -o -name var \) -type d -prune -o -name '*.py' -print0 | $(XARGS) -n 1 pycodestyle --repeat --exclude=build/*,docs/*,mu/contrib*,mu/modes/api/*,utils/* --ignore=E731,E402

test: clean
	pytest

coverage: clean
	pytest --cov-config .coveragerc --cov-report term-missing --cov=mu tests/

check: clean pycodestyle pyflakes coverage

dist: check
	@echo "\nChecks pass, good to package..."
	python setup.py sdist bdist_wheel

publish-test: dist
	@echo "\nPackaging complete... Uploading to PyPi..."
	twine upload -r test --sign dist/*

publish-live: dist 
	@echo "\nPackaging complete... Uploading to PyPi..."
	twine upload --sign dist/*

docs: clean
	$(MAKE) -C docs html
	@echo "\nDocumentation can be found here:"
	@echo file://`pwd`/docs/_build/html/index.html
	@echo "\n"

translate:
	find . \( -name _build -o -name var -o -path ./docs -o -path ./mu/contrib -o -path ./utils -o -path ./mu/modes/api \) -type d -prune -o -name '*.py' -print0 | $(XARGS) pygettext
	@echo "\nNew messages.pot file created."
	@echo "Remember to update the translation strings found in the locale directory."

translateall:
	pygettext mu/* mu/debugger/* mu/modes/* mu/resources/*
	@echo "\nNew messages.pot file created."
	@echo "Remember to update the translation strings found in the locale directory."
