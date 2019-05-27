import json

import requests

class testApi(object):
    def __init__(self, method, url, data, session_token = None):
        self.method = method
        self.url = url
        self.data = data
        self.session_token = session_token

    @property
    def testApi(self):
        # 根据不同的访问方式来访问接口
        try:
            if self.method == 'post':
                if self.data == "":
                    print("No data post")
                else:
                    if self.session_token is not None:
                        result = requests.post(
                            self.url,
                            data=json.dumps(self.data).encode('utf-8'),
                            headers={
                                'session-token': self.session_token
                            }
                        )
                    else:
                        result = requests.post(self.url, data=json.dumps(self.data).encode('utf-8'))

            elif self.method == 'get':
                if self.data == "":
                    result = requests.get(self.url)
                else:
                    result = requests.get(self.url, params=self.data)

            return result
        except:
            print('失败')

    def getCode(self):
        # 获取访问接口的状态码
        code = self.testApi.status_code
        return code

    def getJson(self):
        # 获取返回信息的json数据
        json_data = self.testApi.json()
        return json_data