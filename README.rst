.. highlight:: shell

=======
Knxproj
=======

Unzip a knxproj and read the xml files.

Intro in a nutshell
------------------------------------
0. Install python3 and pipenv
1. Clone this repository

.. code-block:: console

    $ git clone git://github.com/fgoettel/knxproj

2. Install the virtual environment

.. code-block:: console

    $ pipenv install

3. Explore the examples, e.g.,

.. code-block:: console

    $ pipenv shell
    $ python knxproj/examples/example_read_switches.py /Path/To/project.knxproj


Features
--------

* Read a .Knxproj


TODOS
-----
* Check exports from ETS != 5.7
* Check on Windows
* MDT GT
    * Nice documentation
    * Nice examples
    * Evaluate kurz/lang and print both
    * Layout other than 2*6
    * Notify LED / Message usage
    * Good tests
    * Good test coverage



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
