# Paint-Program
A remake of MS Paint, with additional cool features (see below).

# Downloading

This repo includes pygame 2.0.0 because of certain functions behaving slightly differently if pygame 1.x.x is used

user_agent (module used to download images) is also included

If you do not wish to download either package (or if you already have those 2 installed), here are the files/folders you should download for the program to function:

* main.py
* image_downloader_modified.py
* static (folder)
* saved images (folder)


# Usage
To use the program, simply click on main.py. Note that you must have Python 3 installed already.


# List of individual features

* tool select highlight: a red border around the selected tool. press tab to cycle through the tools. also applies to music player buttons

* highlighting tool

* spraypaint

* undo/redo

* import image moving and resizing: after importing an image, click on the image, move the mouse and click again to where you want to move it. to resize, click on the small circle, move the mouse to reiszethen click again after finishing resize.

* image stamps searching: need a stamp for anything? just type in the search bar, search, and stamp it on. results randomized. to return to original stamps, press search without any inputting any keywords
    
* music player; featuring previous track, next track, pause/play, play through mode, loop play mode, and shuffle mode. 
    
* convenient keyboard shortcuts:
    * "u" to undo
    * "r" to redo
    * enter to search
    * tab to cycle through tools (dont worry, tools such as clear screen, import/export, undo/redo wont be executed automatically if u do this)
    * spacebar to play/pause music
    * left arrow/right arrow to change music playing mode (in order play through, loop, shuffle
    * page down/page up to toggle next track/previous track


# Additional Notes

* theoretically all necessary packages/modules (pygame and user_agent) should already come with the program folder, provided that Python 3 is installed on the computer already

* the theme of this paint project is...Wood!

* you cannot download images from the internet if you do not have internet :D however the rest of the program will still be usable

* more than one keyword can be typed into the search bar. each time the search engine will scrape random images so that you dont get the same results every time. searching an empty string will load preloaded stamps

* you can scroll up or down to change the drawwidth, or the up and down arrows. for functionality, the width will be limited to between 1 to 40 pixels, and you cannot change drawing width during a stroke. this will end the stroke.

* filling a large area with the paint bucket will work, but it takes a couple seconds. to floodfill the entire canvas, expect around 2-4 seconds on a regular laptop

* unfilled pixels may appear on the border of an unfilled ellipse. this is somewhat inevitable

* when you try to save the canvas, the dialog will lead you to the "saved images" directory of the folder, but you can save it anywhere on your computer

* similarly, importing will lead you to the "images" directory first (this way you can find all the images previously searched), but you can import from anywhere on the pc

* dont like the music? just replace the music in the static/music folder (not hardcoded), but remember to index from 0 -> n-1, where n is the amount of songs
