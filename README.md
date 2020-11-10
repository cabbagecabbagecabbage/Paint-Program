# Paint Program
A remake of MS Paint, with additional cool features (see below).

<br>

## Downloading
The easiest way to download is to click on the green "Code" button, and click download zip folder.

<br>

## Usage
To use the program, you need to satisfy the following requirements:
* Python 3
* pygame 2.0.0 or higher (pygame 1.x.x will cause the program to crash eventually)
* user_agent

Python 3 can be installed at https://www.python.org/downloads/

If any of the modules/packages are missing, follow these steps:
1. go to the Python Shell (idle)
2. run `import sys`
3. run `sys.path`, copy one of the paths
4. go to the command shell and type `pip install <package name> -t"<copied path>"`
    
A restart may or may not be required after installing a new package

After all the packages are installed, simply run main.py

<br>

## List of Individual Features

* tool select highlight: a red border around the selected tool. also applies to music player buttons

* highlighting tool

* spraypaint

* undo/redo

* import image moving and resizing: after importing an image, click on the image, move the mouse and click again to where you want to move it. to resize, click on the small circle, move the mouse to reisze then click again after finishing resize.

* image stamps searching: need a stamp for anything? just type in the search bar, search, and stamp it on. results randomized. to return to original stamps, press search without any inputting any keywords
    
* music player; featuring previous track, next track, pause/play, play through mode, loop play mode, and shuffle mode. 
    
* convenient keyboard shortcuts:
    * "u" to undo
    * "r" to redo
    * enter to search
    * tab to cycle through tools (dont worry, tools such as clear screen, import/export, undo/redo wont be executed automatically if u do this)
    * spacebar to play/pause music
    * page down/page up to toggle next track/previous track
    * left arrow/right arrow to change music playing mode (in order play through, loop, shuffle
    * up/down arrow or scrollwheel to change drawing width
    

* additional features:
    * colour preview box also shows drawing width
    * info bar shows the name of the tool selected, (R,G,B) of colour chosen, mouse position on the canvas, and current song track
    * the cursor is replaced with a crosshair when on the canvas for better visibility and accuracy when drawing
    * if you have not saved the canvas during the session yet, the program will ask you whether you would like to save the canvas before exiting. if so, it will automatically         commence the saving dialogue for you

<br>

## Additional Notes

* the theme of this paint project is...Wood!

* you cannot download images from the internet if you do not have internet :D however the rest of the program will still be usable

* more than one keyword can be typed into the search bar. each time the search engine will scrape random images so that you dont get the same results every time. searching an empty string will load preloaded stamps. keyboard shortcuts will not be activated while you are typing in the search bar

* you can scroll up or down to change the drawwidth, or the up and down arrows. for functionality, the width will be limited to between 1 to 40 pixels, and you cannot change drawing width during a stroke. this will end the stroke.

* filling a large area with the paint bucket will work, but it takes a couple seconds. to floodfill the entire canvas, expect around 2-4 seconds on a regular laptop

* unfilled pixels may appear on the border of an unfilled ellipse. this is somewhat inevitable

* when you try to save the canvas, the dialog will lead you to the "saved images" directory of the folder, but you can save it anywhere on your computer

* similarly, importing will lead you to the "images" directory first (this way you can find all the images previously searched), but you can import from anywhere on the pc

* don't like the music? just replace the music in the static/music folder (not hardcoded), but remember to index from 0 -> n-1, where n is the number of songs
