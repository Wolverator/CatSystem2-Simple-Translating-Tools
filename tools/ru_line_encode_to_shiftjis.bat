cd update13
for /f %%a IN ('dir /b *.txt') do php ../message.php %%a
set /p =