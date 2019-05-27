import math

from manageexcel import readExcel
import pandas as pd

# CASE_NUMBER = 0  # 用例编号
# CASE_NAME = 1  # 用例名称
# CASE_METHOD = 3  # 请求类型
# CASE_URL = 2  # 请求地址
# CASE_DATA = 4  # 用例数据
# CASE_STATUS = 5  # 用例状态
# CASE_KEY = 6  # 验证关键字

file_path = "API_TEST.xlsx"
sheet_name_valid_cases = 'valid_cases'


# host = "http://localhost:5000"

# row_num = readExcel(file_path).getRows
#
#
# class CASE:
#   number = readExcel(file_path).getName(CASE_NUMBER)
#   name = readExcel(file_path).getName(CASE_NAME)
#   method = readExcel(file_path).getName(CASE_METHOD)
#   url = readExcel(file_path).getName(CASE_URL)
#   data = readExcel(file_path).getName(CASE_DATA)
#   status = readExcel(file_path).getName(CASE_STATUS)
#   key = readExcel(file_path).getName(CASE_KEY)
#
#   case_df = pd.read_excel(file_path,  sheet_name=sheet_name_valid_cases)
#
#   print()
#
#   for index, row in case_df.iterrows():
#     if row['message'] is not None:
#       print(row['message'])
#       l = row['message'].split(',')
#       case_df.loc[index, 'message'] = l
#       print(row['message'])
#
#   print()

def func(message):
  if not message != message:
    message = message[1:-1].replace("'", "").split(',')
  return message


def getCaseTests():
  case_df = pd.read_excel(file_path, sheet_name=sheet_name_valid_cases)

  case_df['message'] = case_df['message'].apply(func)

  return case_df
