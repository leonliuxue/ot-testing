import json
import unittest
import requests


class TestApiMethods(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.url = 'http://103.224.167.234/api/'

    with open('test_cases.json') as f:
      cls.test_cases = json.load(f)

  def test_login(self):
    login_test_cases = self.test_cases['test_login']
    for key, test_case in login_test_cases.items():
      res = requests.post(self.url, data=json.dumps(test_case['message']))
      self.assertIsNotNone(res)
      self.assertEqual(res.status_code, test_case['expected']['status_code'])

      if res.status_code == 200:
        self.assertEqual(json.loads(res.text)[0], test_case['expected']['text'][0])
        self.assertEqual(json.loads(res.text)[1], test_case['expected']['text'][1])

        if json.loads(res.text)[1] == 'ok':
          self.assertIsNot(json.loads(res.text)[2]['sessionToken'], '')


if __name__ == '__main__':
  unittest.main()