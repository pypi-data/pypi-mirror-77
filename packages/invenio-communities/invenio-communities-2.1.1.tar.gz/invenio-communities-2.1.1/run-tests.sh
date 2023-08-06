#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

isort invenio_communities tests --check-only --diff && \
check-manifest --ignore ".travis-*" && \
pytest

# TODO: Enable when tests are in place
# pydocstyle invenio_communities tests && \
# isort -rc -c -df && \
# check-manifest --ignore ".travis-*" && \
# sphinx-build -qnNW docs docs/_build/html && \
# pytest && \
# sphinx-build -qnNW -b doctest docs docs/_build/doctest
