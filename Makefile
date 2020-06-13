XARGS := xargs -0 $(shell test $$(uname) = Linux && echo -r)
GREP_T_FLAG := $(shell test $$(uname) = Linux && echo -T)
export PYFLAKES_BUILTINS=_

all:
	@echo "\nThere is no default Makefile target right now. Try:\n"
	@echo "make run - run the local development version of Mu."
	@echo "make clean - reset the project and remove auto-generated assets."
	@echo "make flake8 - run the flake8 code checker."
	@echo "make test - run the test suite."
	@echo "make coverage - view a report on test coverage."
	@echo "make tidy - tidy code with the 'black' formatter."
	@echo "make check - run all the checkers and tests."
	@echo "make dist - make a dist/wheel for the project."
	@echo "make publish-test - publish the project to PyPI test instance."
	@echo "make publish-live - publish the project to PyPI production."
	@echo "make docs - run sphinx to create project documentation."
	@echo "make translate - create a messages.pot file for translations."
	@echo "make translateall - as with translate but for all API strings."
	@echo "make win32 - create a 32bit Windows installer for Mu."
	@echo "make win64 - create a 64bit Windows installer for Mu."
	@echo "make macos - create a macOS native application for Mu."
	@echo "make video - create an mp4 video representing code commits.\n"

clean:
	rm -rf build
	rm -rf dist
	rm -rf .coverage
	rm -rf .eggs
	rm -rf docs/_build
	rm -rf .pytest_cache
	rm -rf lib
	rm -rf pynsist_pkgs
	rm -rf pynsist_tkinter*
	rm -rf macOS
	rm -rf *.mp4
	rm -rf .git/avatar/*
	find . \( -name '*.py[co]' -o -name dropin.cache \) -delete
	find . \( -name '*.bak' -o -name dropin.cache \) -delete
	find . \( -name '*.tgz' -o -name dropin.cache \) -delete
	find . | grep -E "(__pycache__)" | xargs rm -rf

run: clean
ifeq ($(VIRTUAL_ENV),)
	@echo "\n\nCannot run Mu. Your Python virtualenv is not activated."
else
	python run.py
endif

flake8:
	flake8

test: clean
	pytest --random-order

coverage: clean
	pytest --random-order --cov-config .coveragerc --cov-report term-missing --cov=mu tests/

tidy: clean
	@echo "\nTidying code with black..."
	black -l 79 setup.py 
	black -l 79 win_installer.py
	black -l 79 make.py
	black -l 79 mu 
	black -l 79 package 
	black -l 79 tests
	black -l 79 utils 

check: clean tidy flake8 coverage

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

win32: check
	@echo "\nBuilding 32bit Windows installer."
	python win_installer.py 32 setup.py

win64: check
	@echo "\nBuilding 64bit Windows installer."
	python win_installer.py 64 setup.py

macos: check
	@echo "\nPackaging Mu into a macOS native application."
	briefcase create
	briefcase build
	briefcase package --no-sign

video: clean
	@echo "\nFetching contributor avatars."
	python utils/avatar.py
	@echo "\nMaking video of source commits."
	gource --user-image-dir .git/avatar/ --title "The Making of Mu" --logo ~/Pictures/icon.png --font-size 24 --file-idle-time 0 --key -1280x720 -s 0.1 --auto-skip-seconds .1 --multi-sampling --stop-at-end --hide mouse,progress --output-ppm-stream - --output-framerate 30 | ffmpeg -y -r 30 -f image2pipe -vcodec ppm -i - -b 65536K movie.mp4
