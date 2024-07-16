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
	@echo "make translate_begin LANG=xx_XX - create/update a mu.po file for translation."
	@echo "make translate_done LANG=xx_XX - compile translation strings in mu.po to mu.mo file."
	@echo "make translate_test LANG=xx_XX - run translate_done and launch Mu in the given LANG."
	@echo "make win32 - create a 32bit Windows installer for Mu."
	@echo "make win64 - create a 64bit Windows installer for Mu."
	@echo "make macos - create a macOS native application for Mu."
	@echo "make video - create an mp4 video representing code commits.\n"

clean:
	rm -rf build
	rm -rf dist
	rm -rf .coverage
	rm -rf .eggs
	rm -rf *.egg-info
	rm -rf docs/_build
	rm -rf .pytest_cache
	rm -rf lib
	rm -rf *.mp4
	rm -rf .git/avatar/*
	rm -rf venv-pup
	find . \( -name '*.py[co]' -o -name dropin.cache \) -delete
	find . \( -name '*.bak' -o -name dropin.cache \) -delete
	find . \( -name '*.tgz' -o -name dropin.cache \) -delete
	find . | grep -E "(__pycache__)" | xargs rm -rf
	rm -f ./mu/locale/messages.pot
	rm -f ./mu/wheels/*.zip

run: clean
ifeq ($(VIRTUAL_ENV),)
	@echo "\n\nCannot run Mu. Your Python virtualenv is not activated."
else
	python run.py
endif

flake8:
	@python make.py flake8

test: clean
	export LANG=en_GB.utf8
	pytest -v --random-order

coverage: clean
	export LANG=en_GB.utf8
	pytest -v --random-order --cov-config setup.cfg --cov-report term-missing --cov=mu tests/

tidy:
	python make.py tidy

black:
	python make.py black

# check: clean black flake8 coverage
check: clean # temporary for a build

dist: check
	@echo "\nChecks pass, good to package..."
	python setup.py sdist bdist_wheel

publish-test: dist
	@echo "\nPackaging complete... Uploading to PyPi..."
	twine upload -r test --sign dist/*

publish-live: dist
	@echo "\nPackaging complete... Uploading to PyPi..."
	twine upload --sign dist/*

docs:
	@python make.py docs
	@echo "\nDocumentation can be found here:"
	@echo file://`pwd`/docs/_build/html/index.html
	@echo "\n"

translate_begin:
	@python make.py translate_begin LANG=$(LANG)

translate_done:
	@python make.py translate_done LANG=$(LANG)

translate_test:
	@python make.py translate_test LANG=$(LANG)

win32: check
	@echo "\nBuilding 32bit Windows MSI installer."
	python make.py win32

win64: check
	@echo "\nBuilding 64bit Windows MSI installer."
	python make.py win64

macos: check
	@echo "\nFetching wheels."
	python -m mu.wheels --package
	@echo "\nPackaging Mu into a macOS native application."
	python -m virtualenv venv-pup
	# Don't activate venv-pup because:
	# 1. Not really needed.
	# 2. Previously active venv would be "gone" on venv-pup deactivation.
	# Installing pup from a fork with the --pip-platform flag proof of concept
	# and using it to install wheels for the `macosx_10_12_x86_64` platform
	./venv-pup/bin/pip install git+https://github.com/carlosperate/pup.git@pip-platform
	./venv-pup/bin/pup package --launch-module=mu --nice-name="Mu Editor" --icon-path=./package/icons/mac_icon.icns --license-path=./LICENSE --pip-platform=macosx_10_12_x86_64 .
	rm -r venv-pup
	ls -la ./build/pup/
	ls -la ./dist/

linux: check
	@echo "\nFetching wheels."
	python -m mu.wheels --package
	@echo "\nPackaging Mu into a Linux AppImage."
	python -m virtualenv venv-pup
	# Don't activate venv-pup because:
	# 1. Not really needed.
	# 2. Previously active venv would be "gone" on venv-pup deactivation.
	./venv-pup/bin/pip install pup
	./venv-pup/bin/pup package --launch-module=mu --nice-name="Mu Editor" --icon-path=./mu/resources/images/icon.png --license-path=./LICENSE .
	rm -r venv-pup
	ls -la ./build/pup/
	ls -la ./dist/

linux-docker: clean
	@echo "\nFetching wheels."
	docker run -v $(CURDIR):/home --rm ghcr.io/mu-editor/mu-appimage:2022.05.01 bash -c "\
		pip install . && \
		python -m mu.wheels --package"
	@echo "\nInstall pup inside the container, build the Linux AppImage, and tar it."
	# pup build directory is hardcoded to ./build, but the build fails if the build folder is inside the docker mounted volume
	# So let's mount the Mu repo into a subdirectory and then invoke pup from the parent folder
	# https://github.com/mu-editor/pup/issues/242
	docker run -v $(CURDIR):/home/mu --rm ghcr.io/mu-editor/mu-appimage:2022.05.01 bash -c "\
		pip install virtualenv && \
		python -m virtualenv venv-pup && \
		./venv-pup/bin/pip install pup && \
		./venv-pup/bin/pup package --launch-module=mu --nice-name='Mu Editor' --icon-path=mu/mu/resources/images/icon.png --license-path=mu/LICENSE mu/ && \
		cd dist/ && \
		find *.AppImage -type f -exec tar -cvf {}.tar {} \; && \
		cd /home && \
		mv build/pup mu/build/pup && \
		mv dist/ mu/dist"
	ls -la ./build/pup/
	ls -la ./dist/

video: clean
	@echo "\nFetching contributor avatars."
	python utils/avatar.py
	@echo "\nMaking video of source commits."
	gource --user-image-dir .git/avatar/ --title "The Making of Mu" --logo docs/icon_small.png --font-size 24 --file-idle-time 0 --key -1280x720 -s 0.1 --auto-skip-seconds .1 --multi-sampling --stop-at-end --hide mouse,progress --output-ppm-stream - --output-framerate 30 | ffmpeg -y -r 30 -f image2pipe -vcodec ppm -i - -b 65536K movie.mp4
