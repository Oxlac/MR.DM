.. _contributing:

Contributing
============

Open Source is driven by contributions. We are very happy seeing you here. We want to make the contribution process as easy and transparent as possible. It can range from (but not limited to):
- Reporting a bug
- Submitting a feature
- Submitting a fix
- Proposing features
- Becoming a maintainer

How to contribute?
------------------

All contrubutions are welcome. First check the open issues and see if you can help with any of them. If you want to add a new feature, please create an issue first so that others can have a look at it. Below are the steps you should follow so that your PR can be merged easily.
1. Check out the [issues](https://github.com/oxlac/mr-dm/issues) page.
2. If you want to contribute a new feature or solve a issue, it is recommended you make it an issue for others to have a brief look at what's happening if the proposed feature is not already in the open issues.
3. Fork the repo and create your branch from `master`.
4. To install the development dependecies(Includes dependencies required for writing documentation and building executables) run

.. code-block:: bash

    pip install -r requirements-dev.txt

.. note::
    This will install sphinx and its other dependecies along with py-two-exe which is used to build executables.

.. warning::
    Due to limitations in Kivy Dependencies this application can only be built on python 3.10.6 only. No other version is tested to support the application. If you want to build the application, please use python 3.10.6 only.

5. Make the changes you want to make.

6. Make sure your code lints. MR.Dm uses [ruff](https://github.com/astral-sh/ruff) for linting. To lint your code run

.. code-block:: bash

    ruff lint

.. note::
    If you are using VSCode, you can install the ruff extension to lint your code on the fly.

7. Commit your changes and push your branch to GitHub.
8. Create a pull request to the `master` branch of the `oxlac/mr-dm` repository.
9. Ensure that your code passes the ruff linter. If it does not pass view the errors and fix them.
10. If you have any questions, please feel free to ask in the Discord Server https://discord.gg/Jrd6A94g


How to report a bug?
--------------------
Use the issue templates to report a bug. Please provide as much information as possible. If you have a solution to the bug, please create a pull request.
