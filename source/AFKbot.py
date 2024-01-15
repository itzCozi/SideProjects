import os, sys
import discord
from discord.ext import commands
import mss
import cv2
import win32api
import ctypes
import time

from typing import *
from win32con import *
from ctypes import wintypes
from win32api import STD_INPUT_HANDLE
from win32console import (
  GetStdHandle, KEY_EVENT, ENABLE_ECHO_INPUT,
  ENABLE_LINE_INPUT, ENABLE_PROCESSED_INPUT
)


# From my py-keyboard-class repo
class Keyboard:
  """
  A class for receiving and sending keystrokes/mouse inputs

  --------------------------------------------------
  |          function         description          |
  |------------------------------------------------|
  | class  moveCursor: Moves cursor to a position  |
  | class  GetKeystroke: A key poller wrapper      |
  | func   mouseScroll: Bare-bones mouse scroller  |
  | func   getKeyState: Returns given key's state  |
  | func   scrollMouse: Scrolls the mouse wheel    |
  | func   pressMouse: Sends a VK input to mouse   |
  | func   releaseMouse: Halt VK signal            |
  | func   pressKey: Presses given key hex code    |
  | func   releaseKey: Stop given VK input         |
  | func   pressAndReleaseKey: N/A                 |
  | func   pressAndReleaseMouse: N/A               |
  | func   keyboardWrite: Sends vk inputs          |
  --------------------------------------------------
  """

  class _Vars:
    """
    Keyboard class for static variables.
    """

    @staticmethod
    def error(
      error_type: str,
      var: str = None,
      type: str = None,
      runtime_error: str = None
    ) -> None:
      """
      Display error messages based on the type of error encountered.
      """
      if error_type == 'p':
        print(f'PARAMETER: Given variable {var} is not a {type}.')
      elif error_type == 'r':
        print(f'RUNTIME: {runtime_error.capitalize()}.')
      elif error_type == 'u':
        print('UNKNOWN: An unknown error was encountered.')
      return None

    exit_code: str = 'null'
    INPUT_MOUSE: int = 0
    INPUT_KEYBOARD: int = 1
    MAPVK_VK_TO_VSC: int = 0
    KEYEVENTF_KEYUP: int = 0x0002
    KEYEVENTF_UNICODE: int = 0x0004
    KEYEVENTF_SCANCODE: int = 0x0008
    KEYEVENTF_EXTENDEDKEY: int = 0x0001
    user32: ctypes.WinDLL = ctypes.WinDLL('user32', use_last_error=True)

  # Reference: https://msdn.microsoft.com/en-us/library/dd375731
  # Each key value is 4 chars long and formatted in hexadecimal
  vk_codes: dict = {
    # --- Mouse ---
    "left_mouse":           0x01,
    "right_mouse":          0x02,
    "middle_mouse":         0x04,
    "mouse_button1":        0x05,
    "mouse_button2":        0x06,
    # --- Control Keys ---
    "win":                  0x5B,  # Left Windows key
    "select":               0x29,
    "pg_down":              0x21,
    "pg_up":                0x22,
    "end":                  0x23,
    "home":                 0x24,
    "insert":               0x2D,
    "delete":               0x2E,
    "back":                 0x08,
    "enter":                0x0D,
    "shift":                0x10,
    "ctrl":                 0x11,
    "alt":                  0x12,
    "caps":                 0x14,
    "escape":               0x1B,
    "space":                0x20,
    "tab":                  0x09,
    "sleep":                0x5F,
    "zoom":                 0xFB,
    "num_lock":             0x90,
    "scroll_lock":          0x91,
    # --- OEM Specific ---
    "plus":                 0xBB,
    "comma":                0xBC,
    "minus":                0xBD,
    "period":               0xBE,
    # --- Media ---
    "vol_mute":             0xAD,
    "vol_down":             0xAE,
    "vol_up":               0xAF,
    "next":                 0xB0,
    "prev":                 0xB1,
    "pause":                0xB2,
    "play":                 0xB3,
    # --- Arrow Keys ---
    "left":                 0x25,
    "up":                   0x26,
    "right":                0x27,
    "down":                 0x28,
    # --- Function Keys ---
    "f1":                   0x70,
    "f2":                   0x71,
    "f3":                   0x72,
    "f4":                   0x73,
    "f5":                   0x74,
    "f6":                   0x75,
    "f7":                   0x76,
    "f8":                   0x77,
    "f9":                   0x78,
    "f10":                  0x79,
    "f11":                  0x7A,
    "f12":                  0x7B,
    "f13":                  0x7C,
    "f14":                  0x7D,
    "f15":                  0x7E,
    # --- Keypad ---
    "pad_0":                0x60,
    "pad_1":                0x61,
    "pad_2":                0x62,
    "pad_3":                0x63,
    "pad_4":                0x64,
    "pad_5":                0x65,
    "pad_6":                0x66,
    "pad_7":                0x67,
    "pad_8":                0x68,
    "pad_9":                0x69,
    # --- Symbols ---
    "multiply":             0x6A,
    "add":                  0x6B,
    "separator":            0x6C,
    "subtract":             0x6D,
    "decimal":              0x6E,
    "divide":               0x6F,
    # --- Alphanumerical ---
    "0":                    0x30,
    "1":                    0x31,
    "2":                    0x32,
    "3":                    0x33,
    "4":                    0x34,
    "5":                    0x35,
    "6":                    0x36,
    "7":                    0x37,
    "8":                    0x38,
    "9":                    0x39,
    "a":                    0x41,
    "b":                    0x42,
    "c":                    0x43,
    "d":                    0x44,
    "e":                    0x45,
    "f":                    0x46,
    "g":                    0x47,
    "h":                    0x48,
    "i":                    0x49,
    "j":                    0x4A,
    "k":                    0x4B,
    "l":                    0x4C,
    "m":                    0x4D,
    "n":                    0x4E,
    "o":                    0x4F,
    "p":                    0x50,
    "q":                    0x51,
    "r":                    0x52,
    "s":                    0x53,
    "t":                    0x54,
    "u":                    0x55,
    "v":                    0x56,
    "w":                    0x57,
    "x":                    0x58,
    "y":                    0x59,
    "z":                    0x5A,
    "=":                    0x6B,
    " ":                    0x20,
    ".":                    0xBE,
    ",":                    0xBC,
    "-":                    0x6D,
    "`":                    0xC0,
    "/":                    0xBF,
    ";":                    0xBA,
    "[":                    0xDB,
    "]":                    0xDD,
    "_":                    0x6D,   # Shift
    "|":                    0xDC,   # Shift
    "~":                    0xC0,   # Shift
    "?":                    0xBF,   # Shift
    ":":                    0xBA,   # Shift
    "<":                    0xBC,   # Shift
    ">":                    0xBE,   # Shift
    "{":                    0xDB,   # Shift
    "}":                    0xDD,   # Shift
    "!":                    0x31,   # Shift
    "@":                    0x32,   # Shift
    "#":                    0x33,   # Shift
    "$":                    0x34,   # Shift
    "%":                    0x35,   # Shift
    "^":                    0x36,   # Shift
    "&":                    0x37,   # Shift
    "*":                    0x38,   # Shift
    "(":                    0x39,   # Shift
    ")":                    0x30,   # Shift
    "+":                    0x6B,   # Shift
    "\"":                   0xDE,   # Shift
    "\'":                   0xDE,
    "\\":                   0xDC,
    "\n":                   0x0D
  }

  # C struct declarations, recently added type hinting
  wintypes.ULONG_PTR: type[wintypes.WPARAM] = wintypes.WPARAM
  global MOUSEINPUT, KEYBDINPUT

  class MOUSEINPUT(ctypes.Structure):
    _fields_: tuple[
      tuple[Literal['dx'], wintypes.LONG],                  # A
      tuple[Literal['dy'], wintypes.LONG],                  # B
      tuple[Literal['mouseData'], wintypes.DWORD],          # C
      tuple[Literal['dwFlags'], wintypes.DWORD],            # D
      tuple[Literal['time'], wintypes.DWORD],               # E
      tuple[Literal['dwExtraInfo'], type[wintypes.WPARAM]]  # F
    ] = (
      ('dx', wintypes.LONG),                                # A
      ('dy', wintypes.LONG),                                # B
      ('mouseData', wintypes.DWORD),                        # C
      ('dwFlags', wintypes.DWORD),                          # D
      ('time', wintypes.DWORD),                             # E
      ('dwExtraInfo', wintypes.ULONG_PTR)                   # F
    )

  class KEYBDINPUT(ctypes.Structure):
    _fields_: tuple[
      tuple[Literal['wVk'], wintypes.WORD],                 # A
      tuple[Literal['wScan'], wintypes.WORD],               # B
      tuple[Literal['dwFlags'], wintypes.DWORD],            # C
      tuple[Literal['time'], wintypes.DWORD],               # D
      tuple[Literal['dwExtraInfo'], type[wintypes.WPARAM]]  # E
    ] = (
      ('wVk', wintypes.WORD),                               # A
      ('wScan', wintypes.WORD),                             # B
      ('dwFlags', wintypes.DWORD),                          # C
      ('time', wintypes.DWORD),                             # D
      ('dwExtraInfo', wintypes.ULONG_PTR)                   # E
    )

    def __init__(
      self: Self,
      *args: tuple[Any, ...],
      **kwds: dict[str, Any]
    ) -> None:
      # *args & **kwds are confusing asf: https://youtu.be/4jBJhCaNrWU?si=0zZQqGuMaR5ulLNb
      super(KEYBDINPUT, self).__init__(*args, **kwds)
      if not self.dwFlags & Keyboard._Vars.KEYEVENTF_UNICODE:
        self.wScan: Any = Keyboard._Vars.user32.MapVirtualKeyExW(
          self.wVk, Keyboard._Vars.MAPVK_VK_TO_VSC, 0
        )

  class INPUT(ctypes.Structure):

    class _INPUT(ctypes.Union):
      _fields_: tuple[
        tuple[Literal['ki'], type[KEYBDINPUT]],
        tuple[Literal['mi'], type[MOUSEINPUT]]
      ] = (('ki', KEYBDINPUT), ('mi', MOUSEINPUT))

    _anonymous_: tuple[Literal['_input']] = ('_input',)
    _fields_: tuple[
      tuple[Literal['type'], wintypes.DWORD],
      tuple[Literal['_input'], type[_INPUT]]
    ] = (('type', wintypes.DWORD), ('_input', _INPUT))

  LPINPUT: Any = ctypes.POINTER(INPUT)

  # Helpers / Bare-bones implementation

  @staticmethod
  def _checkCount(result: Any, func: Any, args: Any) -> Any:
    if result == 0:
      raise ctypes.WinError(ctypes.get_last_error())
    return args

  @staticmethod
  def _lookup(key: Any) -> int | bool:
    if key in Keyboard.vk_codes:
      return Keyboard.vk_codes.get(key)
    else:
      return False

  @staticmethod
  def mouseScroll(axis: str, dist: int, x: int = 0, y: int = 0) -> None | bool:
    if axis == 'v' or axis == 'vertical':
      win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, dist, 0)
    elif axis == 'h' or axis == 'horizontal':
      win32api.mouse_event(MOUSEEVENTF_HWHEEL, x, y, dist, 0)
    else:
      return False

  class ManipulateMouse:
    """
    A simple class to control the mouse cursor

    Functions:
      getPosition(): Returns a tuple with the cursor's current position
      setPosition(x, y): Moves the cursor to the given x and y coordinates
    """

    @staticmethod
    def getPosition() -> tuple:
      """
      Retrieve the current position of the mouse cursor.
      """
      # Define the POINT structure to store cursor position
      class POINT(ctypes.Structure):
        _fields_: list = [("x", ctypes.c_long), ("y", ctypes.c_long)]

      point: POINT = POINT()
      ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
      return (point.x, point.y)

    @staticmethod
    def setPosition(x: int, y: int) -> None:
      """
      Set the position of the mouse cursor to the given coordinates.
      """
      ctypes.windll.user32.SetCursorPos(x, y)

  class GetKeystroke:
    """
    A wrapper that returns the key pressed

    Example:
      with KeyPoller() as keyPoller:
        while True:
          key: str = keyPoller.poll()
          if key is not None:
            if key == "c": break
            print(key)

    Returns:
      str: The key pressed after calling the class
    """

    def __init__(self: Self) -> None:
      """
      Initialize the class and config.
      """
      self.cur_event_len: None | int = None

    def __enter__(self: Self) -> Any:
      """
      Enter context manager to initialize resources.
      """
      self.readHandle: Any = GetStdHandle(STD_INPUT_HANDLE)
      self.readHandle.SetConsoleMode(
        ENABLE_LINE_INPUT | ENABLE_ECHO_INPUT | ENABLE_PROCESSED_INPUT
      )  # Set terminal flags/mode

      self.cur_event_len: int = 0
      self.cur_keys_len: int = 0
      self.captured_chars: list = []

      return self

    def __exit__(self: Self, type: Any, value: Any, traceback: Any) -> None:
      """
      Exit context manager to release resources.
      """
      pass

    # Main function
    def poll(self: Self) -> str | None:
      """
      Poll and return the last pressed key from the input stream.

      Returns:
        str | None: The last pressed key, or None if no key is pressed.
      """
      if not len(self.captured_chars) == 0:
        return self.captured_chars.pop(0)
      events_peek: tuple = self.readHandle.PeekConsoleInput(10000)

      if len(events_peek) == 0:
        return None

      if not len(events_peek) == self.cur_event_len:

        for cur_event in events_peek[self.cur_event_len:]:
          if cur_event.EventType == KEY_EVENT:
            if ord(cur_event.Char) == 0 or not cur_event.KeyDown:
              pass
            else:
              cur_char: str = str(cur_event.Char)
              self.captured_chars.append(cur_char)

        self.cur_event_len: int = len(events_peek)
      if not len(self.captured_chars) == 0:
        return self.captured_chars.pop()  # Return the last item in the list

  _Vars.user32.SendInput.errcheck: Any = _checkCount
  _Vars.user32.SendInput.argtypes: Any = (
    wintypes.UINT,  # nInputs
    LPINPUT,  # pInputs
    ctypes.c_int  # cbSize
  )

  # Functions (most people will only use these)

  @staticmethod
  def getKeyState(key_code: str | int) -> bool:
    """
    Returns the given key's current state

    Args:
      key_code (str | int): The key to be checked for state

    Returns:
      bool: 'False' if the key is not pressed and 'True' if it is
    """
    if not isinstance(key_code, str | int):
      Keyboard._Vars.error(error_type='p', var='key_code', type='integer or string')
      return Keyboard._Vars.exit_code

    if Keyboard._lookup(key_code) is not False:
      key_code: int = Keyboard._lookup(key_code)
    elif key_code not in Keyboard.vk_codes and key_code not in Keyboard.vk_codes.values():
      Keyboard._Vars.error(error_type='r', runtime_error='given key code is not valid')
      return Keyboard._Vars.exit_code

    integer_state: int = Keyboard._Vars.user32.GetKeyState(key_code)
    if integer_state == 1:
      key_state: bool = True
    else:
      key_state: bool = False

    if 'key_state' in locals():
      return key_state
    else:
      Keyboard._Vars.error(
        error_type='r', runtime_error='user32 returned a non "1" or "0" value'
      )
      return Keyboard._Vars.exit_code

  @staticmethod
  def locateCursor() -> Tuple[int, int]:
    """
    Return a tuple of the current X & Y coordinates of the mouse

    Returns:
      tuple[int, int]: The current X and Y coordinates EX: (350, 940)
    """

    # The ManipulateMouse class has a function for this
    return Keyboard.ManipulateMouse.getPosition()

  @staticmethod
  def moveCursor(x: int, y: int) -> None:
    """
    Moves the cursor to a specific coordinate on the screen.

    Args:
      x (int): The x-coordinate to be sent to user32
      y (int): The y-coordinate to be sent to user32
    """
    if not isinstance(x, int):
      Keyboard._Vars.error(error_type='p', var='x', type='integer')
      return Keyboard._Vars.exit_code
    if not isinstance(y, int):
      Keyboard._Vars.error(error_type='p', var='y', type='integer')
      return Keyboard._Vars.exit_code

    # The ManipulateMouse class also has a function for this
    Keyboard.ManipulateMouse.setPosition(x, y)

  @staticmethod
  def scrollMouse(direction: str, amount: int, dx: int = 0, dy: int = 0) -> None:
    """
    Scrolls mouse up, down, right and left by a certain amount

    Args:
      direction (str): The way to scroll, valid inputs: (
        up, down, right, left
      )
      amount (int): How much to scroll has to be at least 1
      dx (int, optional): The mouse's position on the x-axis
      dy (int, optional): The mouse's position on the x-axis
    """
    if not isinstance(direction, str):
      Keyboard._Vars.error(error_type='p', var='direction', type='string')
      return Keyboard._Vars.exit_code
    if not isinstance(amount, int):
      Keyboard._Vars.error(error_type='p', var='amount', type='integer')
      return Keyboard._Vars.exit_code
    if not isinstance(dx, int):
      Keyboard._Vars.error(error_type='p', var='dx', type='integer')
      return Keyboard._Vars.exit_code
    if not isinstance(dy, int):
      Keyboard._Vars.error(error_type='p', var='dy', type='integer')
      return Keyboard._Vars.exit_code

    direction_list: list = ['up', 'down', 'left', 'right']
    if direction not in direction_list:
      Keyboard._Vars.error(error_type='r', runtime_error='given direction is not valid')
      return Keyboard._Vars.exit_code
    if amount < 1:
      Keyboard._Vars.error(error_type='r', runtime_error='given amount is less than 1')
      return Keyboard._Vars.exit_code

    if direction == 'up':
      Keyboard.mouseScroll('vertical', amount, dx, dy)
    elif direction == 'down':
      Keyboard.mouseScroll('vertical', -amount, dx, dy)
    elif direction == 'right':
      Keyboard.mouseScroll('horizontal', amount, dx, dy)
    elif direction == 'left':
      Keyboard.mouseScroll('horizontal', -amount, dx, dy)

  @staticmethod
  def pressMouse(mouse_button: str | int) -> None:
    """
    Releases a mouse button

    Args:
      mouse_button (str | int): The button to press accepted: (
        left_mouse,
        right_mouse,
        middle_mouse,
        mouse_button1,
        mouse_button
      )
    """
    if not isinstance(mouse_button, str | int):
      Keyboard._Vars.error(error_type='p', var='mouse_button', type='integer or string')
      return Keyboard._Vars.exit_code

    mouse_list: list = [
      "left_mouse", 0x01, "right_mouse", 0x02, "middle_mouse", 0x04,
      "mouse_button1", 0x05, "mouse_button2", 0x06
    ]
    if mouse_button not in mouse_list and hex(mouse_button) not in mouse_list:
      Keyboard._Vars.error(error_type='r', runtime_error='given key code is not a mouse button')
      return Keyboard._Vars.exit_code

    if Keyboard._lookup(mouse_button) is not False:
      mouse_button: int = Keyboard._lookup(mouse_button)
    elif mouse_button not in Keyboard.vk_codes and mouse_button not in Keyboard.vk_codes.values():
      Keyboard._Vars.error(error_type='r', runtime_error='given key code is not valid')
      return Keyboard._Vars.exit_code

    x: Keyboard.INPUT = Keyboard.INPUT(
      type=Keyboard._Vars.INPUT_MOUSE,
      mi=MOUSEINPUT(
        wVk=mouse_button,
        dwFlags=Keyboard._Vars.KEYEVENTF_KEYUP
      )
    )
    Keyboard._Vars.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

  @staticmethod
  def releaseMouse(mouse_button: str | int) -> None:
    """
    Presses a mouse button

    Args:
      mouse_button (str | int): The button to press accepted: (
        left_mouse,
        right_mouse,
        middle_mouse,
        mouse_button1,
        mouse_button
      )
    """
    if not isinstance(mouse_button, str | int):
      Keyboard._Vars.error(error_type='p', var='mouse_button', type='integer or string')
      return Keyboard._Vars.exit_code

    mouse_list: list = [
      "left_mouse", 0x01, "right_mouse", 0x02, "middle_mouse", 0x04,
      "mouse_button1", 0x05, "mouse_button2", 0x06
    ]
    if mouse_button not in mouse_list and hex(mouse_button) not in mouse_list:
      Keyboard._Vars.error(
        error_type='r', runtime_error='given key code is not a mouse button'
      )
      return Keyboard._Vars.exit_code

    if Keyboard._lookup(mouse_button) is not False:
      mouse_button: int = Keyboard._lookup(mouse_button)
    elif mouse_button not in Keyboard.vk_codes and mouse_button not in Keyboard.vk_codes.values():
      Keyboard._Vars.error(error_type='r', runtime_error='given key code is not valid')
      return Keyboard._Vars.exit_code

    x: Keyboard.INPUT = Keyboard.INPUT(
      type=Keyboard._Vars.INPUT_MOUSE,
      mi=MOUSEINPUT(wVk=mouse_button)
    )
    Keyboard._Vars.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

  @staticmethod
  def pressKey(key_code: str | int) -> None:
    """
    Presses a keyboard key

    Args:
      key_code (str | int): All keys in vk_codes dict are valid
    """
    if not isinstance(key_code, str | int):
      Keyboard._Vars.error(error_type='p', var='key_code', type='integer or string')
      return Keyboard._Vars.exit_code

    if Keyboard._lookup(key_code) is not False:
      key_code: int = Keyboard._lookup(key_code)
    elif key_code not in Keyboard.vk_codes and key_code not in Keyboard.vk_codes.values():
      Keyboard._Vars.error(error_type='r', runtime_error='given key code is not valid')
      return Keyboard._Vars.exit_code

    x: Keyboard.INPUT = Keyboard.INPUT(
      type=Keyboard._Vars.INPUT_KEYBOARD,
      ki=KEYBDINPUT(wVk=key_code)
    )
    Keyboard._Vars.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

  @staticmethod
  def releaseKey(key_code: str | int) -> None:
    """
    Releases a keyboard key

    Args:
      key_code (str | int): All keys in vk_codes dict are valid
    """
    if not isinstance(key_code, str | int):
      Keyboard._Vars.error(error_type='p', var='key_code', type='integer or string')
      return Keyboard._Vars.exit_code

    if Keyboard._lookup(key_code) is not False:
      key_code: int = Keyboard._lookup(key_code)
    elif key_code not in Keyboard.vk_codes and key_code not in Keyboard.vk_codes.values():
      Keyboard._Vars.error(error_type='r', runtime_error='given key code is not valid')
      return Keyboard._Vars.exit_code

    x: Keyboard.INPUT = Keyboard.INPUT(
      type=Keyboard._Vars.INPUT_KEYBOARD,
      ki=KEYBDINPUT(
        wVk=key_code,
        dwFlags=Keyboard._Vars.KEYEVENTF_KEYUP
      )
    )
    Keyboard._Vars.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

  @staticmethod
  def pressAndReleaseKey(key_code: str | int) -> None:
    """
    Presses and releases a keyboard key sequentially

    Args:
      key_code (str | int): All keys in vk_codes dict are valid
    """
    if not isinstance(key_code, str | int):
      Keyboard._Vars.error(error_type='p', var='key_code', type='integer or string')
      return Keyboard._Vars.exit_code

    if Keyboard._lookup(key_code) is not False:
      key_code: int = Keyboard._lookup(key_code)
    elif key_code not in Keyboard.vk_codes and key_code not in Keyboard.vk_codes.values():
      Keyboard._Vars.error(error_type='r', runtime_error='given key code is not valid')
      return Keyboard._Vars.exit_code

    Keyboard.pressKey(key_code)
    Keyboard.releaseKey(key_code)

  @staticmethod
  def pressAndReleaseMouse(mouse_button: str | int) -> None:
    """
    Presses and releases a mouse button sequentially

    Args:
      mouse_button (str | int): The button to press accepted: (
        left_mouse,
        right_mouse,
        middle_mouse,
        mouse_button1,
        mouse_button
      )
    """
    if not isinstance(mouse_button, str | int):
      Keyboard._Vars.error(error_type='p', var='mouse_button', type='integer or string')
      return Keyboard._Vars.exit_code

    mouse_list: list = [
      "left_mouse", 0x01, "right_mouse", 0x02, "middle_mouse", 0x04,
      "mouse_button1", 0x05, "mouse_button2", 0x06
    ]
    if mouse_button not in mouse_list and hex(mouse_button) not in mouse_list:
      Keyboard._Vars.error(error_type='r', runtime_error='given key code is not a mouse button')
      return Keyboard._Vars.exit_code
    original_name: str = mouse_button  # Keeps the original string before reassignment

    if Keyboard._lookup(mouse_button) is not False:
      mouse_button: int = Keyboard._lookup(mouse_button)
    elif mouse_button not in Keyboard.vk_codes and mouse_button not in Keyboard.vk_codes.values():
      Keyboard._Vars.error(error_type='r', runtime_error='given key code is not valid')
      return Keyboard._Vars.exit_code

    Keyboard.pressMouse(original_name)
    Keyboard.releaseMouse(original_name)

  @staticmethod
  def keyboardWrite(source_str: str) -> None:
    """
    Writes by sending virtual inputs

    Args:
      source_str (str): The string to be inputted on the keyboard, all
      keys in the 'Alphanumerical' section of vk_codes dict are valid
    """
    if not isinstance(source_str, str):
      Keyboard._Vars.error(error_type='p', var='string', type='string')
      return Keyboard._Vars.exit_code

    str_list: list = list(source_str)
    shift_alternate: list = [
      '|', '~', '?', ':', '{', '}', '\"', '!', '@',
      '#', '$', '%', '^', '&', '*', '(', ')', '+',
      '<', '>', '_'
    ]
    for char in str_list:
      if char not in Keyboard.vk_codes and not char.isupper():
        Keyboard._Vars.error(
          error_type='r',
          runtime_error=f'character: {char} is not in vk_codes map'
        )
        return Keyboard._Vars.exit_code

      if char.isupper() or char in shift_alternate:
        Keyboard.pressKey('shift')
      else:
        Keyboard.releaseKey('shift')

      key_code: int = Keyboard._lookup(char.lower())  # All dict entry's all lowercase
      x: Keyboard.INPUT = Keyboard.INPUT(
        type=Keyboard._Vars.INPUT_KEYBOARD,
        ki=KEYBDINPUT(wVk=key_code)
      )
      Keyboard._Vars.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

      y: Keyboard.INPUT = Keyboard.INPUT(
        type=Keyboard._Vars.INPUT_KEYBOARD,
        ki=KEYBDINPUT(
          wVk=key_code,
          dwFlags=Keyboard._Vars.KEYEVENTF_KEYUP
        )
      )
      Keyboard._Vars.user32.SendInput(1, ctypes.byref(y), ctypes.sizeof(y))
    Keyboard.releaseKey('shift')  # Incase it is not already released

  @staticmethod
  def altTab() -> None:
    """
    My development test function, just opens alt-tab menu
    """
    # Here we use the value of alt and tab, so we can
    # test if the functions still take VK codes directly
    Keyboard.pressKey(Keyboard.vk_codes['alt'])
    Keyboard.pressKey(Keyboard.vk_codes['tab'])
    Keyboard.releaseKey(Keyboard.vk_codes['tab'])
    time.sleep(2)
    Keyboard.releaseKey(Keyboard.vk_codes['alt'])


