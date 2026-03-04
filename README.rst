Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-nitroclass/badge/?version=latest
    :target: https://circuitpython-nitroclass.readthedocs.io/
    :alt: Documentation Status


.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/tekktrik/CircuitPython_Nitroclass/workflows/Build%20CI/badge.svg
    :target: https://github.com/tekktrik/CircuitPython_Nitroclass/actions
    :alt: Build Status


.. image:: https://codecov.io/gh/tekktrik/CircuitPython_Nitroclass/graph/badge.svg?token=ZPTV7SXHIO
    :target: https://codecov.io/gh/tekktrik/CircuitPython_Nitroclass
    :alt: CodeCov Metrics


.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff


.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License: MIT


.. image:: https://img.shields.io/badge/License-PSF_2.0-yellow.svg
    :target: https://opensource.org/license/python-2-0
    :alt: License: PSF-2.0


.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
    :target: https://github.com/tekktrik/CircuitPython_CSV
    :alt: Maintained: Yes

Supercharge your CircuitPython classes similar to CPython dataclasses


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-nitroclass/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-nitroclass

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-nitroclass

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install circuitpython-nitroclass

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install circuitpython_nitroclass

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python

    from circuitpython_nitroclass import field, nitroclass

    @nitroclass
    class DataPacket:
        req = field(type=int)
        dyn = field(default_factory=list)
        cls_var = "a"


    x = DataPacket(req=1)
    y = DataPacket(req=2)

    assert x != y

    x.req = 2

    assert x == y

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-nitroclass.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/tekktrik/CircuitPython_Nitroclass/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
