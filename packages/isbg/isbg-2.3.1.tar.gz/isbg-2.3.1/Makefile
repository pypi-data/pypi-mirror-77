#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

# Note: required utilities:
# - For test: pytest
# - For cov: python-pytest-cov and python3-pytest-cov, also
#            python-coverage
# - For docs: sphinx and recommonmark
TEST   = pytest-3 -m "not spamassassin"
COV    = pytest-3 -m "not spamassassin" --cov-append --cov isbg -m 2
COVREP = python3-coverage
COVDIR = build/htmlcov

.PHONY: help all test-clean test cov-clean cov docs clean \
        distclean build build-clean man sphinx sphinx-clean

help:
	@echo "Please use 'make <target>' where target is one of:"
	@echo "  help       to show this help message."
	@echo "   "
	@echo "  test       to run the tests."
	@echo "  cov        to check test 'coverage'."
	@echo "   "
	@echo "  build      build create a build dist 'python3 setup.py'."
	@echo "  docs       build the docs with 'sphinx'."
	@echo "    html     build only html pages"
	@echo "    man      build only manpages"
	@echo "   "
	@echo "  clean      clean generates files."
	@echo "  distclean  clean all generates files."


all: help

# -------------------------------------------------------------------- #
test-clean:
	rm -fr .pytest_cache
	rm -fr .cache

test:
	@$(TEST)

cov-clean:
	@$(COVREP) erase | true
	rm -f .coverage
	rm -fr $(COVDIR)

cov: cov-clean
	@$(COV)
	@$(COVREP) html --directory $(COVDIR)

# -------------------------------------------------------------------- #
build-clean:
	python3 setup.py clean
	rm -fr build/build
	rm -fr .eggs

build:
	python3 setup.py build -b build/build -t build/tmp
	python3 setup.py sdist -d build/dist --formats=bztar,zip
	python3 setup.py bdist -d build/dist
	python3 setup.py bdist_egg -d build/dist
	python3 setup.py bdist_wheel -d build/dist
	rm -fr isbg.egg-info
	rm -fr build/lib.*
	rm -fr build/bdist.*
	mv -f dist/* build/dist
	rmdir dist
	@echo "   "
	@echo "  See build/build for generated build files."
	@echo "  See build/dist for generated dist files."

# -------------------------------------------------------------------- #
sphinx-clean:
	rm -fr build.sphinx

sphinx:
	mkdir -p build.sphinx
	cp -fr docs/* build.sphinx
	# $(MAKE) -C build.sphinx apidoc  # It's called from sphinx

html: sphinx
	$(MAKE) -C build.sphinx html

man: sphinx
	$(MAKE) -C build.sphinx man

docs-clean: sphinx-clean
	$(MAKE) -C docs clean
	$(MAKE) -C docs clean-all

docs: html man
	@echo "   "
	@echo "  See build/sphinx/html for generated html docs."
	@echo "  See build/sphinx/man for generated manpages."

# -------------------------------------------------------------------- #
clean: test-clean sphinx-clean build-clean
	find . -name '*.pyc' -exec rm -f {} +
	rm -fr isbg/__pycache__
	rm -fr tests/__pycache__

distclean: clean cov-clean docs-clean
	$(MAKE) -C docs clean-all
	rm -fr build
	rm -fr dist
	rm -fr sdist
	rm -fr isbg.egg-info
	rm -f installed_files.txt