class Helper:

  def takeWebcamShot():
    resolution = (1920, 1080)
    pic_name = 'webcam-shot.png'
    cap = cv2.VideoCapture(0)
    cap.set(3, resolution[0])  # set Width
    cap.set(4, resolution[1])  # set Height
    r, image = cap.read()
    cv2.imwrite(pic_name, image)
    return pic_name

  def getDisplayCount():
    with mss.mss() as sct:
      monitor_count = len(sct.monitors)
      return monitor_count

  def grabScreenshot():
    monitor_count = Helper.getDisplayCount()
    for i in range(monitor_count):
      mss.mss().shot(mon=i)

  def getTime():
    time = os.popen('time /t').read()
    return str(time)

  def getUptime():
    lib = ctypes.windll.kernel32
    t = lib.GetTickCount64()
    t = int(str(t)[:-3])
    mins, sec = divmod(t, 60)
    hour, mins = divmod(mins, 60)
    days, hour = divmod(hour, 24)
    return (f'{days} days, {hour:02}:{mins:02}')


# ---- Bot code starts here ----
token = open('token.key', 'r').read().replace('\n', '')  # Now u cant fuck this up
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
  os.system('cls')
  for guild in bot.guilds:
    print(f'* {guild.name} (ID: {guild.id})')
  print('Status: READY...\n')

  helpMsg = '''
    Command                      Description                     Args   
|----------------------------------------------------------------------|
| !ping          |  Returns the bot's current ping in MS       |  N/A  |
|----------------------------------------------------------------------|
| !send-input    |  Presses then releases any keyboard key     |  key  |
|----------------------------------------------------------------------|
| !press-mouse   |  Presses then releases any mouse button     |  key  |
|----------------------------------------------------------------------|
| !command       |  Passes a command to the system             |  cmd  |
|----------------------------------------------------------------------|
| !send-string   |  Sends a string of keyboard inputs          |  str  |
|----------------------------------------------------------------------|
| !scroll-mouse  |  Scroll mouse by args direction and amount  |  <2>  |
|----------------------------------------------------------------------|
| !find-mouse    |  Reply's with mouse's current location      |  X,Y  |
|----------------------------------------------------------------------|
| !move-mouse    |  Move mouse to given X & Y coordinates      |  N/A  |
|----------------------------------------------------------------------|
| !shutdown      |  Shuts down host computer                   |  N/A  |
|----------------------------------------------------------------------|
| !uptime        |  Returns host computer's uptime             |  N/A  |
|----------------------------------------------------------------------|
| !screenshot    |  Reply's with a screen shot of displays     |  N/A  |
|----------------------------------------------------------------------|
| !webcam-shot   |  Reply's with a shot of the webcam          |  N/A  |
|----------------------------------------------------------------------|
  '''

  target_channel = bot.get_channel(1137852190933913741)
  if target_channel:
    await target_channel.send(f'AFK bot initialized... {Helper.getTime()}')
    await target_channel.send(f'```{helpMsg}```')
  else:
    print(f'Channel with ID: "{target_channel}" not found.')
  print(helpMsg)


