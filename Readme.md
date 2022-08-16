# CatSystem2SimpleTools
Single-click tools to "extract movies, images and text right into editable state" and "pack all it back". Or as simple as I am able to make it :D (WIP)

HUGE thanks to Trigger and his **[TriggersTools.CatSystem2 wiki](https://github.com/trigger-segfault/TriggersTools.CatSystem2)** for gathering all info on CS2 file formats and tools in one place!


Unpacker v0.5.2 features:
1) extracts: \
1.1) `.int` and `.zt` archives (using `exkifint_v3.exe` by asmodean)\
1.2) `.hg2` and `.hg3` into `.bmp` (minimalistic version, using `hgx2bmp_noexpand.exe` by asmodean)\
1.3) `.cst` into `.txt` (tho, it's `.cst -> .out -> .txt`, but no-one will see `.out` files :D)
2) results in files in according folders:\
2.1) folder `animations` with `.anm` files (no unpacker for those yet)\
2.2) folder `images` with `.bmp` and `.jpg` files (already unpacked from `.int`, `.hg2` and `.hg3` formats)\
2.3) folder `movies` with `.mpg` files\
2.4) folder `scripts` with `.fes` and `.kcs` files (no unpacker for those yet)\
2.5) folder`sounds` with `.ogg` and `.wav` files\
2.6) folder `texts` with `.txt` files (already unpacked from `.cst` files)\
2.7) if there were no files moved into folder after whole process - folder is removed (since it's empty)

Tested on games:
1) **[Grisaia no Kajitsu](https://vndb.org/v5154)** (non-steam, unrated) =  ✅ success
2) **[Grisaia no Meikyuu](https://vndb.org/v7723)** (non-steam, unrated) =  ✅ success
3) **[Grisaia no Rakuen](https://vndb.org/v7724)** (non-steam, unrated) =  ✅ success

Todo list:
0) make main game's `.bin` and `.exe` usage easier for user (teach unpacker how to understand which file it needs to use)
1) duplicate clear text lines from `.txt`(which are with game code right now) into `.xlsx` to have 1st column as original text and 2nd column for enthusiasts' translation (which then will be read and packed by "all-in-one" packer)
2) move functions from `.php` files into `.exe`, `.py.` or `.bat` files, since now it requires user to install PHP in order to run this tool (it also requires Python 3.10, but that's easier than PHP, means acceptable, imo :thinking: )
3) implement `.fes` unpacker (if possible?)
4) implement `.kcs` unpacker (if possible?)
5) implement `.anm` unpacker (if possible?)