# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.

SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = DivioDocumentation
SOURCEDIR     = .
BUILDDIR      = _build
VENV = env/bin/activate
PORT = 9001

# list the targets that we don't want confused with files in the directory
.PHONY: help install clean run Makefile

# "help" is first so that "make" without an argument acts like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

install:
	@echo "... setting up virtualenv"
	python3 -m venv env
	. $(VENV); pip install --upgrade -r requirements.txt

	@echo "\n" \
	  "--------------------------------------------------------------- \n" \
      "* watch, build and serve the documentation: make run \n" \
	  "* check spelling: make spelling \n" \
	  "\n" \
      "enchant must be installed in order for pyenchant (and therefore \n" \
	  "spelling checks) to work. \n" \
	  "--------------------------------------------------------------- \n"

clean:
	-rm -r $(BUILDDIR)/*

run:
	. $(VENV); sphinx-autobuild $(ALLSPHINXOPTS) --ignore ".git/*" --ignore "*.scss" . -b dirhtml -a $(BUILDDIR)/html --host 0.0.0.0 --port $(PORT)

html:
	$(SPHINXBUILD) -b html . $(BUILDDIR)/html

open:
	open $(BUILDDIR)/html/index.html

test:
	sphinx-build -b html . $(BUILDDIR)/html

spelling:
	$(SPHINXBUILD) -b spelling $(ALLSPHINXOPTS) . $(BUILDDIR)/spelling
	@echo
	@echo "Check finished. Wrong words can be found in " \
		"$(BUILDDIR)/spelling/output.txt."

changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) . $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) . $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
