# My compile, run and print to terminal script for C and C++

# HUGE TODO READ THIS
# ADD EXCEPTION FOR "'gcc' is not recognized" AND cd TO THE MinGW PATH THEN EXECUTE COMMAND

import os, sys
import time
import random
from colorama import Fore, Back, Style

# CODE
'''
* All references to 'exe' in comments mean executable
* All functions use camelCase and variables use snake_case
* All variable declarations must be type hinted EX: num: int = 0
* Most test files are .c because it compiles a couple seconds faster
* If a function has parameters each variable must have specified types
* Functions without any parameters in a class must have the @staticmethod tag
* If a variable or function uses more than one type use EX: num: int | float = 0.1
'''

# TODO
'''
* Make it possible to compile multi source files and 
print the output of both files... (func: handleVArguments)
* Add a objectFile compile function and argument '-obj'
* COMPILE TO .EXE WHEN DONE CODING
'''


class vars:

  def error(error_type: str, var: str = None, type: str = None, runtime_error: str = None) -> None:
    if error_type == 'p':
      print(f'PARAMETER: Given variable {var} is not a {type}.')
    elif error_type == 'r':
      print(f'RUNTIME: {runtime_error.capitalize()}.')
    elif error_type == 'u':
      print('UNKNOWN: An unknown error was encountered.')

  DEV_MODE: bool = True
  exit_code: None = None  # Returned after an error
  C_compiler: str = r'c:\MinGW\bin\gcc.exe'
  CPP_compiler: str = r'c:\MinGW\bin\g++.exe'
  varg_list: list = ['-gf', '-test', '-msf', '-out']


