.. -*- coding: utf-8; -*-

=======================================
 Convert YouTube Subtitle XML into srt
=======================================

This program converts youtube subtitle XML file into srt file.

Usage
=====

Specify subtitle XML file retrieved from YouTube as an input.
This outputs SRT onto your display.

.. code-block:: bash

   $ python main.py abcde.xml

You can specify output SRT filename with ``-o`` option.
The output file is written with UTF-8 encoding.

.. code-block:: bash

   $ python main.py -o abcde.srt abcde.xml

Limitation
==========

Not fully tested.

Copyright, License
==================

Copyright (c) 2017, Shigemi ISHIDA

This software is released under the BSD 3-clause license.
See ``LICENSE``.
