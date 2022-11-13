# CatSystem2 Simple Translating Tools
Single-click tools to "extract text right into editable state" and "pack all it back". Or as simple as I am able to make it :D (WIP)

####  Changelog v0.7:
+ Added logic to process `nametable.csv` and translate it, as I've found out that it is required to make some in-game functions work.
+ Now launching `1) unpack.bat` more than once won't remove any translation in the according cells in `.xlsx` files that you've already filled in.
+ Changed folders structure to improve "user-friendliness" of new tools' logic.
+ If you're updating from previous version of this tool - make backup copy of your `.xslx` files with translations, then copy them into `translate here/clean texts/` folder.\
Then you will need to run steps 1 and 2 from `How to use` section again, but it should keep all your translated progress intact, only changing names column.

As of v0.7 there is only text being automatically extracted to xlsx files prepared for translation and then being packed back.
Images (`.hg2`), videos (`.mpg`), sounds (`.ogg`) and other files will be in according folders for manual editing if you need them.

HUGE thanks to Trigger and his **[TriggersTools.CatSystem2 wiki](https://github.com/trigger-segfault/TriggersTools.CatSystem2)** for gathering all info on CS2 file formats and tools in one place!

### Known problems:
1) ShiftJIS (game engine encoding) doesn't support use of some specific symbols from some languages:
   + `Ää, Öö, Üü, ß` from German; 
   + `Áá, Ââ, Ãã, Àà, Çç, Éé, Êê, Íí, Óó, Ôô, Õõ, Úú` from portuguese; 
   + `Ññ` from Spanish; 
   + `Èè, Ëë, Îî, Ïï, Ûû, Ùù, Ÿÿ` from French; etc.

   Possible solution = create and use custom font that shows required unsupported symbols instead of unused symbols (f.e. Cyrillic ones),
E.g.: you need the game to show word `Färbung` so you type something like `Fьrbung` and font shows `ь` as `ä`. Added it into ToDo list, will try to solve later.


## How to use:
0) copy `.bat` files and `tools` folder into your game folder
1) run `1) unpack.bat` to get:
   * `source game files` will be all extracted game files. They are there for references, if you need them - copy them into other folder and edit them there. 
   * `translate here` folder with `.xlsx` files that contains all text possible to translate
2) translate names in `translate here/nametable.xlsx` and run `2) apply names translations.bat` to apply names translations to all `.xslx` files in `translate here/clean texts/` folder. (made for exact names placing to make sure some in-game features still work)
3) running `3) pack.bat` will generate `updateXX.in` archive with files included:
   * all translations from `translate here/clean texts/` `.xlsx` files will be automatically converted into `.cst` game scenes scripts
   * all files from subfolders in `translate here/your files AS IS` folder (do NOT place files directly in `your files AS IS` - they will be ignored! Use `your files AS IS/other` folder for that)


## Unpacker features:
1) extracts:
   + `.int` and `.zt` archives (using `exkifint_v3.exe` by asmodean)
   + `.cst` into `.txt` (using `cs2_decompile.exe` by Trigger)
   + also extracts everything worth translating into `.xlsx` files inside according folder
2) places files in according folders:
   * `source game files` folder with original game files used later as reference
      + folder `texts` with `.txt` files (already unpacked from `.cst` files)
      + folder `for manual processing` with other files:
        1) folder `animations` with `.anm` files
        2) folder `images` with `.hg2` and `.hg3` files
        3) folder `movies` with `.mpg` files
        4) folder `scripts` with `.fes` and `.kcs` files
        5) folder `sounds` with `.ogg` and `.wav` files
   * `translate here` folder with everything ready to be translated or packed:
      + folder `clean texts` with `.xslx` files containing main game texts (extracted from text `.txt` files, will be used by this tool to generate new scene-files for your game)
      + folder `your files AS IS` with categories (files you add there will be packed into archive, but won't be changed by this tool)



## Packer features:
1) copies original game files from `source game files/texts` folder and `nametable.csv`, applies translations and packs translated files
2) takes all files in `translate here/your files AS IS` subfolders and packs them "as is"

## Tested on games:
1) **[Grisaia no Kajitsu](https://vndb.org/v5154)** (non-steam, unrated) and (steam, all-ages) =  ✅ success
2) **[Grisaia no Meikyuu](https://vndb.org/v7723)** (non-steam, unrated) =  ✅ success
3) **[Grisaia no Rakuen](https://vndb.org/v7724)** (non-steam, unrated) =  ✅ success

## Todo list:
1) create custom font for specific symbols and include option to use it with automatic symbols swapping.
   + f.e.: you type `ä`, packer understands it and replaces for "encoded" symbols, while ingame it'll still be shown as `ä`
