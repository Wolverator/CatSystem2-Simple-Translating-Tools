@echo off
mode con: cols=150 lines=30
py -3.10 tools\apply_name_translations.py
@pause