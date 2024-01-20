import os, sys
import socket
import time


# TROUBLE SHOOTS VPN CONNECTION AND CONNECTS TO NORDVPN


def is_online() -> bool:
  '''
  Determine if the computer is online

  Returns:
    bool: 'True' if the computer is online
  '''
  try:
    # Try and create a connection to Google's DNS server
    socket.create_connection(("8.8.8.8", 53), timeout=5)
    return True
  except OSError:
    pass
  return False


def parallel_commands(commands: list) -> str:
  '''
  Joins commands together then returns the output

  Args:
    commands (list): The commands to be passed

  Returns:
    str: The return from the command
  '''
  separator = '&&' if os.name != 'nt' else '&'
  full_command = separator.join(commands)
  result = os.popen(full_command).read()
  return result


def connect_vpn() -> None:
  '''
  Connect to nordVPN
  '''
  # https://support.nordvpn.com/Connectivity/Linux/1325531132/Installing-and-using-NordVPN-on-Debian-Ubuntu-Raspberry-Pi-Elementary-OS-and-Linux-Mint.htm
  commands_list = [
    'cd "C:\Program Files\NordVPN\"',
    'NEXT_COMMAND'
  ]
  parallel_commands(commands_list)
  
connect_vpn()import os, sys
import socket
import time


def is_online() -> bool:
  '''
  Determine if the computer is online

  Returns:
    bool: 'True' if the computer is online
  '''
  try:
    # Try and create a connection to Google's DNS server
    socket.create_connection(("8.8.8.8", 53), timeout=5)
    return True
  except OSError:
    pass
  return False


def parallel_commands(commands: list) -> str:
  '''
  Joins commands together then returns the output

  Args:
    commands (list): The commands to be passed

  Returns:
    str: The return from the command
  '''
  separator = '&&' if os.name != 'nt' else '&'
  full_command = separator.join(commands)
  result = os.popen(full_command).read()
  return result


def connect_vpn() -> None:
  '''
  Connect to nordVPN
  '''
  # https://support.nordvpn.com/Connectivity/Linux/1325531132/Installing-and-using-NordVPN-on-Debian-Ubuntu-Raspberry-Pi-Elementary-OS-and-Linux-Mint.htm
  commands_list = [
    'cd "C:\Program Files\NordVPN\"',
    'NEXT_COMMAND'
  ]
  parallel_commands(commands_list)
  
connect_vpn()