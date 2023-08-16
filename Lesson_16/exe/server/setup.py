import sys
import os

from cx_Freeze import setup, Executable


build_exe_options = {
    'packages': [
        'common',
        'logs',
        'server',
    ]
}

setup(
    name='mess_server',
    version='0.0.1',
    description='mess_server',
    options={
        'build_exe': build_exe_options
    },
    executables=[Executable(
        'server.py',
        # base='Win32GUI',
        target_name='server.exe'
    )]
)
