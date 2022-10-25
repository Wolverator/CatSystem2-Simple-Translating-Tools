# CatSystem2 Simple Tools
Single-click tools to "extract movies, images and text right into editable state" and "pack all it back". Or as simple as I am able to make it :D (WIP)

HUGE thanks to Trigger and his **[TriggersTools.CatSystem2 wiki](https://github.com/trigger-segfault/TriggersTools.CatSystem2)** for gathering all info on CS2 file formats and tools in one place!

### Known problems:
1) ShiftJIS (game engine encoding) doesn't support use of some specific symbols from some languages:
   + `Ää, Öö, Üü, ß` from German; 
   + `Áá, Ââ, Ãã, Àà, Çç, Éé, Êê, Íí, Óó, Ôô, Õõ, Úú` from portuguese; 
   + `Ññ` from Spanish; 
   + `Èè, Ëë, Îî, Ïï, Ûû, Ùù, Ÿÿ` from French; etc.

Possible solution = create and use custom font that shows required unsupported symbols instead of unused symbols (f.e. Cyrillic ones),
E.g.: you need the game to show word `Färbung` so you type something like `Fьrbung` and font shows `ь` as `ä`.

Grisaia `.int` files unpacker and extractor  = v0.6 possibly stable (?)\
Grisaia compiler for your edited files and packer those into `updateXX.int`  = 0.4 maybe stable (?)\
(should work with any CatSystem2 games, but if you encountered problems - contact me)

### TL;DR:
1) copy `.bat` files and `tools` folder into your game folder
2) run `_unpack.bat`
3) inside `extracted` folder remove files you don't need, change files you want changed
4) run `_pack.bat` - it will take all files in `extracted` folder and pack them into single `updateXX.int` file, where XX = 1 + biggest index of existing `updateYY.int` files (will be `update00.int` if there were no such files before)

## Unpacker features:
1) extracts:
   + `.int` and `.zt` archives (using `exkifint_v3.exe` by asmodean)\
   + `.hg2` and `.hg3` into `.bmp` (using `hgx2bmp.exe` by asmodean) - be careful while unpacking `image.int` - it might require up to 250 GB of disk space to extract all images!\
   + `.cst` into `.txt` (using `cs2_decompile.exe` by Trigger)
   + also extracts everything worth translating into `.xlsx` files inside according folder
2) results in files in according folders:
   + folder `animations` with `.anm` files (no unpacker for those yet)\
   +folder `images` with `.bmp` and `.jpg` files (already unpacked from `.int`, `.hg2` and `.hg3` formats)\
   + folder `movies` with `.mpg` files\
   + folder `scripts` with `.fes` and `.kcs` files (no unpacker for those yet)\
   + folder`sounds` with `.ogg` and `.wav` files\
   + folder `texts` with `.txt` files (already unpacked from `.cst` files)\
   + folder `clean texts for translations` with `.xslx` (extracted from text `.txt` files)\
   + if there were no files moved into folder after whole process - folder is removed (since it's empty)

## Packer features:
1) takes all files in `extracted` folder and packs them from according folders into `updateXX.int`, where `XX` is the index of existing update-files +1, starting with `update00.int`
2) takes translations from `.xlsx` files into `.txt` files and them packs `.cst` files
3) packing scripts 

## Tested on games:
1) **[Grisaia no Kajitsu](https://vndb.org/v5154)** (non-steam, unrated) and (steam, all-ages) =  ✅ success
2) **[Grisaia no Meikyuu](https://vndb.org/v7723)** (non-steam, unrated) =  ✅ success
3) **[Grisaia no Rakuen](https://vndb.org/v7724)** (non-steam, unrated) =  ✅ success

## Todo list:
1) create custom font for specific symbols and include option to use it with automatic symbols swapping.
   + f.e.: you type `ä`, packer understands it and replaces for "encoded" symbols, while ingame it'll still be shown as `ä`