@bot.command(name='ping', description='Get bot latency')
async def ping(ctx):
  await ctx.reply(f'ET latency: {round(bot.latency, 1)}')


@bot.command(name='send-input', description='Sends an input to the computer')
async def sendInput(ctx, key):
  returnValue = Keyboard.pressAndReleaseKey(key)
  if returnValue == 'null':
    await ctx.reply(
      'ERROR: Keyboard.pressAndReleaseKey() returned "null" meaning an error occurred during execution.'
    )
    return None
  else:
    await ctx.reply(f'Pressed key: "{key}"')


@bot.command(name='press-mouse', description='Sends an input to the computer\'s mouse')
async def sendMouseInput(ctx, key):
  returnValue = Keyboard.pressAndReleaseMouse(key)
  if returnValue == 'null':
    await ctx.reply(
      'ERROR: Keyboard.pressAndReleaseMouse() returned "null" meaning an error occurred during execution.'
    )
    return None
  else:
    await ctx.reply(f'Pressed key: "{key}"')


@bot.command(name='command', description='Pass a command to PC')
async def passcmd(ctx, cmd):
  out = os.popen(cmd).read()
  if out != '':
    await ctx.reply(out)
  else:
    await ctx.reply('Command returned a blank string')


@bot.command(name='send-input-string', description='Sends the given string to the keyboard, each char is a key pressed')
async def sendString(ctx, *string):
  for currentWord in string:
    idx = string.index(currentWord)
    if idx + 1 != len(string):
      currentWord = currentWord + ' '  # Cause words are basicly arguments due to spaces :)
    returnValue = Keyboard.keyboardWrite(currentWord)

    if returnValue == 'null':
      await ctx.reply(
        'ERROR: Keyboard.keyboardWrite() returned "null" meaning an error occurred during execution.'
      )
      return None
  
  await ctx.reply(f'String: "{" ".join(string)}" sent to target computer\'s keyboard.')
  time.sleep(1)
  Helper.grabScreenshot()
  for i in range(Helper.getDisplayCount()):
    screen = f'monitor-{i + 1}.png'

    if os.path.exists(screen):
      with open(screen, 'rb') as f:
        picture = discord.File(f)

      await ctx.reply(f'Monitor {i + 1}', file=picture)


