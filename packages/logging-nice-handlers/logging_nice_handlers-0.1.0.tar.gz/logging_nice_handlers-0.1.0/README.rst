=====================
logging_nice_handlers
=====================

.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/logging_nice_handlers
   :target: https://img.shields.io/github/last-commit/stas-prokopiev/logging_nice_handlers
   :alt: GitHub last commit

.. image:: https://img.shields.io/github/license/stas-prokopiev/logging_nice_handlers
    :target: https://github.com/stas-prokopiev/logging_nice_handlers/blob/master/LICENSE.txt
    :alt: GitHub license<space><space>

.. image:: https://readthedocs.org/projects/logging_nice_handlers/badge/?version=latest
    :target: https://logging_nice_handlers.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/stas-prokopiev/logging_nice_handlers.svg?branch=master
    :target: https://travis-ci.org/stas-prokopiev/char

.. image:: https://img.shields.io/pypi/v/logging_nice_handlers
   :target: https://img.shields.io/pypi/v/logging_nice_handlers
   :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/logging_nice_handlers
   :target: https://img.shields.io/pypi/pyversions/logging_nice_handlers
   :alt: PyPI - Python Version


.. contents:: **Table of Contents**

Overview.
=========================
This library consists of different logging handlers which I see usefull in different projects.

Installation via pip:
======================

.. code-block:: bash

    pip install char

logging Handlers
============================

AllLevelFileHandler
------------------------------
| This handler quite similar to logging.FileHandler but instead of FileHandler
| it saves not in one file but in separate file for every level
| So as the results in some directory you will get files

- debug_msgs.txt - For all messages for levels logging.DEBUG and above
- info_msgs.txt - For all messages for levels logging.INFO and above
- warning_msgs.txt - For all messages for levels logging.WARNING and above
- error_msgs.txt - For all messages for levels logging.ERROR and above

| Such structure of logs can be quite usefull if your projected is expected to be used by externel users
| So in case of some errors all these files with logs can be sent to the author and be analyzed.

.. code-block:: python

    import logging
    from logging_nice_handlers import AllLevelFileHandler

    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(10)
    LOGGER.addHandler(
        AllLevelFileHandler(
            str_path_dir_with_logs="Logs",
            str_open_mode="w",
        )
    )
    LOGGER.info("Hi friend!")

JupyterStreamHandler
------------------------------
| This handler is the replacement for logging.StreamHandler when it should be used in jupyter notebooks
| It will highlight in red all messages with the level which is above some set level.
| So you won't miss that the warnings or errors are happening in you programm.


.. code-block:: python

    import logging
    from logging_nice_handlers import JupyterStreamHandler

    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(10)
    LOGGER.addHandler(
        JupyterStreamHandler(
            int_min_stdout_level=logging.INFO,
            int_min_stderr_level=logging.WARNING,
        )
    )
    LOGGER.warning("Hi friend!")


Links
=====

    * `PYPI <https://pypi.org/project/logging_nice_handlers/>`_
    * `readthedocs <https://logging_nice_handlers.readthedocs.io/en/latest/>`_
    * `GitHub <https://github.com/stas-prokopiev/logging_nice_handlers>`_

Project local Links
===================

    * `CHANGELOG <https://github.com/stas-prokopiev/logging_nice_handlers/blob/master/CHANGELOG.rst>`_.
    * `CONTRIBUTING <https://github.com/stas-prokopiev/logging_nice_handlers/blob/master/CONTRIBUTING.rst>`_.

Contacts
========

    * Email: stas.prokopiev@gmail.com
    * `vk.com <https://vk.com/stas.prokopyev>`_
    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_

License
=======

This project is licensed under the MIT License.

