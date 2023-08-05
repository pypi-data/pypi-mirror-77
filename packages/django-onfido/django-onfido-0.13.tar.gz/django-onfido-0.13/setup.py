# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onfido',
 'onfido.management',
 'onfido.management.commands',
 'onfido.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0', 'python-dateutil', 'requests', 'simplejson']

setup_kwargs = {
    'name': 'django-onfido',
    'version': '0.13',
    'description': 'Django app for integration with Onfido.',
    'long_description': '.. image:: https://travis-ci.org/yunojuno/django-onfido.svg?branch=master\n    :target: https://travis-ci.org/yunojuno/django-onfido\n\n.. image:: https://badge.fury.io/py/django-onfido.svg\n    :target: https://badge.fury.io/py/django-onfido\n\nDjango Onfido\n==============\n\nDjango app for integration with the Onfido API (v2)\n\nBackground\n----------\n\nOnfido is an online identity verification service. It provides API access to a\nrange of tests (identity, right to work, criminal history, credit report). It\nis assumed that you are only interested in this project because you are\nalready aware of what Onfido does, and so I won\'t repeat it here. If you want\nto find out more, head over to their website.\n\nIf you *are* using Onfido, and you are using Django, then this project can be\nused to manage Onfido checks against your existing Django users. It handles\nthe API interactions, as well as providing the callback webhooks required to\nsupport live status updates.\n\nInstallation\n------------\n\nThe project is available through PyPI as ``django-onfido``:\n\n.. code::\n\n    $ pip install django-onfido\n\nAnd the main package itself is just ``onfido``:\n\n.. code:: python\n\n    >>> from onfido import api, models, views, urls, admin, signals, helpers, decorators\n\nUsage\n-----\n\nThe main use case is as follows:\n\n1. Create an Onfido **Applicant** from your Django user:\n\n.. code:: python\n\n    >>> from django.contrib.auth import get_user_model\n    >>> from onfido.helpers import create_applicant\n    >>> user = get_user_model().objects.last()  # any old one will do\n    >>> applicant = create_applicant(user)\n    DEBUG Making POST request to https://api.onfido.com/v2/applicants\n    DEBUG <Response [201]>\n    DEBUG {u\'first_name\': u\'hugo\', u\'last_name\': u\'rb\', u\'middle_name\': None, ...}\n    DEBUG Creating new Onfido applicant from JSON: {u\'first_name\': u\'hugo\', u\'last_name\': u\'rb\', ...}\n    <Applicant id=a2c98eae-XXX user=\'hugo\'>\n\n2. Create your check + reports for the applicant:\n\n.. code:: python\n\n    >>> from onfido.helpers import create_check\n    >>> create_check(applicant, \'standard\', [\'identity\', \'right_to_work\'])\n    >>> assert Check.objects.count() == 1\n    >>> assert Report.objects.count() == 2\n\nThis will create the **Check** and **Report** objects on Onfido, and store them locally as Django model objects.\n\n3. Wait for callback events to update the status of reports and checks:\n\n.. code:: shell\n\n    DEBUG Received Onfido callback: {"payload":{...}}\n    DEBUG Processing \'check.completed\' action on check.bd8232c4-...\n\nNB If you are using the callback functionality, you **must** set the ``ONFIDO_WEBHOOK_TOKEN``\nproperty (see settings section below). The callback handler will force verification of the\nX-Signature request header as specified in the `webhooks documentation <https://documentation.onfido.com/#webhooks>`_.\n\nThe raw JSON returned from the API for a given entity (``Applicant``,\n``Check``, ``Report``) is stored on the model as the ``raw`` attribute, and\nthis can be parsed into the relevant model attributes. (Yes this does mean\nduplication of data.) The core pattern for interaction with the API on a per-\nobject basis is a read-only fetch / pull pattern (analagous to git operations\nof the same name). If you call the ``fetch`` method on an object, it will use\nthe ``href`` value in the raw JSON to fetch the latest data from the API and\nparse it, but without saving the changes. If you want to update the object,\nuse the ``pull`` method instead.\n\nThe ``Report`` object is a special case, where the raw data from the API often\ncontains sensitive information that you may not wish to store locally\n(passport numbers, Visa information, personal data). In order to get around\nthis, there is a ``scrub_report_data`` function that will remove certain\nattributes of the raw data before it is parsed. By default this will remove\nthe ``breakdown`` and ``properties`` elements.\n\n.. code:: python\n\n    >>> check = Check.objects.last()\n    >>> check.raw\n    {\n        "id": "c26f22d5-4903-401f-8a48-7b0211d03c1f",\n        "created_at": "2016-10-15T19:05:50Z",\n        "status": "awaiting_applicant",\n        "type": "standard",\n        "result": "clear",\n        "href": "applicants/123/checks/456"\n    }\n    >>> check.fetch()  # fetch and parse the latest raw data\n    >>> check.pull()  # calls fetch and then saves the object\n\nThere is a management command ``onfido_sync`` which can be used to ``pull`` all the objects\nin a queryset. It takes a single positional arg - \'applicant\', check\' or \'report\', and has two\noptions - ``--filter`` and ``--exclude`` - both of which take multiple space-separated\nargs which can be used to manage the queryset that is used.\n\nExamples:\n\n.. code:: bash\n\n    $ ./manage.py onfido_sync check\n    $ ./manage.py onfido_sync report\n    $ ./manage.py onfido_sync check --filter complete\n    $ ./manage.py onfido_sync check --exclude complete\n\nSettings\n--------\n\nThe following settings can be specified as environment settings or within the Django settings.\n\n* ``ONFIDO_API_KEY``: your API key, found under **setting** in your Onfido account.\n* ``ONFIDO_WEBHOOK_TOKEN``: (optional) the Onfido webhook callback token - required if using webhooks.\n\nThe following settings can be specified in the Django settings:\n\n* ``ONFIDO_LOG_EVENTS``: (optional) if True then callback events from the API will also be recorded as ``Event`` objects. Defaults to False.\n* ``ONFIDO_REPORT_SCRUBBER``: (optional) a function that is used to scrub sensitive data from ``Report`` objects. The default implementation will remove **breakdown** and **properties**.\n\nTests\n-----\n\nThe project has pretty good test coverage (>90%) and the tests themselves run through ``tox``.\n\n.. code::\n\n    $ pip install tox\n    $ tox\n\nIf you want to run the tests manually, make sure you install the requirements, and Django.\n\n.. code::\n\n    $ pip install -r requirements.txt\n    $ pip install django==1.8  # your version goes here\n    $ python manage.py test onfido.tests\n\nIf you are hacking on the project, please keep coverage up.\n\nContributing\n------------\n\nStandard GH rules apply: clone the repo to your own account, create a branch,\nmake sure you update the tests, and submit a pull request.\n\nStatus\n------\n\nThis project is very early in its development. We are using it at YunoJuno,\nbut \'caveat emptor\'. It currently only supports \'standard\' checks, and has\nvery patchy support for the full API. It does what we need it to do right now,\nand we will extend it as we evolve. If you need or want additional features,\nget involved :-).\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-onfido',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
