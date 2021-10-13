======================
Cookiecutter PyPackage
======================

Cookiecutter_ template for a Basic Python CLI Application, inspired by and cribbed from
`briggySmalls/cookiecutter-pypackage`_

* GitHub repo: https://github.com/midwatch/cc-py3-pkg
* Free software: MIT license

.. _briggySmalls/cookiecutter-pypackage: https://github.com/briggySmalls/cookiecutter-pypackage
.. _Cookiecutter: https://github.com/audreyr/cookiecutter


Features
--------

* Portable development environment using vagrant_
* Branch management using gitflow_
* Dependency tracking using poetry_
* Code linting provided by:

  * pylint_
  * pycodestyle_
  * pydocstyle_

* Code formanting provided by:

  * yapf_
  * isort_

* All development tasks (init, lint, format, test, etc) automated by invoke_


Limitations
--------

* No tox testing. Intended for a single deployment target only (eg Ubuntu 20.04 LTS/Python 3.8.x)
* Intended for Pyton CLI apps installed per user using pipx_
* Host dependencies need to be manually installed before installing app


Quickstart
----------

.. _gitflow: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow
.. _invoke: http://www.pyinvoke.org/
.. _isort: https://pypi.org/project/isort/
.. _pipx: https://pypa.github.io/pipx/
.. _poetry: https://python-poetry.org/
.. _pycodestyle: https://pycodestyle.pycqa.org/en/latest/
.. _pydocstyle: http://www.pydocstyle.org/en/stable/
.. _pylint: https://www.pylint.org/
.. _vagrant: https://www.vagrantup.com/
.. _yapf: https://github.com/google/yapf
