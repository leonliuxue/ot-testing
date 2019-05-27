import unittest

# from globals import CASE,host,row_num
from globals import get_test_cases
from api_tester import ApiTester

session_token = None
test_cases = get_test_cases()

def isNaN(param):
  return param != param


class testRestApi(unittest.TestCase):
  # def __init__(self, t):
    # super().__init__()


  def testRestApi(self):
    for index, row in test_cases.iterrows():
      if not isNaN(row['message']):
        if index == 0:
          api = ApiTester(row['method'], row['url'], row['message'])
          apicode = api.get_code()
          res = api.get_json()
          if res[1] == 'ok':
            session_token = res[2]['sessionToken']
        else:
          api = ApiTester(row['method'], row['url'], row['message'], session_token)
          apicode = api.get_code()
          res = api.get_json()

        if apicode == row['status_code']:
          print('{}、{}:测试成功。json数据为:{}'.format(index, row['action'], res))

        else:
          print('{}、{}:测试失败'.format(index, row['action']))


if __name__ == '__main__':
  unittest.main(verbosity=2)
