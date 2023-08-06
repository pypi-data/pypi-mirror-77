<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED IN THE NAMESPACE ROOT PACKAGE. CHANGES HAVE TO BE DONE THERE.
  All changes will be deployed automatically to all the portions of this namespace package.
-->
# db_pg portion of ae namespace package

[![GitLabPipeline](https://img.shields.io/gitlab/pipeline/ae-group/ae_db_pg/master?logo=python)](
    https://gitlab.com/ae-group/ae_db_pg)
[![PyPIVersion](https://img.shields.io/pypi/v/ae_db_pg)](
    https://pypi.org/project/ae-db-pg/#history)

>The portions (modules and sub-packages) of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes for to develop
full-featured applications with Python.

[![Coverage](https://ae-group.gitlab.io/ae_db_pg/coverage.svg)](
    https://ae-group.gitlab.io/ae_db_pg/coverage/ae_db_pg_py.html)
[![MyPyPrecision](https://ae-group.gitlab.io/ae_db_pg/mypy.svg)](
    https://ae-group.gitlab.io/ae_db_pg/lineprecision.txt)
[![PyLintScore](https://ae-group.gitlab.io/ae_db_pg/pylint.svg)](
    https://ae-group.gitlab.io/ae_db_pg/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_db_pg)](
    https://pypi.org/project/ae-db-pg/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_db_pg)](
    https://pypi.org/project/ae-db-pg/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_db_pg)](
    https://pypi.org/project/ae-db-pg/)
[![PyPIFormat](https://img.shields.io/pypi/format/ae_db_pg)](
    https://pypi.org/project/ae-db-pg/)
[![PyPIStatus](https://img.shields.io/pypi/status/ae_db_pg)](
    https://libraries.io/pypi/ae-db-pg)
[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_db_pg)](
    https://pypi.org/project/ae-db-pg/#files)


## installation


Execute the following command for to use the ae.db_pg module in your
application. It will install ae.db_pg into your python (virtual) environment:
 
```shell script
pip install ae-db-pg
```

If you instead want to contribute to this portion then first fork
[the ae_db_pg repository at GitLab](https://gitlab.com/ae-group/ae_db_pg "ae.db_pg code repository"),
then pull it to your machine and finally execute the following command in the root folder
of this repository (ae_db_pg):

```shell script
pip install -e .[dev]
```

The last command will install this module portion into your virtual environment, along with
the tools you need to develop and run tests or for to extend the portion documentation.
For to contribute only to the unit tests or the documentation of this portion replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

More info on the features and usage of this portion are available at
[ReadTheDocs](https://ae.readthedocs.io/en/latest/_autosummary/ae.db_pg.html#module-ae.db_pg
"ae_db_pg documentation").

<!-- Common files version 0.0.42 deployed  version 0.0.1 (with 0.0.42)
     to https://gitlab.com/ae-group as ae_db_pg module as well as
     to https://ae-group.gitlab.io with CI check results as well as
     to https://pypi.org/project as ae-db-pg package.
-->