@bot.command(name='scroll-mouse', description='Scrolls mouse and reply\'s with screenshot')
async def scroll(ctx, direction, amount):
  returnValue = Keyboard.scrollMouse(direction, amount)

  if returnValue == 'null':
    await ctx.reply(
      'ERROR: Keyboard.scrollMouse() returned "null" meaning an error occurred during execution.'
    )
    return None
  
  await ctx.reply(f'Scroll: ({direction, amount}) has been sent to the mouse.')
  time.sleep(1)
  Helper.grabScreenshot()
  for i in range(Helper.getDisplayCount()):
    screen = f'monitor-{i + 1}.png'

    if os.path.exists(screen):
      with open(screen, 'rb') as f:
        picture = discord.File(f)

      await ctx.reply(f'Monitor {i + 1}', file=picture)


@bot.command(name='find-mouse', description='Reply\'s with mouse\'s current location')
async def getMouseLocation(ctx):
  position = Keyboard.ManipulateMouse.getPosition()
  await ctx.reply(f'The mouse is currently at: {position}')


@bot.command(name='move-mouse', description='Moves mouse to given X and Y')
async def moveMouseLocation(ctx, x, y):
  prev_position = Keyboard.ManipulateMouse.getPosition()
  Keyboard.ManipulateMouse.setPosition(x, y)
  await ctx.reply(f'The mouse was moved from: {prev_position} and is currently at: ({x}, {y})')


@bot.command(name='shutdown', description='Shuts down PC')
async def shutdown(ctx):
  shutdown_cmd = 'shutdown /s'
  os.system(shutdown_cmd)
  await ctx.reply('PC shutting down, ET going offline...')


@bot.command(name='uptime', description='Get computer uptime')
async def uptime(ctx):
  time = Helper.getUptime()
  await ctx.reply(time)


@bot.command(name='screenshot', description='Get a screenshot from the computer')
async def screenshot(ctx):
  Helper.grabScreenshot()
  for i in range(Helper.getDisplayCount()):
    screen = f'monitor-{i + 1}.png'

    if os.path.exists(screen):
      with open(screen, 'rb') as f:
        picture = discord.File(f)

      await ctx.reply(f'Monitor {i + 1}', file=picture)


@bot.command(name='webcam-shot', description='Grab a shot from the webcam')
async def grabWebcam(ctx):
  pic_name = Helper.takeWebcamShot()
  await ctx.reply('Webcam', file=discord.File(pic_name))


def start():
  try:
    bot.run(token)
  except Exception as f:
    print(f'Initialization function\'s try block tripped: {f}')
    sys.exit(1)


if __name__ == '__main__':
  start()
