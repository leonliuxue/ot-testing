import json

import pytest
import requests

from api.utils import test_cases_all, is_skip
from api.utils import url


@pytest.mark.skipif(is_skip is True, reason='')
def test_login():
  test_cases = test_cases_all['admin']

  for key, test_case in test_cases.items():
    res = requests.post(url, data=json.dumps(test_case['message']))
    assert res is not None
    assert test_case['expected']['status_code'] == res.status_code

    if res.status_code == 200:
      assert test_case['expected']['text'][0] == json.loads(res.text)[0]
      assert test_case['expected']['text'][1] == json.loads(res.text)[1]

      if json.loads(res.text)[1] == 'ok':
        assert json.loads(res.text)[2]['sessionToken'] != ''
