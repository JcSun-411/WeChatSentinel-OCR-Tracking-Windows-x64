@echo off
setlocal
"%~dp0WeChatSentinel.exe" --floating-ocr
if errorlevel 1 pause
