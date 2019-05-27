import unittest

# from globals import CASE,host,row_num
from globals import getCaseTests
from manageapi import testApi

test_cases = getCaseTests()
session_token = None


def isNaN(param):
    return param != param

for index, row in test_cases.iterrows():
    # for i in range(0, row_num - 1):
    if not isNaN(row['message']):
        if index == 0:
            api = testApi(row['method'], row['url'], row['message'])
            apicode = api.getCode()
            res = api.getJson()
            if res[1] == 'ok':
                session_token = res[2]['sessionToken']
        else:
            api = testApi(row['method'], row['url'], row['message'], session_token)
            apicode = api.getCode()
            res = api.getJson()


        if apicode == row['status_code']:
            print('{}、{}:测试成功。json数据为:{}'.format(index, row['action'], res))

        else:
            print('{}、{}:测试失败'.format(index, row['action']))


if __name__ == '__main__':
    unittest.main(verbosity=2)