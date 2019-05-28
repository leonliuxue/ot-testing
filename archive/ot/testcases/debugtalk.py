import hashlib
import hmac
import random
import string

def parse_token():
  print('parse_token')
  # print(res)
  # return res
  # if res[1] == 'ok':
  #   session_token = res[2]['sessionToken']
  #   return session_token
  # else:
  #   return




SECRET_KEY = "DebugTalk"

def gen_random_string(str_len):
    print(str_len)
    random_char_list = []
    for _ in range(str_len):
        random_char = random.choice(string.ascii_letters + string.digits)
        random_char_list.append(random_char)

    random_string = ''.join(random_char_list)
    return random_string

def get_sign(*args):
    content = ''.join(args).encode('ascii')
    sign_key = SECRET_KEY.encode('ascii')
    sign = hmac.new(sign_key, content, hashlib.sha1).hexdigest()
    return sign

def gen_user_id():
    return "test"