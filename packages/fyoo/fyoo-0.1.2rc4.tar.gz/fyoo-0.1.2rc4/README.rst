Fyoo
====

|PyPI Package|
|Documentation| 
|Git tag|
|Test status|
|Code coverage|

Fyoo is a simple argument templatizer that wraps around a command.
CLIs exist for pretty much everything, isn't it about time we
started using them in our pipelines as they are? The best data
flow code is code you don't have to write.

Installation
------------

.. code-block:: bash

   pip install fyoo

Basic Usage
-----------

Fyoo can provide context to a subcommand's arguments after ``--``.
All arguments to that subcommand become pre-rendered jinja2 templates.

Fyoo allows you to inject context into shell arguments in a few
ways, ``--fyoo-set`` being the simplest and easiest to get started
with.

.. code-block:: bash
   
   fyoo \
     --set table=Employee \
     -- \
   sqlite3 \
     'examples/Chinook_Sqlite.sqlite' \
     'select * from {{ table }} where date(HireDate) < "{{ date() }}"' \
     -csv -header
   # ... csv results

This goes further than simple bash replacement, because you have
the full template power of jinja2 between when arguments are
processed and before the process is started.

Let's use this sql template file now.

.. code-block:: sql
   :name: count-sql-jinja

   {%- if not table %}
     {{ throw("'table' required") }}
   {%- endif %}

   select count(*)
   from {{ table }}
   {%- if condition %}
     where ({{ condition }})
   {%- endif %}

The template file contents are passed as a bash argument, but then
fyoo renders the template before passing it to sqllite3 subcommand.

The ``-v/--verbose`` flag will show the executable before running
it.

.. code-block:: bash

   fyoo \
     --verbose \
     --jinja-template-folder ./tests/sql \
     --set table=Employee \
     --set condition='lower(Title) like "%sales%"' \
     -- \
   sqlite3 \
     'examples/Chinook_Sqlite.sqlite' \
     '{% include "count.sql.jinja" %}' \
     -csv
   # ["sqlite3", "examples/Chinook_Sqlite.sqlite", "\nselect count(*) as c\nfrom Employee\nwhere (lower(Title) like \"%sales%\")", "-csv"]
   # 4

.. warning::

   Only pass context that you trust! Otherwise you may be leaving yourself
   wide open for `Command Injection`_. Fyoo is suited for use-cases where *you*
   are still directly in control of template context.

.. links

.. |PyPI Package| image:: https://img.shields.io/pypi/v/fyoo.svg
   :target: https://pypi.python.org/pypi/fyoo/
.. |Documentation| image:: https://readthedocs.org/projects/fyoo/badge/?version=latest
    :target: https://fyoo.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. |Git tag| image:: https://img.shields.io/github/tag/brian-bk/fyoo.svg
   :target: https://github.com/brian-bk/fyoo/commit/
.. |Test status| image:: https://circleci.com/gh/brian-bk/fyoo/tree/master.svg?style=svg
    :target: https://circleci.com/gh/brian-bk/fyoo/tree/master
.. |Code coverage| image:: https://codecov.io/gh/brian-bk/fyoo/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/brian-bk/fyoo
.. _Command Injection: https://owasp.org/www-community/attacks/Command_Injection
.. _Pipenv: https://pipenv-fork.readthedocs.io/
