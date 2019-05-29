import json

import pytest
import requests

from api.utils import is_skip, url, session_token
from api.utils import test_cases_all


# @pytest.mark.skipif(is_skip is True, reason='')
def test_securities():
  test_cases = test_cases_all['securities']

  for key, test_case in test_cases.items():
    res = requests.post(url,
                        data=json.dumps(test_case['message']),
                        headers={
                          'session-token': session_token
                        })
    assert res is not None
    assert test_case['expected']['status_code'] == res.status_code

    if res.status_code == 200:
      text = json.loads(res.text)
      assert test_case['expected']['total_securities'] == len(text)


@pytest.mark.skipif(is_skip is True, reason='')
def test_opentick():
  test_cases = test_cases_all['opentick']

  for key, test_case in test_cases.items():
    res = requests.post(url,
                        data=json.dumps(test_case['message']),
                        headers={
                          'session-token': session_token
                        })
    assert res is not None
    assert test_case['expected']['status_code'] == res.status_code

    if res.status_code == 200:
      text = json.loads(res.text)
      assert test_case['expected']['total_no'] == len(text)
