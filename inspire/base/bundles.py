# -*- coding: utf-8 -*-
## This file is part of INSPIRE.
## Copyright (C) 2014 CERN.
##
## INSPIRE is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## INSPIRE is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
##
## In applying this licence, CERN does not waive the privileges and immunities
## granted to it by virtue of its status as an Intergovernmental Organization
## or submit itself to any jurisdiction.
"""Inspire bundles."""

from invenio.ext.assets import Bundle

styles = Bundle(
    'css/inspire.css',
    'css/font-awesome.min.css',
    output='base.css',
    weight=20,
)

index_js = Bundle(
    'js/jquery.feeds.min.js',
    output='index.js',
    weight=60,
    bower={
        "jquery-feeds": "git://github.com/camagu/jquery-feeds.git",
    },
)

# '_' prefix indicates private variables, and prevents duplicated import by
# auto-discovery service of invenio

from invenio.modules.search.bundles import js as _search_js

_search_js.contents += (
    'js/search/invenio_with_spires_typeahead_configuration.js',
    'js/search/search_box.js',
)

from invenio.modules.formatter.bundles import css as _formatter_css

_formatter_css.contents += (
    'css/formatter/templates_detailed_inspire.css',
)
