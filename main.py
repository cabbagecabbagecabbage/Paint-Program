'''
ICS3U Paint Project main.py
By Rayton Chen

for more info:

https://github.com/cabbagecabbagecabbage/Paint-Program

'''

########################### import packages ###########################
import sys
from pygame import *
from pygame.locals import *
from pygame.color import Color as c
from random import *
from image_downloader_modified import download_images #image downloader (google image search result html parsing) SEE THE ORIGINAL FILE FOR MORE INFO
from os import *
import shutil
from math import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *

init()
root = Tk()
root.withdraw()

########################### create objects ###########################

class bg: #background objects
    def __init__(self,dim):
        self.w = dim[0]
        self.h = dim[1]
        self.surface = Surface(dim)
        self.surface.set_alpha(100)
        self.surface.fill(c("black"))

class button: #button objects
    def __init__(self,x,y,mode):
        self.x = x
        self.y = y
        self.rect = Rect(x,y,35,35)
        self.mode = mode

    #function that checks if said button is pressed
    def checkpressed(self,pos):
        global mode
        mx,my = pos
        if self.rect.collidepoint((mx,my)):
            if mode != self.mode:
                mode = self.mode
                return True
        if not cprect.collidepoint(pos) and not canvas.collidepoint(pos):
            mode = 0
        return False

########################### create functions ###########################

# canvas functions

def capture():
    #permanently captures the screen, appends into the undo list
    global screencap, undo, redo, action, saved
    screencap = screen.subsurface(canvas).copy()
    undo.append(screencap)
    redo = []
    action = 0
    saved = 0

def handleUndo():
    #undo the last action, append into redo list
    global undo, redo, screencap, mode
    try:
        prevcap = undo.pop()
        redo.append(prevcap)
        screencap = undo[-1]
    except:
        pass
    mode = 0

def handleRedo():
    #redo the action, append into undo list
    global undo, redo, screencap, mode
    try:
        nextcap = redo.pop()
        undo.append(nextcap)
        screencap = nextcap
    except:
        pass
    mode = 0


# event handling #

