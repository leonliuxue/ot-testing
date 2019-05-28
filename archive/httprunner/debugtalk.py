def parse_token(res=''):
  print('parse_token')
  # print(res)
  if res[1] == 'ok':
    session_token = res[2]['sessionToken']
    return session_token
  else:
    return