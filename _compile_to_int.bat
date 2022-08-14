copy mc.exe update13\mc.exe

cd update13
for /f %%a IN ('dir /b *.txt') do php ../insert_text.php %%a
mc.exe *

del mc.exe

cd ..
makeint update13.int update13\*.cst
set /p =