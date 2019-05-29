import json

import pytest
import requests

from api.utils import is_skip, url, session_token
from api.utils import test_cases_all


@pytest.mark.skipif(is_skip is True, reason='')
def test_position():
  test_cases = test_cases_all['position']

  for key, test_case in test_cases.items():
    _res = requests.post(url,
                         data=json.dumps(test_case['message']),
                         headers={
                           'session-token': session_token
                         })
    assert _res is not None
    assert test_case['expected']['status_code'] == _res.status_code

    if _res.status_code == 200:
      text = json.loads(_res.text)
      # TODO: add test
      # assert test_case['expected']['total_no'] == len(text)


def test_target():
  test_cases = test_cases_all['target']

  for key, test_case in test_cases.items():
    _res = requests.post(url,
                         data=json.dumps(test_case['message']),
                         headers={
                           'session-token': session_token
                         })
    assert _res is not None
    assert test_case['expected']['status_code'] == _res.status_code

    if _res.status_code == 200:
      text = json.loads(_res.text)
      # TODO: add test
      # assert test_case['expected']['total_no'] == len(text)


@pytest.mark.skipif(is_skip is True, reason='')
def test_bod():
  test_cases = test_cases_all['bod']

  for key, test_case in test_cases.items():
    _res = requests.post(url,
                         data=json.dumps(test_case['message']),
                         headers={
                           'session-token': session_token
                         })
    assert _res is not None
    assert test_case['expected']['status_code'] == _res.status_code

    if _res.status_code == 200:
      text = json.loads(_res.text)
      # TODO: add test
      # assert test_case['expected']['total_no'] == len(text)