def handleMousePress(evt):
    #handle MOUSEBUTTONDOWN event, including scroll wheel events to change drawwidth. also checks button press events
    global text, imglist, mode, chosencolour, drawwidth, startx, starty, action, imgmoving, imgrect, importimg, imgresize, stamping, stampimg,stampoffset
    if evt.button == 4:
        drawwidth = min(drawwidth+1,40)
    if evt.button == 5:
        drawwidth = max(drawwidth-1,1)

    #must left click, check button press and change modes. handle import image resizing
    if evt.button == 1:
        if canvas.collidepoint(evt.pos):
            action = 1
            startx, starty = evt.pos
            if stamping == 1 and mode == 0:
                screen.blit(stampimg,(evt.pos[0]-stampoffset[0]//2,evt.pos[1]-stampoffset[1]//2))
                capture()
        else: action = 0

        #imported image resizing
        if modes[mode] == "import":
            if not imgrect.collidepoint(evt.pos) and hypot(abs(evt.pos[0]-imgrect[0]-imgrect[2]), abs(evt.pos[1]-imgrect[1]-imgrect[3])) > 6:
                screen.blit(importimg,imgrect)
                capture()
                imgmoving = 0
                mode = 0
                importimg = Surface((0,0))
                imgrect = Rect(0,0,0,0)

            elif hypot(abs(evt.pos[0]-imgrect[0]-imgrect[2]), abs(evt.pos[1]-imgrect[1]-imgrect[3])) <=5:
                imgresize = not imgresize

            elif imgrect.collidepoint(evt.pos):
                imgmoving = not imgmoving
                
        #check every button's press state
        for b in buttons:
            if b.checkpressed(evt.pos):
                break

        #check colour picker press state
        if cprect.collidepoint(evt.pos):
            chosencolour = screen.get_at(evt.pos)

        #check image search press state
        elif imgsearch.collidepoint(evt.pos):
            mode = 0 if mode == 1 else 1
        elif searchbtn.collidepoint(evt.pos):
            handleDownload()

        #check stamps press state
        for i in range(len(stamprects)):
            if stamprects[i].collidepoint(evt.pos):
                mode = 0
                stamping = 1
                stampimg = imglist[i]
                stampoffset = stamprects[i][2],stamprects[i][3]


def handleMusic(evt):
    #check if there are any interactions with the music player, and handle each event
    global cur,cursong,prevsong,nextsong,musicmode
    if playerrect.collidepoint(evt.pos):
        if playrect.collidepoint(evt.pos):
            togglePlay()  
        elif prevrect.collidepoint(evt.pos):
            handleMusicPrevious()
        elif nextrect.collidepoint(evt.pos):
            handleMusicNext()
        elif inorderrect.collidepoint(evt.pos):
            musicmode = "inorder"
        elif looprect.collidepoint(evt.pos):
            musicmode = "loop"
        elif shufflerect.collidepoint(evt.pos):
            musicmode = "shuffle"

def togglePlay():
    #toggle play or pause
    global cur
    if cur == playimg:
        cur = pauseimg
        mixer.music.unpause()
    elif cur == pauseimg:
        cur = playimg
        mixer.music.pause()

def handleMusicPrevious():
    #regardless of the mode, play the previous song of the playlist
    global nextsong,cursong,prevsong,playprevborder,borderframecount, cur
    playprevborder = 1
    borderframecount = 10
    mixer.music.unload()
    mixer.music.load(musicfnames[prevsong])
    mixer.music.play()
    nextsong = cursong
    cursong = prevsong
    prevsong = (prevsong-1+musicquant)%musicquant
    cur = pauseimg
        
def handleMusicNext():
    #depending on the mode, play the next song of the playlist
    global nextsong,cursong,prevsong,playnextborder,borderframecount, cur
    playnextborder = 1
    borderframecount = 10
    if musicmode == "loop":
        mixer.music.play()
    elif musicmode == "inorder":
        mixer.music.unload()
        mixer.music.load(musicfnames[nextsong])
        mixer.music.play()
        prevsong = cursong
        cursong = nextsong
        nextsong = (nextsong+1)%musicquant
    elif musicmode == "shuffle":
        cursong = randint(0,musicquant-1)
        prevsong = (cursong-1+musicquant)%musicquant
        nextsong = (cursong+1)%musicquant
        mixer.music.unload()
        mixer.music.load(musicfnames[cursong])
        mixer.music.play()
    cur = pauseimg

def nextMusicMode():
    #toggle music playing mode: next
    global musicmode
    for i in range(3):
        if musicmodes[i] == musicmode:
            musicmode = musicmodes[(i+1)%3]
            break

def prevMusicMode():
    #toggle music playing mode: previous
    global musicmode
    for i in range(3):
        if musicmodes[i] == musicmode:
            musicmode = musicmodes[(i-1+3)%3]
            break

def handleMouseUp(evt,mx,my):
    #handle MOUSEBUTTONUP event. permanently completes the drawing actions, depending on the mode.
    global drawwidth,importimg, imgrect, imgmoving, imgresize, mode
    
    if not imgrect.collidepoint(mx,my) and hypot(abs(evt.pos[0]-imgrect[0]-imgrect[2]), abs(evt.pos[1]-imgrect[1]-imgrect[3])) > 5:
        if imgmoving == 1:
            imgmoving = 0
    
    if action: #check if there is canvas action, if so draw according to the mode
        left, top = min(startx,mx),min(starty,my)
        rwidth, rheight = abs(mx-startx),abs(my-starty)

        if modes[mode] == "pencil":
            global pencilcircles
            brush(pencilcircles,1,c("black"))
            pencilcircles = []
            
        elif modes[mode] == "eraser":
            global erasercircles
            brush(erasercircles,drawwidth,c("white"))
            erasercircles = []
            
        elif modes[mode] == "brush":
            global brushcircles
            brush(brushcircles,drawwidth,chosencolour)
            brushcircles = []

        elif modes[mode] == "spraypaint":
            global spraylist, spraycirclelist
            for px,py in spraylist:
                screen.set_at((px,py),chosencolour)
            spraylist = []
            spraycirclelist = []

        elif modes[mode] == "highlight":
            global highlightlist, alphasf
            for x,y in highlightlist:
                    draw.circle(alphasf, (chosencolour[0], chosencolour[1], chosencolour[2], 100), (x-475,y-25), drawwidth)
            screen.blit(alphasf, (475, 25))
            highlightlist = []
            alphasf = Surface((700,450),SRCALPHA)

        elif modes[mode] == "fill bucket":
            global startcolour
            startcolour = screen.get_at((mx,my))
            if startcolour != chosencolour:
                floodfill(mx,my)

        elif modes[mode] == "line":
            drawline(startx,starty,mx,my)
            
        elif modes[mode] == "rect":
            draw.rect(screen, chosencolour, (left,top,rwidth,rheight))
            
        elif modes[mode] == "ellipse":
            draw.ellipse(screen, chosencolour, (left,top,rwidth,rheight))

        elif modes[mode] == "unfilled rect":
            draw.rect(screen,chosencolour,(left,top,rwidth,drawwidth))
            draw.rect(screen,chosencolour,(left,top,drawwidth,rheight))
            draw.rect(screen,chosencolour,(left+rwidth-drawwidth,top,drawwidth,rheight))
            draw.rect(screen,chosencolour,(left,top+rheight-drawwidth,rwidth,drawwidth))

        elif modes[mode] == "unfilled ellipse":
            #drawing 3 overlapping ellipses makes the ellipse border look more filled
            for i in range(-1,2):
                    try:
                        draw.ellipse(screen, chosencolour, (left-i,top-i,rwidth+2*i,rheight+2*i) ,min(drawwidth,min(rwidth,rheight)//2))
                    except:pass
                    
        #capture to make changes permanent
        capture()
        
    elif modes[mode] == "clear screen": #outside of "if action" because there doesnt need to be canvas action, only button
        draw.rect(screen, c("white"), canvas)
        capture()

    #similarly with importing/exporting images, and undo/redo
    elif buttons[6].rect.collidepoint(evt.pos): 
        try:
            importimg = image.load(filedialog.askopenfilename(initialdir="./images")) 
            importimg.convert()
            global ogimportimg
            ogimportimg = importimg.copy() #this is an important step. keep a copy of the original image, and each time perform a transformation on the original copy, not a transformed copy. this perserves image quality significantly
            imgrect = importimg.get_rect()
            imgrect.center = 825, 250
            screen.blit(importimg,(imgrect))
            
        except Exception as e:
            print(e)

    elif modes[mode] == "export":
        global saved
        try:
            fname=filedialog.asksaveasfilename(defaultextension=".png",initialdir="./saved images/")
            image.save(screen.subsurface(canvas),fname)
            saved = 1
        except Exception as e:
            print(e)

    elif modes[mode] == "undo":
        handleUndo()

    elif modes[mode] == "redo":
        handleRedo()
        

def handleKeydown(evt):
    #handle keydown event. text input recieved help from https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame
    global text, imglist, mode
    if evt.key == K_TAB:
        mode += 1
        mode %= len(modes)
    elif modes[mode] == "searching":
        if evt.key == K_BACKSPACE:
            text = text[:-1]
        elif evt.key == K_RETURN:
            handleDownload()
        else:
            text += evt.unicode
    else:
        #call different functions depending on key press
        if evt.key == K_u:
            handleUndo()
        elif evt.key == K_r:
            handleRedo()
        elif evt.key == K_SPACE:
            togglePlay()
        elif evt.key == K_PAGEDOWN:
            handleMusicNext()
        elif evt.key == K_PAGEUP:
            handleMusicPrevious()
        elif evt.key == K_RIGHT:
            nextMusicMode()
        elif evt.key == K_LEFT:
            prevMusicMode()

def showaction(mb,mx,my):
    #show temporarily what the user is doing (depending on the mode)
    if action:
        if mb[0]: #only left clicks
            left, top = min(startx,mx),min(starty,my)
            rwidth, rheight = abs(mx-startx),abs(my-starty)
            
            if modes[mode] == "pencil":
                global pencilcircles
                pencilcircles = addstroke(mx,my, pencilcircles)
                brush(pencilcircles,1, c("black"))
                
            elif modes[mode] == "eraser":
                global erasercircles
                erasercircles  = addstroke(mx,my, erasercircles)
                brush(erasercircles,drawwidth, c("white"))
                
            elif modes[mode] == "brush":
                global brushcircles
                brushcircles = addstroke(mx,my,brushcircles)
                brush(brushcircles,drawwidth,chosencolour)

            elif modes[mode] == "spraypaint":
                global spraylist, spraycirclelist
                l = len(spraycirclelist)
                spraycirclelist = addstroke(mx, my, spraycirclelist)
                for x,y in spraycirclelist[l:]:
                    tempspraypoints = randpoints(x,y)
                    spraylist += tempspraypoints
                for px,py in spraylist:
                    screen.set_at((px,py),chosencolour)
                    #draw.circle(screen, chosencolour, (px,py), 0.5)

            elif modes[mode] == "highlight":
                global highlightlist, alphasf
                highlightlist = addstroke(mx,my, highlightlist)
                for x,y in highlightlist:
                    draw.circle(alphasf, (chosencolour[0], chosencolour[1], chosencolour[2], 100), (x-475,y-25), drawwidth)
                screen.blit(alphasf, (475, 25))

            elif modes[mode] == "line":
                drawline(startx,starty,mx,my)

            elif modes[mode] == "rect":
                draw.rect(screen, chosencolour, (left,top,rwidth,rheight))
                
            elif modes[mode] == "ellipse":
                draw.ellipse(screen, chosencolour, (left,top,rwidth,rheight))

            elif modes[mode] == "unfilled rect":
                draw.rect(screen,chosencolour,(left,top,rwidth,drawwidth))
                draw.rect(screen,chosencolour,(left,top,drawwidth,rheight))
                draw.rect(screen,chosencolour,(left+rwidth-drawwidth,top,drawwidth,rheight))
                draw.rect(screen,chosencolour,(left,top+rheight-drawwidth,rwidth,drawwidth))

            elif modes[mode] == "unfilled ellipse":
                for i in range(-1,2):
                    try:
                        draw.ellipse(screen, chosencolour, (left-i,top-i,rwidth+2*i,rheight+2*i) ,min(drawwidth,min(rwidth,rheight)//2))
                    except:pass

    #resizing and moving images
    if modes[mode] == "import":
        global importimg, imgrect
        if imgresize == 1: #if they are currently resizing, perform transformation
            importimg = transform.scale(ogimportimg, (max(0,mx-imgrect[0]), max(0,my-imgrect[1])))
            imgrect = Rect(imgrect[0],imgrect[1], max(0,mx-imgrect[0]), max(0,my-imgrect[1]))
        draw.rect(screen, c("black"), imgrect, 3)
        screen.blit(importimg,imgrect)
        draw.circle(screen,c("green"), (imgrect[0]+imgrect[2],imgrect[1]+imgrect[3]), 5)
        draw.circle(screen,c("black"), (imgrect[0]+imgrect[2],imgrect[1]+imgrect[3]), 5, 1)

    #canvas border to look nice
    draw.rect(screen,c("black"),canvas,2)

    
# drawing functions #

def brush(circlelist, width, col):
    #draw all the circles within a circle list
    for x,y in circlelist:
        draw.circle(screen, col, (x,y), width)

def addstroke(mx,my,circlelist):
    #take the previous captured point, and fill the gap with circles
    if circlelist != []:
        px,py = circlelist[-1]
        xdiff = mx-px
        ydiff = my-py
        length = max(abs(xdiff),abs(ydiff))
        if length>0:
            #calculate how long each interval should be
            xinterval = xdiff/length
            yinterval = ydiff/length
            for j in range(length):
                #append circles at each interval
                x,y = int(px+j*xinterval), int(py+j*yinterval)
                circlelist.append((x,y))
        return circlelist
    else:
        return [(mx,my)]

def drawline(sx,sy,mx,my):
    #draw circles to form a line from start to end
    clis = addstroke(mx,my,[(sx,sy)])
    for x,y in clis:
        draw.circle(screen, chosencolour, (x,y), drawwidth//2)

def randpoints(x,y):
    #let drawwidth be radius, generate random points within an area (spraypaint)
    global spraylist
    pointslis = []
    xmin,xmax = x-drawwidth, x+drawwidth
    ymin,ymax = y-drawwidth, y+drawwidth
    while len(pointslis) <drawwidth//1.5: #scale according to drawwidth, make sure to have a certain amount of points before breaking
        px, py = randint(xmin, xmax), randint(ymin, ymax)
        if hypot(abs(px-x),abs(py-y)) <= drawwidth: #add to pointslis if within circle
            pointslis.append((px,py))
    return pointslis

from collections import deque #deques have efficient pop and append
#using dfs is the most efficient compared to bfs or recursion dfs, because a queue stack is much smaller in memory than a recursion call or a bfs queue (our graph is very wide)
def floodfill(sx,sy):
    #paintbucket fill using dfs
    global startcolour, chosencolour
    d = deque()
    d.append((sx,sy))
    while d:
        x,y = d.pop()
        screen.set_at((x,y),chosencolour) #set current pixel to chosencolour
        for a,b in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]: #check in each direction
            if screen.get_at((a,b)) == startcolour: #if it is the same colour as we started
                if 475<=a<1175 and 25<=b<475: #if it is within the canvas
                    d.append((a,b)) #add to deque
        
def drawSearched():
    #draw searched images
    draw.rect(screen, c("white"), imgsearch)
    draw.rect(screen, c("blue"), searchbtn)
    screen.blit(searchicon, (200+searchbarx, searchbary))

    if text != '': #only render font if it exists
        searchinput = searchfont.render(text, True, c("black"))
        screen.blit(searchinput, (searchbarx+10,searchbarx+15))

    if modes[mode] == "searching":
        draw.rect(screen, c("red"), imgsearch,3)
    else:
        draw.rect(screen, c("black"), imgsearch,3)

    #bliting searched images
    for i in range(len(imglist)):
        screen.blit(imglist[i], (searchbarx,searchbarx+i*140+65))

def handleDownload():
    #handle image downloading, see image_downloader_modified.py for specific info
    global text, mode, imglist, stamprects
    imglist = []
    stamprects = []
    if text != '':
        download_images(text,4) #download images, using the imported function from the other file
        directory = "images/"+text+"/"
        ld = listdir(directory)
        for i in range(len(ld)):
            try:
                timg = image.load(directory+ld[i]) #load images
                x,y = timg.get_size()
                transformed = [int(120*x/y),120] #maintain ratio
                if transformed[0] > 250:
                    transformed[0] = 250
                timg = transform.scale(timg,transformed)
                imglist.append(timg) #add image to list of images
                stamprects.append(Rect(searchbarx,searchbarx+i*140+65,transformed[0],transformed[1])) #append to a list of rects that correspond to the images
            except Exception as e:
                print(e)
    else:
        imglist = originalimgs[:]
        stamprects = originalstamprects[:]
    mode = 0
    text = ""

def clearImageDownloads():
    #delete the images folder when the program exits
    try:shutil.rmtree("./images")
    except:pass

def arrowchangedrawwidth(kp):
    #changing drawwidth with up/down arrow keys
    global drawwidth
    if kp[K_UP]:
        drawwidth = min(drawwidth+1,40) #no more than 40 pixels wide
    if kp[K_DOWN]:
        drawwidth = max(drawwidth-1,1) #no less than 1 pixel wide

def drawButtons():
    #draw all the buttons
    global mode,playnextborder,playprevborder, borderframecount
    for b in buttons:
        draw.rect(screen, c("white"), b.rect)
        screen.blit(woodenbtn,b.rect)
        screen.blit(buttonimgs[b.mode-2],b.rect)
        if mode == b.mode:
            draw.rect(screen,c("red"), b.rect, 2)
    screen.blit(colours,cprect)
    draw.rect(screen, chosencolour, (400-drawwidth,435-drawwidth,drawwidth*2,drawwidth*2))
    draw.rect(screen,c("black"),cprect,2)
    draw.rect(screen,c("black"),(400-drawwidth,435-drawwidth,drawwidth*2,drawwidth*2),2)

    draw.rect(screen,c("white"),playerrect) #player
    draw.rect(screen,c("black"),playrect) #play
    draw.rect(screen,c("black"),prevrect) #previous
    draw.rect(screen,c("black"),nextrect) #next
    
    screen.blit(playerimg,playerrect)
    screen.blit(cur,playrect)
    screen.blit(previmg,prevrect)
    screen.blit(nextimg,nextrect)
    screen.blit(inorderimg,inorderrect)
    screen.blit(loopimg,looprect)
    screen.blit(shuffleimg,shufflerect)

    draw.rect(screen,c("black"),inorderrect,2)
    draw.rect(screen,c("black"),looprect,2)
    draw.rect(screen,c("black"),shufflerect,2)
    draw.rect(screen,c("black"),playerrect,2)
    draw.rect(screen,c("black"),prevrect,2)
    draw.rect(screen,c("black"),nextrect,2)

    if musicmode == "inorder":
        draw.rect(screen,c("red"),inorderrect,2)
    elif musicmode == "loop":
        draw.rect(screen,c("red"),looprect,2)
    elif musicmode == "shuffle":
        draw.rect(screen,c("red"),shufflerect,2)

    if playnextborder:
        if borderframecount != 0:
            draw.rect(screen,c("red"),nextrect,2)
            borderframecount -= 1
        else:
            playnextborder = 0
    if playprevborder:
        if borderframecount != 0:
            draw.rect(screen,c("red"),prevrect,2)
            borderframecount -= 1
        else:
            playprevborder = 0
        
def drawBG():
    #draw background
    screen.blit(woodbg,(0,0))
    screen.blit(bgdim1.surface,(searchbarx//2,25))
    screen.blit(bgdim2.surface,(350,25))
    screen.blit(bgdim3.surface,(475,500))

def showinfo(mx,my):
    #shows on the bottom right, info about the current tool, current colour, mouse position, and playing track

    #shows position relative to canvas
    left,top,width,height = canvas
    mx = mx-left
    my = my-top

    #make sure coordinates are not negative
    if mx < 0:
        mx = 0
    elif mx > left+width:
        mx = left+width
    
    if my < 0:
        my = 0
    elif my > top+height:
        my = top+height

    text = f'Current tool: {modes[mode]}    Current colour: {(chosencolour[0],chosencolour[1],chosencolour[2])}    Mouse position: {mx}, {my}    Current Song: {musicnames[cursong]}'
    text = infofont.render(text, True, c("white"))
    screen.blit(text, (1175-text.get_size()[0],682))

def blitcursor(mx,my):
    #show a different cursor depending on position
    if canvas.collidepoint(mx,my):
        mouse.set_visible(0)
        screen.blit(cursor,(mx-10//2,my-10//2))
    else:
        mouse.set_visible(1)

def handleQuit():
    #handle quit event
    if not saved: #if the user hasnt saved
        ans = messagebox.askyesnocancel(title=None, message="Save the canvas?") #ask the user if they want to save
        if ans == False:
            return False
        if ans == True: #if the answer is yes, commence saving process, then exit when done
            try:
                fname=filedialog.asksaveasfilename(defaultextension=".png",initialdir="./saved images/")
                image.save(screen.subsurface(canvas),fname)
                return False
            except:
                print("Failed to save, exit cancelled")
                return True
        return True
    else: #if the user already saved the canvas, just exit
        return False

def main():
    #main program loop
    running=True
    clock = time.Clock()
    while running:
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        kp = key.get_pressed()
        screen.set_clip()

        if not action: arrowchangedrawwidth(kp)
        
        ########################### event handling, calculations ###########################
        for evt in event.get():
            if evt.type == QUIT:
                running = handleQuit()
            if evt.type == MOUSEBUTTONDOWN: #mouse down event
                handleMousePress(evt)
                handleMusic(evt)
            if evt.type == MOUSEBUTTONUP: #button up event
                handleMouseUp(evt,mx,my)
            if evt.type == KEYDOWN: #keydown event
                handleKeydown(evt)
            if evt.type == MOUSEMOTION: #only used for image movement
                if imgmoving == 1:
                    imgrect.move_ip(evt.rel)
            if evt.type == MUSICEND: #self defined event: when the music finishes
                handleMusicNext()
        
        ########################### draw stuff ###########################

        
        #draw background rects
        drawBG()

        #search section
        drawSearched()

        #draw buttons
        drawButtons()

        #draw title
        screen.blit(title,(483,520))

        #show info
        showinfo(mx,my)
        
        #draw canvas
        screen.set_clip(Rect(canvas[0],canvas[1],canvas[2]+1,canvas[3]+1))
        screen.blit(screencap,(475,25))
        draw.rect(screen,c("black"),canvas,2)

        #show action
        showaction(mb,mx,my)

        #draw cursor
        blitcursor(mx,my)


        ########################### adjust framerate, update ###########################
        clock.tick(120) #control framerate
        display.flip()#update display

        screen.blit(screencap,(475,25)) #after showing action, erase what was shown in showaction() so that its temporary


########################### load images, define global variables ###########################

width,height=1200,700
screen=display.set_mode((width,height))
mode = 0
modes = [None, "searching", "pencil", "eraser", "brush", 'spraypaint', 'highlight', 'fill bucket', "line", 'rect', 'ellipse', 'unfilled rect', 'unfilled ellipse', 'clear screen', 'import', 'export', 'undo', 'redo']

saved = 0

#background image
woodbg = transform.scale(image.load("static/woodbg.jpg"),(width,height))
bgdim1 = bg((300,height-50))
bgdim2 = bg((100,650))
bgdim3 = bg((700,175))

#title
title = transform.scale(image.load("static/title.png"),(450,130))

#cursor
cursor = image.load("static/crosshair.png")
cursor = transform.scale(cursor,(10,10))

#buttons
buttons = [button(360,i*45+35,2*i+2) for i in range(8)]+[button(405,i*45+35,2*i+3) for i in range(8)]
selectedborder = Rect(0,0,0,0)

buttonimgs = [0 for i in range(16)]
for b in buttons:
    bm = b.mode-2
    buttonimgs[bm] = transform.scale(image.load(f"static/buttonspng/{bm}.png"),(35,35))
woodenbtn = transform.scale(image.load("static/wooden button.jpg"),(35,35))

#music player
playerrect = Rect(950,520,200,125)
playrect = Rect(1025,540,50,50)
prevrect = Rect(970,550,35,35)
nextrect = Rect(1095,550,35,35)

inorderrect = Rect(970,600,35,35)
looprect = Rect(1033,600,35,35)
shufflerect = Rect(1095,600,35,35)

playnextborder = 0
playprevborder = 0
borderframecount = 0

playerimg = transform.scale(image.load("static/musicplayer.png"),(200,125))
playimg = transform.scale(image.load("static/play.png"),(50,50))
pauseimg = transform.scale(image.load("static/pause.png"),(50,50))
previmg = transform.scale(image.load("static/previous.png"),(35,35))
nextimg = transform.scale(image.load("static/next.png"),(35,35))
cur = playimg

shuffleimg = transform.scale(image.load("static/shuffle.png"),(35,35))
loopimg = transform.scale(image.load("static/loop.png"),(35,35))
inorderimg = transform.scale(image.load("static/inorder.png"),(35,35))

musicmode = "inorder"
musicmodes = ["inorder","loop","shuffle"]
musicquant = len(listdir("static/music"))
musicfnames = [f"static/music/{i}.mp3" for i in range(musicquant)]
musicnames = ["Unnamed Track" for i in range(musicquant)]
musicnames[0]="Illusion of Inflict"
musicnames[1]="Croatian Rhapsody"
musicnames[2]="Again"
musicnames[3]="nc17"
musicnames[4]="seele"
musicnames[5]="Rainbow Main Theme"
musicnames[6]="Guns and Roses"
mixer.music.load(musicfnames[0])
prevsong = 6
cursong = 0
nextsong = 1
mixer.music.play(0)
mixer.music.pause()
#https://stackoverflow.com/questions/58630700/utilising-the-pygame-mixer-music-get-endevent
MUSICEND = USEREVENT+1
mixer.music.set_endevent(MUSICEND)


#tools util lists
drawwidth = 10
brushcircles = []
pencilcircles = []
erasercircles = []
spraylist = []
spraycirclelist = []
highlightlist = []
alphasf = Surface((700,450),SRCALPHA)

startcolour = (255,255,255)


#import img variables
if not path.exists("./images"):
    makedirs("./images")
imgmoving = 0
imgresize = 0
imgrect = Rect(0,0,0,0)
importimg = Surface((0,0))

#colour picker
colours = image.load("static/colourpicker.jpg")
cix,ciy = colours.get_size()
ch = 180
colours = transform.scale(colours, (80,ch))
cprect = Rect(360,485,80,ch)
chosencolrect = Rect(360,395,80,80)
chosencolour = c("white")

#canvas
undo = []
redo = []

canvas = Rect(475,25,700,450)
draw.rect(screen,(255,255,255),canvas)
capture()


#searchbar
searchbarx,searchbary = 50,50
imgsearch = Rect(searchbarx, searchbary, 200, 50)
searchbtn = Rect(200+searchbarx, searchbary, 50, 50)
text = ''
searchfont = font.SysFont("Calibri", 24)
infofont = font.SysFont("Calibri",12)
stamping = 0
stampimg = Surface((0,0))
searchicon = transform.scale(image.load("static/buttons/searchicon.png"),(50,50))

imglist = []
stamprects = []
originalimgs = []

#preload images
for i in range(4):
    timg = image.load(f"static/preloaded imgs/{i}.png")
    x,y = timg.get_size()
    transformed = [int(120*x/y),120] #maintain ratio
    if transformed[0] > 250:
        transformed[0] = 250
    timg = transform.scale(timg,transformed)
    imglist.append(timg)
    stamprects.append(Rect(searchbarx,searchbarx+i*140+65,transformed[0],transformed[1]))
originalimgs = imglist[:]
originalstamprects = stamprects[:]

########################### call functions ###########################

main()

clearImageDownloads()

quit()
