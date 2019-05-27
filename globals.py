
import pandas as pd

file_path = "API_TEST.xlsx"
sheet_name_valid_cases = 'valid_cases'

def parse_message(message):
  if not message != message:
    message = message[1:-1].replace("'", "").split(',')
  return message


def get_test_cases():
  case_df = pd.read_excel(file_path, sheet_name=sheet_name_valid_cases)

  case_df['message'] = case_df['message'].apply(parse_message)

  return case_df
