# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from __future__ import absolute_import, division, print_function

import pytest
from flask import current_app
from mock import patch
from wtforms.validators import StopValidation

from inspirehep.modules.forms.validation_utils import (
    DOISyntaxValidator,
    ORCIDValidator,
)


class MockField(object):
    def __init__(self, data):
        self.data = data


class MockOrcidAPI(object):
    def __init__(self, response):
        self._response = response

    def search_member(self, query):
        return self._response


def test_doi_syntax_validator_accepts_valid_dois():
    field = MockField(u'10.1086/305772')
    doi_syntax_validator = DOISyntaxValidator()

    assert doi_syntax_validator(None, field) is None


def test_doi_syntax_validator_accepts_valid_dois_with_doi_prefix():
    field = MockField(u'doi:10.1086/305772')
    doi_syntax_validator = DOISyntaxValidator()

    assert doi_syntax_validator(None, field) is None


def test_doi_syntax_validator_raises_on_invalid_dois():
    field = MockField(u'dummy:10.1086/305772')
    doi_syntax_validator = DOISyntaxValidator()

    with pytest.raises(StopValidation):
        assert doi_syntax_validator(None, field)


@patch('inspirehep.modules.forms.validation_utils.orcid.MemberAPI')
def test_orcid_validator_accepts_existing_orcids(mock_member_api):
    mock_orcid_api = MockOrcidAPI({'orcid-search-results': {'num-found': 1}})
    mock_member_api.return_value = mock_orcid_api

    config = {
        'ORCID_APP_CREDENTIALS': {
            'consumer_key': 'consumer_key',
            'consumer_secret': 'consumer_secret',
        }
    }

    with patch.dict(current_app.config, config):
        field = MockField(u'0000-0003-1032-3957')

        assert ORCIDValidator(None, field) is None


@patch('inspirehep.modules.forms.validation_utils.orcid.MemberAPI')
def test_orcid_validator_raises_on_non_existing_orcids(mock_member_api):
    mock_orcid_api = MockOrcidAPI({'orcid-search-results': {'num-found': 0}})
    mock_member_api.return_value = mock_orcid_api

    config = {
        'ORCID_APP_CREDENTIALS': {
            'consumer_key': 'consumer_key',
            'consumer_secret': 'consumer_secret',
        }
    }

    with patch.dict(current_app.config, config):
        field = MockField(u'THIS-ORCID-DOES-NOT-EXIST')

        with pytest.raises(StopValidation):
            ORCIDValidator(None, field)


@patch('inspirehep.modules.forms.validation_utils.orcid.MemberAPI')
def test_orcid_validator_accepts_everything_when_orcid_is_not_configured(mock_member_api):
    mock_orcid_api = MockOrcidAPI({'orcid-search-results': {'num-found': 0}})
    mock_member_api.return_value = mock_orcid_api

    config = {}

    with patch.dict(current_app.config, config, clear=True):
        field = MockField(u'THIS-ORCID-DOES-NOT-EXIST')

        assert ORCIDValidator(None, field) is None