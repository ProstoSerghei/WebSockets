import sys
import os

from cx_Freeze import setup, Executable


build_exe_options = {
    'packages': [
        'common',
        'logs',
        'client',
        'sqlite3',
        'dlls',
    ]
}

setup(
    name='mess_client',
    version='0.0.1',
    description='mess_client',
    options={
        'build_exe': build_exe_options
    },
    executables=[Executable(
        'client.py',
        # base='Win32GUI',
        target_name='client.exe'
    )]
)
