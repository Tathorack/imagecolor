# mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
# current_dir = $(patsubst %/,%,$(dir $(mkfile_path)))
#
# PIPENV        = cd $(current_dir) && pipenv run

PIPENV        = pipenv run
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = imagecolor
DOCSSOURCEDIR     = docs/source
DOCSBUILDDIR      = docs/build

all : release html

release : test source-dist wheel-dist

source-dist :
	@$(PIPENV) python setup.py sdist

wheel-dist :
	@$(PIPENV) python setup.py bdist_wheel

clean :
	rm -rf build/
	rm -rf dist/
	rm -rf imagecolor.egg-info
	rm -rf docs/build
	rm -rf .cache

lint :
# @$(PIPENV) pylint --rcfile=.pylintrc imagecolor -f parseable -r n
	@$(PIPENV) pylint imagecolor -f parseable -r n && \
	$(PIPENV) pycodestyle imagecolor && \
	$(PIPENV) pydocstyle imagecolor

test : lint
	@$(PIPENV) python3 -m pytest

html :
	@$(PIPENV) $(SPHINXBUILD) -M html "$(DOCSSOURCEDIR)" "$(DOCSBUILDDIR)" $(SPHINXOPTS) $(O)
