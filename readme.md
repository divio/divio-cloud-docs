# Divio Cloud documentation for developers

This documentation is intended for developers using the Divio Cloud.

## Build the documentation locally

You'll need the [enchant](https://www.abisource.com/projects/enchant/) library,
used by ``pyenchant`` for spelling.

Install with ``brew install enchant`` (macOS) or the appropriate command for
your system.

Then:

    git clone git@github.com:divio/divio-cloud-docs.git  # clone
    cd divio-cloud-docs
    make install  # create a virtualenv and install required components
    make run  # build and serve the documentation
    open http://localhost:8001  # open it in a browser

