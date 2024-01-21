import os, sys
import requests
import time


def is_online() -> bool:
  '''
  Determine if the computer is online

  Returns:
    bool: 'True' if the computer is online
  '''
  url = 'https://example.com/'
  timeout = 5
  try:
    requests.get(url, timeout=timeout)
    return True
  except (requests.ConnectionError, requests.Timeout) as exception:
    return False


def parallel_commands(commands: list) -> str:
  '''
  Joins commands together then returns the output

  Args:
    commands (list): The commands to be passed

  Returns:
    str: The return from the command
  '''
  separator = '&&' if os.name != 'nt' else ';'
  full_command = separator.join(commands)
  print(f'powershell {full_command}')
  result = os.popen(f'powershell {full_command}').read()
  print(result)
  return result


def disconnect_vpn() -> None:
  '''
  Disconnects VPN
  '''
  exe_name = 'NordVPN.exe'
  commands_list = [
    'cd \'C:\\Program Files\\NordVPN\'', f'./{exe_name} -d'
  ]
  parallel_commands(commands_list)


def disconnect_and_reconnect(trouble_shoot: bool = False) -> None:
  '''
  Disconnects then reconnects VPN
  '''
  if trouble_shoot:
    time.sleep(2)
    if not is_online():
      disconnect_vpn()
      time.sleep(1)
      connect_vpn()
  else:
    disconnect_vpn()
    connect_vpn()


def connect_vpn(connect_opt: str = 'default') -> None:
  '''
  Connect to nordVPN
  '''
  # https://support.nordvpn.com/Connectivity/Linux/1325531132/Installing-and-using-NordVPN-on-Debian-Ubuntu-Raspberry-Pi-Elementary-OS-and-Linux-Mint.htm

  connect_opt = connect_opt.lower()
  if 'win' in sys.platform:
    exe_name = 'NordVPN.exe'
    connect_options = {
      1: "Dedicated IP",
      2: "Double VPN",
      3: "Obfuscated servers",
      4: "Onion Over VPN",
      5: "P2P",
    }
    cd_cmd = 'cd \'C:\\Program Files\\NordVPN\''

    if connect_opt == 'default':
      commands_list = [cd_cmd, f'./{exe_name} -c']
      parallel_commands(commands_list)
      disconnect_and_reconnect(True)

    elif connect_opt == 'dedicated' or connect_opt == 'personal':
      commands_list = [cd_cmd, f'./{exe_name} -c -g {connect_options[0]}']
      parallel_commands(commands_list)
      disconnect_and_reconnect(True)

    elif connect_opt == 'dual' or connect_opt == 'double':
      commands_list = [cd_cmd, f'./{exe_name} -c -g {connect_options[1]}']
      parallel_commands(commands_list)
      disconnect_and_reconnect(True)

    elif connect_opt == 'secure' or connect_opt == 'obfuscated':
      commands_list = [cd_cmd, f'./{exe_name} -c -g {connect_options[2]}']
      parallel_commands(commands_list)
      disconnect_and_reconnect(True)

    elif connect_opt == 'onion' or connect_opt == 'tor':
      commands_list = [cd_cmd, f'./{exe_name} -c -g {connect_options[4]}']
      parallel_commands(commands_list)
      disconnect_and_reconnect(True)

    elif connect_opt == 'p2p' or connect_opt == 'peer':
      commands_list = [cd_cmd, f'./{exe_name} -c -g {connect_options[5]}']
      parallel_commands(commands_list)
      disconnect_and_reconnect(True)


if __name__ == '__main__':
  try:
    if __file__.endswith('.py'):
      arg1 = sys.argv[1].lower()
      arg2 = sys.argv[2].lower()
    if __file__.endswith('.exe'):
      arg1 = sys.argv[0].lower()
      arg2 = sys.argv[2].lower()
  except Exception:
    pass

  if arg1 == 'disconnect':
    disconnect_vpn()
  connect_vpn(arg1)