class core:
  # Only can compile .o, .c, .cpp and .h

  @staticmethod
  def compilationCall() -> None:
    """
    Initializes the program and calls correct compile option
    """
    arg_table: dict = core.determineArguments()
    if 'dll_name' in arg_table and 'arg1' not in arg_table:
      core.compileDLL(arg_table)  # Single output file compile
    elif 'exe_name' in arg_table and 'arg1' not in arg_table:
      core.compileFiles(arg_table)  # Also only one output
    else:
      if 'arg1' not in arg_table:
        print(f'{Fore.RED}Neither "exe_name" or "dll_name" is in argument list.{Style.RESET_ALL}')
        return vars.exit_code
      else:
        core.handleVArguments(arg_table)

  @staticmethod
  def determineArguments() -> dict:
    """
    Puts all vargs into a map and return it for use

    Returns:
      dict: The map of files and keys
    """
    arg_list: list = list(sys.argv)
    source_file_counter: int = 0
    object_file_counter: int = 0
    header_file_counter: int = 0
    exe_file_counter: int = 0  # Used during multi-source file compilation
    dll_file_counter: int = 0  # This to...
    arg_counter: int = 0
    file_map: dict = {}

    for arg in arg_list:

      if arg.endswith('.cpp'):
        source_file_counter += 1
        if os.path.exists(arg):
          file_map[f'source_file{source_file_counter}']: str = arg
        else:
          vars.error(error_type='r', runtime_error='A file argument cannot be found')
          return vars.exit_code

      elif arg.endswith('.c'):
        source_file_counter += 1
        if os.path.exists(arg):
          file_map[f'source_file{source_file_counter}']: str = arg
        else:
          vars.error(error_type='r', runtime_error='A file argument cannot be found')
          return vars.exit_code

      elif arg.endswith('.o'):
        object_file_counter += 1
        if os.path.exists(arg) or arg_counter > 0:
          file_map[f'object_file{object_file_counter}']: str = arg
        else:
          vars.error(error_type='r', runtime_error='A file argument cannot be found')
          return vars.exit_code

      elif arg.endswith('.h'):
        header_file_counter += 1
        if os.path.exists(arg):
          file_map[f'header_file{header_file_counter}']: str = arg
        else:
          vars.error(error_type='r', runtime_error='A file argument cannot be found')
          return vars.exit_code

      elif arg.endswith('.exe'):
        exe_file_counter += 1
        if exe_file_counter == 1:
          file_map['exe_name']: str = arg
        else:
          file_map[f'exe_name{exe_file_counter}']: str = arg

      elif arg.endswith('.dll'):
        dll_file_counter += 1
        if dll_file_counter == 1:
          file_map['dll_name']: str = arg
        else:
          file_map[f'dll_name{dll_file_counter}']: str = arg

      elif arg[0] == '-':
        arg_counter += 1
        file_map[f'arg{arg_counter}']: str = arg

    if exe_file_counter + dll_file_counter == 0:
      if vars.DEV_MODE is not True:
        print(f'{Fore.RED}No executable file name given to compile too.{Style.RESET_ALL}')
        return vars.exit_code
    return file_map

  def filterFileList(file_list: list) -> list:  # This small function is to filter stupid args
    """
    Removes arguments from file_list then returns new list

    Args:
      file_list (list): The list of values from args

    Returns:
      list: The filtered list of file_list
    """
    if not isinstance(file_list, list):
      vars.error(error_type='p', var='file_list', type='list')
      return vars.exit_code

    for file in file_list:
      if file in vars.varg_list:
        file_list.remove(file)
    return file_list

  def executeFileAndPrint(exe_path: str) -> None:  # Attempted to make once
    """
    Executes a file and prints the os.popen read output

    Args:
      exe_path (str): The path to the executable file
    """
    if not isinstance(exe_path, str):
      vars.error(error_type='p', var='exe_path', type='string')
      return vars.exit_code

    exe_path: str = exe_path.replace('\\', '/')
    file_list: list = exe_path.split('/')
    exe_name: str = file_list[-1]
    exe_path: str = '/'.join(file_list[:-1])
    cd_command: str = f'cd {exe_path}'
    cur_dir: str = os.getcwd().replace('\\', '/')
    platform: str = sys.platform
    if len(file_list) > 1:
      # If true we use powershell, so we can cd to the directory
      # and run the file in one command using a semi-colan (;)
      if cur_dir in exe_path:
        if 'linux' in platform:
          command: str = f'{cd_command};./{exe_name}'
        else:
          command: str = f'ps {cd_command};./{exe_name}'
      else:
        exe_path: str = f'{cur_dir}/{exe_path}'
        cd_command: str = f'cd {exe_path}'
        if 'linux' in platform:
          command: str = f'{cd_command};./{exe_name}'
        else:
          command: str = f'ps {cd_command};./{exe_name}'
    else:
      if 'linux' in platform:
        command: str = f'./{exe_name}'
      else:
        command: str = exe_name
    command: str = command.replace('ps', 'powershell')
    file_output: str = os.popen(command).read()
    print(
      f'\n{Back.CYAN+Fore.WHITE} ----- {Back.RED} {exe_name} {Style.RESET_ALL+Back.CYAN} ----- {Style.RESET_ALL}'
    )
    if file_output == '':
      print(f'{Fore.RED}No output received from given executable.\n{Style.RESET_ALL}')
    else:
      print(file_output)
    line_list: list = []
    for i in range(len(exe_name) + 14):
      line_list.append('-')
    print(f'{Back.CYAN+Fore.WHITE} {"".join(line_list)} {Style.RESET_ALL}\n')

  def handleVArguments(file_map: dict) -> None:
    """
    Handles hyphen arguments or '-' args

    Args:
      file_map (dict): The map of arguments passed
    """
    if not isinstance(file_map, dict):
      vars.error(error_type='p', var='file_map', type='dict')
      return vars.exit_code

    argument_list: list = [
      arg for key, arg in file_map.items() if 'arg' in key
    ]
    for arg in argument_list:
      if arg == '-test':
        print('Hello, World!')
        return vars.exit_code

      if arg == '-gf':
        color_list: list = [
          Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.RED,
          Fore.YELLOW, Fore.WHITE
        ]
        ticker: int = random.randint(0, len(color_list) - 1)
        char_count: int = -1
        message: str = '!Feature Removed!'
        print('\033[?25l', end='')

        for i in range(100):  # Takes about 10 seconds
          for char in message:
            char_count += 1
            ticker += 1
            if ticker == len(color_list):
              ticker: int = 0
            color = color_list[ticker]  # This is a weird type
            if char_count == len(message):
              char_count: int = 0
              print('\x1b[2K', end='')
            else:
              print(f'{color}{char}{Style.RESET_ALL}', end='')

          print('\r', end='')
          char_count: int = -1
          ticker: int = random.randint(0, len(color_list) - 1)
          time.sleep(0.2)
        print('\033[?25h', end='')  # Shows cursor
        return vars.exit_code

      if arg == '-msf':  # Multiple source files
        core.compileMultipleExecutables(file_map)

      if arg == '-out':  # Runs compiled file
        # Only works with single file output no multi exe's or dll's
        if 'dll_name' in file_map and 'dll_name2' not in file_map:
          exe_file: str = core.compileDLL(file_map)
        elif 'exe_name' in file_map and 'exe_name2' not in file_map:
          exe_file: str = core.compileFiles(file_map)
        core.executeFileAndPrint(exe_file)

      if arg == '-obj':
        core.compileObject(file_map)

  def determineCompiler(file_list: list) -> str:
    """
    Determines what compiler to use depending on source file

    Args:
      file_list (list): The list of values in the file_map

    Returns:
      str: 'gcc' for all .c files and 'g++' for .cpp files
    """
    if not isinstance(file_list, list):
      vars.error(error_type='p', var='file_list', type='list')
      return vars.exit_code

    compiler_type: None = None
    for file in file_list:
      if file.endswith('.cpp'):
        compiler_type: str = 'g++'
      if file.endswith('.c'):
        compiler_type: str = 'gcc'
    return compiler_type

  def compileCountdown(hide_cursor: bool = True) -> None:
    """
    Counts down till compile process and also prints the separator

    Args:
      hide_cursor (bool): Hides cursor if is true
    """
    if not isinstance(hide_cursor, bool):
      vars.error(error_type='p', var='hide_cursor', type='bool')
      return vars.exit_code

    if hide_cursor is True:
      print('\033[?25l', end='')  # Hides cursor
    print('-----------------------------------------------------------------')
    for i in reversed(range(1, 4)):
      if i == 3: color = Fore.GREEN
      if i == 2: color = Fore.YELLOW
      if i == 1 or i == 0: color = Fore.RED
      print(f'Build operation starting in: {color}{i}...{Style.RESET_ALL}', end='\r')
      time.sleep(1)
    if hide_cursor is True:
      print('\033[?25h', end='')  # Shows cursor
    print('\x1b[2K', end='')

  def outputCompileTime(total_compile_time: float | int, ticker: int) -> None:
    """
    Changes the color of the compile time if its a certain number

    Args:
      total_compile_time (int): The total time compilation took
    """
    if not isinstance(total_compile_time, float | int):
      vars.error(error_type='p', var='total_compile_time', type='float')
      return vars.exit_code
    if not isinstance(ticker, int):
      vars.error(error_type='p', var='ticker', type='integer')
      return vars.exit_code

    comp_time: float = round(total_compile_time, 2)
    if total_compile_time < 1.5:
      print(
        f'\n({ticker}) file compilation took: {Fore.GREEN}{comp_time}{Style.RESET_ALL} seconds\n'
      )
    elif total_compile_time < 3:
      print(
        f'\n({ticker}) file compilation took: {Fore.YELLOW}{comp_time}{Style.RESET_ALL} seconds\n'
      )
    elif total_compile_time > 4:
      print(
        f'\n({ticker}) file compilation took: {Fore.RED}{comp_time}{Style.RESET_ALL} seconds\n'
      )

  def outputCompilerText(compiler_text: str, file_list: list, compiled_file: str) -> None:
    """
    Prints the completion text after attempted compilation

    Args:
      compiler_text (str): The output from the popen command
      file_list (list): The list of files used at compilation
      compiled_file (str): The compiled file's name
    """
    if not isinstance(file_list, list):
      vars.error(error_type='p', var='file_list', type='list')
      return vars.exit_code
    if not isinstance(compiler_text, str):
      vars.error(error_type='p', var='compiler_text', type='string')
      return vars.exit_code
    if not isinstance(compiled_file, str):
      vars.error(error_type='p', var='compiled_file', type='string')
      return vars.exit_code

    if compiled_file.endswith('.exe'):
      compile_type: str = 'executable'.upper()
    else:
      compile_type: str = 'dynamic link library'.upper()

    # Really ugly console output code
    if compiler_text == '':
      file_list[-1]: str = ''
      if len(file_list) == 2:
        files: str = ''.join(file_list)
        if os.path.exists(compiled_file):
          print(
            f'\n{Fore.GREEN}!SUCCESS!{Style.RESET_ALL} Compiled file: ({files} -> {compiled_file}) | {Back.WHITE+Fore.BLACK}{compile_type}{Style.RESET_ALL}\n'
          )
        else:
          print(
            f'\n{Fore.RED}!FAILED!{Style.RESET_ALL} Attempted compile: ({files} -> {compiled_file}) | {Back.WHITE+Fore.BLACK}{compile_type}{Style.RESET_ALL}\n'
          )
      else:
        files: str = ', '.join(file_list)[:-2]
        if os.path.exists(compiled_file):
          print(
            f'\n{Fore.GREEN}!SUCCESS!{Style.RESET_ALL} Compiled file: ({files} -> {compiled_file}) | {Back.WHITE+Fore.BLACK}{compile_type}{Style.RESET_ALL}\n'
          )
        else:
          print(
            f'\n{Fore.RED}!FAILED!{Style.RESET_ALL} Attempted compile: ({files} -> {compiled_file}) | {Back.WHITE+Fore.BLACK}{compile_type}{Style.RESET_ALL}\n'
          )
    else:
      print(compiler_text)

  def compileMultipleExecutables(file_map: dict) -> list:
    """
    Turns a multiple .c or .cpp files into exe's and dll's

    Args:
      file_map (dict): The map of files from determineArguments()

    Returns:
      list: The compiled files path/name
    """
    if not isinstance(file_map, dict):
      vars.error(error_type='p', var='file_map', type='dict')
      return vars.exit_code

    file_list: list = list(file_map.values())
    passed_exe_files: list = []  # Passed .exe or .dll files
    passed_src_files: list = []  # Passed .c or .cpp files
    compiled_files: list = []  # List to be returned

    for file in file_list:
      if file.endswith('.cpp'):
        passed_src_files.append(file)
      elif file.endswith('.c'):
        passed_src_files.append(file)
      elif file.endswith('.exe'):
        passed_exe_files.append(file)
      elif file.endswith('.dll'):
        passed_exe_files.append(file)

    core.compileCountdown()
    total_compile_time: int = 0
    ticker: int = 0

    for src_file in passed_src_files:
      st: float = time.time()
      cmd_list: list = []
      # Parsing makes a check for length of 2
      source: list = [src_file, '']
      ticker += 1

      if src_file.endswith('.cpp'):
        compiler_type: str = 'g++'
      if src_file.endswith('.c'):
        compiler_type: str = 'gcc'
      file_idx: int = passed_src_files.index(src_file)
      exe_file: str = passed_exe_files[file_idx]
      cmd_list.append(src_file)
      cmd_list.append(exe_file)

      cmd_list.insert(-1, '-o')
      cmd_list.insert(0, compiler_type)
      command: str = ' '.join(cmd_list)
      compiler_return: str = os.popen(command).read()
      core.outputCompilerText(compiler_return, source, exe_file)
      et: float = time.time()
      compile_time: float = round(et - st, 2)
      total_compile_time += compile_time
      print(
        f'{ticker}. {Back.MAGENTA}{compiler_type.upper()}{Style.RESET_ALL} compilation took: {Fore.BLUE}{compile_time}{Style.RESET_ALL} seconds\n'
      )
      compiled_files.append(exe_file)

    core.outputCompileTime(total_compile_time, ticker)
    print('-----------------------------------------------------------------')
    return compiled_files

  def compileFiles(file_map: dict) -> str:
    """
    Compiles .c, .o, .h and .cpp files into executable's

    Args:
      file_map (dict): The map of files from determineArguments()

    Returns:
      str: The compiled files path/name
    """
    if not isinstance(file_map, dict):
      vars.error(error_type='p', var='file_map', type='dict')
      return vars.exit_code

    st: float = time.time()
    file_list: list = list(file_map.values())
    compiler_type: str = core.determineCompiler(file_list)
    cmd_list: list = []

    for file in file_list:
      if file.endswith('.cpp'):
        cmd_list.append(file)
      elif file.endswith('.c'):
        cmd_list.append(file)
      elif file.endswith('.o'):
        cmd_list.append(file)
      elif file.endswith('.h'):
        cmd_list.append(file)
      elif file.endswith('.exe'):
        output_file: str = file
        cmd_list.append(file)
    core.compileCountdown()

    cmd_list.insert(-1, '-o')
    cmd_list.insert(0, compiler_type)
    command: str = ' '.join(cmd_list)
    compiler_return: str = os.popen(command).read()
    file_list: list = core.filterFileList(file_list)
    core.outputCompilerText(compiler_return, file_list, output_file)
    et: float = time.time()
    compile_time: float = round(et - st - 3, 2)
    print(
      f'\n{Back.MAGENTA}{compiler_type.upper()}{Style.RESET_ALL} compilation took: {Fore.BLUE}{compile_time}{Style.RESET_ALL} seconds\n'
    )
    print('-----------------------------------------------------------------')
    return output_file

  def compileObject(file_map: dict) -> str:
    """
    Turns a .c or .cpp file into a .o file

    Args:
      file_map (dict): The map of files from determineArguments()

    Returns:
      str: The compiled files path/name
    """
    if not isinstance(file_map, dict):
      vars.error(error_type='p', var='file_map', type='dict')
      return vars.exit_code

    st: float = time.time()
    file_list: list = list(file_map.values())
    compiler_type: str = core.determineCompiler(file_list)
    passed_files: list = []
    holding_list: list = []
    cmd_list: list = []

    for file in file_list:
      if file.endswith('.cpp'):
        passed_files.append(file.replace('.cpp', '.o'))
        cmd_list.append(file)
      elif file.endswith('.c'):
        passed_files.append(file.replace('.c', '.o'))
        cmd_list.append(file)
      elif file.endswith('.o'):
        passed_files.append(file)
        object_file: str = file.replace('\\', '/')
    #core.compileCountdown()
    print(holding_list, cmd_list, passed_files)

    cmd_list.insert(-1, '-c')
    cmd_list.insert(0, compiler_type)
    # NOTE: I think for every dir we cd to we add a ../ to the compile file
    cd_command: str = f'cd {"/".join(object_file.split("/")[:-1])}'
    cmd_list.insert(0, f'{cd_command} ;')
    command: str = ' '.join(cmd_list)
    print(command)  # Whenever changing dirs to the output one we cannot
    # compile the source file without adding ../.. to get to the directory
    # EX: (cd out/sub ; gcc -c ../../src/foo.c) out/sub is the output dir
    # and src/foo.c is the location of the source file after compilation
    # in this example the compiled file should be in out/sub/foo.o but 
    # we must cd back then into the directory
    print(os.popen(command).read())

  def compileDLL(file_map: dict) -> str:
    # I know this is a long function for only making like 3 sys calls with but this is
    # the legacy way of make .dll files (https://www.cygwin.com/cygwin-ug-net/dll.html)
    """
    Turns a .c or .cpp file into a .dll file after turning it into an object file

    Args:
      file_map (dict): The map of files from determineArguments()

    Returns:
      str: The compiled files path/name
    """
    if not isinstance(file_map, dict):
      vars.error(error_type='p', var='file_map', type='dict')
      return vars.exit_code

    st: float = time.time()
    file_list: list = list(file_map.values())
    compiler_type: str = core.determineCompiler(file_list)
    passed_files: list = []
    holding_list: list = []
    cmd_list: list = []

    for file in file_list:
      if file.endswith('.cpp'):
        passed_files.append(file.replace('.cpp', '.o'))
        holding_list.append(file)
      elif file.endswith('.c'):
        passed_files.append(file.replace('.c', '.o'))
        holding_list.append(file)
      elif file.endswith('.dll'):
        passed_files.append(file)

    for file in holding_list:
      if file.endswith('.cpp'):
        passed_files.append(file.replace('.cpp', '.o'))
        cmd_list.append(file.split('/')[-1])
      elif file.endswith('.c'):
        passed_files.append(file.replace('.c', '.o'))
        cmd_list.append(file.split('/')[-1])
    core.compileCountdown()

    cmd_list.insert(-1, '-c')
    cmd_list.insert(0, compiler_type)
    cd_command: str = f'cd {"/".join(holding_list[-1].split("/")[:-1])}'
    cmd_list.insert(0, f'{cd_command} ;')
    command: str = ' '.join(cmd_list)
    os.popen(command).read()  # No need to make 'compiler_return' var here
    cmd_list: list = []

    for file in passed_files:
      if file.endswith('.dll') and file not in cmd_list:
        output_file: str = file
        cmd_list.insert(0, file)  # Put .dll in front
      elif file.endswith('.o') and file not in cmd_list:
        object_file: str = file
        cmd_list.append(file)  # Add .o to any place

    cmd_list.insert(0, '-shared')
    cmd_list.insert(1, '-o')
    cmd_list.insert(0, compiler_type)
    command: str = ' '.join(cmd_list)
    compiler_return: str = os.popen(command).read()
    os.remove(object_file)  # Therefore we only return the .dll
    file_list: list = core.filterFileList(file_list)
    core.outputCompilerText(compiler_return, file_list, output_file)
    et: float = time.time()
    compile_time: float = round(et - st - 3, 2)
    print(
      f'\n{Back.MAGENTA}{compiler_type.upper()}{Style.RESET_ALL} compilation took: {Fore.BLUE}{compile_time}{Style.RESET_ALL} seconds\n'
    )
    print('-----------------------------------------------------------------')
    return output_file


core.compilationCall()
