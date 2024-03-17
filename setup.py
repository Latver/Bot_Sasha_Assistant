# coding: utf-8

from cx_Freeze import setup, Executable

executables = [Executable('C:\\Прочее\\Bot_v2 главный\\Bot_main_menu.py')]

excludes = []

zip_include_packages = []

options = {
    'build_exe': {
        'include_msvcr': True,
        'excludes': excludes,
        'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',
    }
}

setup(name='Бот-помощник',
      version='1.7.2',
      description='Ассистент "Саша"',
      executables=executables,
      options=options)