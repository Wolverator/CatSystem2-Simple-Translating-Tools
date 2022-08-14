:: CatSystem2 files unpacker
:: lines that start with "::" - are commentaries 


::do all required steps for unpacking
for /f %%a IN ('dir /b *.cst') do Decat2 %%a
for /f %%a IN ('dir /b *.out') do php convert.php %%a
::TODO use txt-to-xlsx

@echo off
echo Removing temporary files...
::remove temporary files
FOR %%A IN (*.out) DO DEL %%A
python unpack.py
pause