import os, sys
import requests
import time
import socket


class Globals:
  host_name = socket.gethostname()
  ip = socket.gethostbyname(host_name)
  def getIP():
    try:
      response = requests.get('https://api.ipify.org?format=json')
      data = response.json()
      public_ip = data.get('ip')
      return public_ip
    except requests.RequestException as e:
      print(f"Error: {e}")
      return None


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
  result = os.popen(f'powershell {full_command}').read()
  if result != '':
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
      print('Connected to the closest server...')

    elif connect_opt == 'dedicated' or connect_opt == 'personal':
      commands_list = [cd_cmd, f'./{exe_name} -c -g {connect_options[1]}']
      parallel_commands(commands_list)
      print(f'Connected to the most optimal "{connect_options[1]}" server...')

    elif connect_opt == 'dual' or connect_opt == 'double':
      commands_list = [cd_cmd, f'./{exe_name} -c -g {connect_options[2]}']
      parallel_commands(commands_list)
      print(f'Connected to the closest "{connect_options[2]}" server...')

    elif connect_opt == 'secure' or connect_opt == 'obfuscated':
      commands_list = [cd_cmd, f'./{exe_name} -c -g {connect_options[3]}']
      parallel_commands(commands_list)
      print(f'Connected to the closest "{connect_options[3]}" server...')

    elif connect_opt == 'onion' or connect_opt == 'tor':
      commands_list = [cd_cmd, f'./{exe_name} -c -g {connect_options[4]}']
      parallel_commands(commands_list)
      print(f'Connected to the closest "{connect_options[4]}" server...')

    elif connect_opt == 'p2p' or connect_opt == 'peer':
      commands_list = [cd_cmd, f'./{exe_name} -c -g {connect_options[5]}']
      parallel_commands(commands_list)
      print(f'Connected to the closest "{connect_options[5]}" server...')


def arg_handler() -> None:
  try:
    if __file__.endswith('.py'):
      arg1 = sys.argv[1].lower()
      arg2 = sys.argv[2].lower()
    if __file__.endswith('.exe'):
      arg1 = sys.argv[0].lower()
      arg2 = sys.argv[2].lower()
  except Exception:
    pass

  connected_to_vpn = 'VPN OFF'

  match arg1:

    case '-c':
      connected_to_vpn = 'VPN ON'
      if 'arg2' not in locals():
        arg2 = 'default'
      connect_vpn(arg2)
    
    case '-d':
      connected_to_vpn = 'VPN OFF'
      print(f'Disconnecting from VPN...')
      disconnect_vpn()
    
    case '-dr' | '-d&r':
      disconnect_and_reconnect()
      print(f'VPN has been reset...')
    
    case '-s':
      status = 'ONLINE' if is_online() else 'OFFLINE'
      print(
        f'********************************** \
        \n >  {socket.gethostname()} is {status} \
        \n >  Assumed Status: {connected_to_vpn} \
        \n >  IP Address: {Globals.getIP()} \
        \n**********************************'
      )


if __name__ == '__main__':
  arg_handler()
