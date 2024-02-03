import os, sys
from typing import *


class StoreData():

  data_file: str = 'data.db'

  def store(key: str | int, value: str | int) -> None:
    if StoreData.fetch_value(key) != None:
      return None  # Entry already exists
    with open(StoreData.data_file, 'a+') as db:
      if isinstance(key, str):
        key: str = f'"{key}"'
      if isinstance(value, str):
        value: str = f'"{value}"'

      db.write(f'{key}: {value}\n')
  
  def fetch_value(key: str | int) -> str | int | None:
    with open(StoreData.data_file, 'r') as db:
      content: str = db.read()
    key_str: str = str(key)
    key_idx: int = content.find(key_str)

    if key_idx == -1:
      return None  # Key not found

    key_end_idx: int = key_idx + len(key_str)
    value_start_idx: int = content.find(':', key_end_idx) + 1
    value_end_idx: int = content.find('\n', value_start_idx)
    value: str = content[value_start_idx:value_end_idx].strip()
    return value.replace('"', '')
  
  def fetch_key(value: str | int) -> str | int | None:
    with open(StoreData.data_file, 'r') as db:
      content: str = db.read()

    # key_value_pairs = [pair.split(':') for pair in content.split('\n')]
    key_value_pairs = []
    for pair in content.split('\n'):
      key_value_pairs.append(pair.split(':'))

    for pair in key_value_pairs:
      if len(pair) == 2:
        key, val = pair
        if val.strip() == str(value):
          return key.strip().strip('"')
    return None

  def get_keys() -> List[str]:
    with open(StoreData.data_file, 'r') as db:
      lines = db.readlines()
    keys: List[str] = []

    for line in lines:
      key_value = line.strip().split(':')
      if len(key_value) == 2:
        key = key_value[0].strip()
        if key.startswith('"') and key.endswith('"'):
          key = key[1:-1]
        keys.append(key)
    return keys
    
    
print(StoreData.fetch_key('69'))