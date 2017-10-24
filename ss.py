#!/usr/bin/env python

import gtk, random, gobject
import gtk as Gtk
from time import sleep
import time
import re
import os
import pickle
import argparse
import pango

#######################################################
class Line():
#######################################################
    def __init__(self, x1, y1, x2, y2, size):
        self.fx1 = x1 / (size - 1.0)
        self.fx2 = x2 / (size - 1.0)
        self.fy1 = y1 / (size - 1.0)
        self.fy2 = y2 / (size - 1.0) 
        self.ix1 = x1
        self.ix2 = x2
        self.iy1 = y1
        self.iy2 = y2
        self.state = False
        
    

#######################################################
class BinaryLines():
#######################################################

    ################################################
    def __init__(self):
    ################################################
        self.initialized = False
        self.size = 0
        self.lines = []
        self.max_state = 1
        self.state = 0 
        self.r = 0
        self.g = 0
        self.b = 0
        self.lr = 0
        self.lg = 0
        self.lb = 0
    ################################################
    def read_file(self, filename):
    ################################################
        self.__init__()
        f = open(filename, 'r')
        self = pickle.load(f)
       
    ################################################
    def initialize(self, size):
    ################################################
        self.__init__()
        self.size = size
        for x1 in range(size):
            for x2 in range(size):
                for y1 in range(size):
                    for y2 in range(size):
#                        print("start of loop:")
#                        for i in range( len (self.lines)):
#                            l = self.lines[i]
#                            print(" (%d,%d)-(%d,%d) " % (l.ix1, l.iy1, l.ix2, l.iy2))
                        
                        # skip lines where the 2nd end is higher than the first end
                        if ( y2 < y1):
                            print ("skipping (%d, %d) to (%d %d) y2 < y1" % (x1, y1, x2, y2))
                            continue
                        
                        # skip horizontal lines where the 2nd end is to the left of the first end
                        if ( ( y2 == y1 ) and ( x2 < x1) )  :
                            print ("skipping (%d, %d) to (%d %d) y2==y1 & x2 < x1" % (x1, y1, x2, y2))
                            continue
                        
                        # skip lines that cross over one of the points
                        if ( abs( x1 - x2 ) > 1 and abs( y1 - y2) > 1 ):
                            if ( ( ( x1 - x2 ) % ( y1 - y2 ) ) == 0 ):
                                print (" (%d, %d) to (%d %d) x mod y = 0" % (x1, y1, x2, y2) )
                                if ( abs( (x1 - x2) / (y1-y2) )  <= abs(x1-x2) ):
                                    print ("skipping (%d, %d) to (%d %d) y mod x" % (x1, y1, x2, y2) )
                                    continue
                            if ( ( ( y1 - y2 ) % ( x1 - x2 ) ) == 0 ):
                                print (" (%d, %d) to (%d %d) y mod x = 0" % (x1, y1, x2, y2) )
                                if( abs( ( y1 - y2 ) / ( x1 - x2) <= abs(y1-y2) ) ) :
                                    print ("skipping (%d, %d) to (%d %d) x mod y" % (x1, y1, x2, y2) )
                                    continue
                                
                        # skip horizontal lines that cross over one of the points
                        if ( y1 == y2 and abs( x1-x2 ) > 1):
                            print ("skipping (%d, %d) to (%d %d) horz x point" % (x1, y1, x2, y2) )
                            continue
                        
                        # skip vertical lines that cross over one of the points
                        if( x1 == x2 and abs( y1 - y2 ) > 1):
                            print ("skipping (%d, %d) to (%d %d) vert x point" % (x1, y1, x2, y2) )
                            continue
                            
                            
                        self.lines.append(Line(x1,y1,x2,y2,size))
                        self.max_state = self.max_state + 1
                        print ("adding state %d (%d, %d) to (%d %d)" % (self.max_state, x1, y1, x2, y2))
                        
        print "Done initializing:"        
        for i in range( len (self.lines)):
            l = self.lines[i]
            print(" (%d,%d)-(%d,%d) " % (l.ix1, l.iy1, l.ix2, l.iy2))
    ################################################
    def set_state(self,new_state):
    ################################################
        self.state = new_state
        self.statestring = ""
        for l in range( len( binaryLines.lines ) ):
            if ( new_state & (1 << l) ):
                binaryLines.lines[l].state = True
                self.statestring = '1' + self.statestring 
            else:
                binaryLines.lines[l].state = False
                self.statestring = '0' + self.statestring 
        print ("current state: %d (%s)" % (self.state, self.statestring))
                            
    ################################################
    def increment_state(self):
    ################################################
        self.state = self.state + 1
        if self.increment_bit(0):
            self.initialize( self.size + 1)
        self.statestring = ""
        for l in range( len( binaryLines.lines ) ):
            if binaryLines.lines[l].state:
                self.statestring = '1' + self.statestring 
            else:
                self.statestring = '0' + self.statestring 
        print ("current state: %d (%s)" % (self.state, self.statestring))
        
    ################################################
    def dump(self):
    ################################################
        for l in range( len( binaryLines.lines ) ):
            ls = binaryLines.lines[l]
            print ("%d:(%d %d) - (%d %d):%d" % (l, ls.ix1, ls.iy1, ls.ix2, ls.iy2, ls.state))
    ################################################
    def dump_file(self, filename):
    ################################################
        f = open(filename, 'w')
        pickle.dump( self, f)
        
    ################################################
    def dump_file_old(self, filename):
    ################################################
        f = open(filename, 'w')
        f.write("size: %d\n" %(self.size))
        f.write("state: %d\n" %(self.size))
        for l in range( len( binaryLines.lines ) ):
            ls = binaryLines.lines[l]
            f.write("line: %d:(%d %d) - (%d %d):%d\n" % (l, ls.ix1, ls.iy1, ls.ix2, ls.iy2, ls.state))
        f.close()
        
        
        
    ################################################
    def increment_bit(self, bit):
    ################################################
        # print( "incrementing bit %d" % bit)
        if bit >= len( self.lines ):
            return True
        else:
            if self.lines[ bit ].state:
                self.lines[ bit ].state = False
                if self.increment_bit( bit + 1):
                    return True
            else:
                self.lines[ bit ].state = True
        return False
        
    ################################################
    def check_skipstate(self):
    ################################################
        # check for dots at the end of lines
        x_min = 10000
        x_max = 0
        y_min = 10000
        y_max = 0
        
        for l in range( len( binaryLines.lines ) ):
            ls = self.lines[l]
            if self.lines[l].state == 0:
                continue
            if ( ls.ix1 == ls.ix2 and ls.iy1 == ls.iy2 ) :
                for l2 in range( len (binaryLines.lines ) ):
                    ls2 = self.lines[l2]
                    # print("checking (%d %d)-(%d %d) and (%d %d)-(%d %d)" % (ls.ix1, ls.iy1, ls.ix2, ls.iy2, ls2.ix1, ls2.iy1, ls2.ix2, ls2.iy2))
                    if self.lines[l2].state == 0:
                        # print "  its off"
                        continue 
                    if ( (ls2.ix1 == ls2.ix2) and (ls2.iy1 == ls2.iy2)):
                        # it's a dot 
                        # print "  its a dot"
                        continue
                    if( (ls.ix1 == ls2.ix1) and (ls.iy1 == ls2.iy1) ):
                        # print("skipping dot (%d %d) line (%d %d)-(%d %d)" % (ls.ix1, ls.iy1, ls2.ix1, ls2.iy1, ls2.ix2, ls2.iy2))
                        return True
                    if( (ls.ix1 == ls2.ix2) and (ls.iy1 == ls2.iy2)):
                        # print("skipping dot (%d %d) line (%d %d)-(%d %d)" % (ls.ix1, ls.iy1, ls2.ix1, ls2.iy1, ls2.ix2, ls2.iy2))
                        return True
            if ls.ix1 > x_max:
                x_max = ls.ix1
            if ls.ix2 > x_max:
                x_max = ls.ix2
            if ls.ix1 < x_min:
                x_min = ls.ix1
            if ls.ix1 < x_min:
                x_min = ls.ix2
                
            if ls.iy1 > y_max:
                y_max = ls.iy1
            if ls.iy2 > y_max:
                y_max = ls.iy2
            if ls.iy1 < y_min:
                y_min = ls.iy1
            if ls.iy1 < y_min:
                y_min = ls.iy2
                
        if x_max - x_min < self.size - 1 and y_max - y_min < self.size - 1:
            print ("skipping - smaller subset x:(%d-%d) y(%d-%d) size:%d" % (x_min, x_max, y_min, y_max, self.size))
            return True
        return False
                
                    
    
        
            
                        

# This function will be called whenever you click on the button:
def click_handler(a, b) :
    # quit the application:
    import os
    home = os.getenv('USERPROFILE') or os.getenv('HOME')
    binaryLines.dump_file(home + "/.binarylines")
    gtk.main_quit()

def clip(i, min, max) :
    if i < min :
        return min
    if i > max :
        return max
    return i

# Global variables used by the expose and idle handlers:
xgc = None
x1 = None
x2 = None
y1 = None
y2 = None
movesize = 20
colorjump = 1 
w = 0
h = 0
scale = 0.0
scale0 = 0.0
sizedir = -1
sizedir0 = 0
sizedir1 = 0
scalestep = 0.1
import random

def idle_handler(widget) :
    global xgc, x1, x2, y1, y2, movesize, colorjump
    global binaryLines
    global then
    global w, h, scale0, w0, h0, w_min, h_min, sizedir, sizedir0, sizedir1, scale, scalestep, xdir
    
    if time.time() - then < 1:
        sleep( 0.1)
        return True
    then = time.time()

    if (xgc == None) :
        xgc = widget.window.new_gc()
    w, h = widget.window.get_size()
    if (scale == 0) :
        w0 = 0
        h0 = 0
        sizedir0 = random.randint(0,1)
        sizedir1 = random.randint(0,1)
        scale = 1
    scale = scale + scalestep * sizedir
    scale0 = 0.05 + (1-scale) * sizedir0
    scale1 = 0.05 + (1-scale) * sizedir1

    if scale < 0.5 :
        sizedir = 1
        scale = 0.5
    if scale > 1 :
        sizedir0 = random.uniform(0,1)
        sizedir1 = random.uniform(0,1)
        scalestep = random.uniform(0.0001,0.001)
        sizedir = -1
        scale = 1
        w0 = 0
        h0 = 0


    binaryLines.r = binaryLines.r + colorjump
    if binaryLines.r > 65535 - colorjump:
        binaryLines.r = 0
        binaryLines.g = binaryLines.g + colorjump
    if binaryLines.g > 65535 - colorjump:
        binaryLines.b = binaryLines.b + colorjump
    if binaryLines.b > 65535 - colorjump :
        binaryLines.r = 0
        binaryLines.g = 0
        binaryLines.b = 0
    xgc.set_rgb_fg_color(gtk.gdk.Color(binaryLines.r, binaryLines.g, binaryLines.b))
    widget.window.draw_rectangle(xgc, True, 0, 0, w, h)
    while binaryLines.check_skipstate():
        print("skipping state %d" % binaryLines.state)
        binaryLines.increment_state()
    cj2 = 100
    
        
    for l in range( len( binaryLines.lines ) ):
        if (binaryLines.lines[l].state):
            x1 = int(0.9 * binaryLines.lines[l].fx1 * w * scale + w * scale1)
            x2 = int(0.9 * binaryLines.lines[l].fx2 * w * scale + w * scale1)
            y1 = int(0.9 * binaryLines.lines[l].fy1 * h * scale + h * scale0)
            y2 = int(0.9 * binaryLines.lines[l].fy2 * h * scale + h * scale0)

            # Change the color a little bit:
            if binaryLines.b > 32000:
                xgc.set_rgb_fg_color(gtk.gdk.Color(binaryLines.lr, binaryLines.lg, binaryLines.lb))
            else:
                xgc.set_rgb_fg_color(gtk.gdk.Color(65535 - binaryLines.lr, 65535-binaryLines.lg, 65535-binaryLines.lb))
            xgc.set_line_attributes( int( h / 100) , gtk.gdk.LINE_SOLID, gtk.gdk.CAP_ROUND, gtk.gdk.JOIN_ROUND)
            
            binaryLines.lr = binaryLines.lr + cj2
            if binaryLines.lr > 65535 - cj2:
                binaryLines.lr = 0
                binaryLines.lg = binaryLines.lg + cj2
            if binaryLines.lg > 65535 - cj2:
                binaryLines.lg = 0
                binaryLines.lb = binaryLines.lb + cj2
            if binaryLines.lb > 65535 - cj2 :
                binaryLines.lr = 0
                binaryLines.lg = 0
                binaryLines.lb = 0

            # Draw the new line
            if (x1 == x2 and y1 == y2):
                print("drawing dot  (%d, %d) to (%d, %d) (DOT)" % (binaryLines.lines[l].ix1,binaryLines.lines[l].iy1,binaryLines.lines[l].ix2,binaryLines.lines[l].iy2))
            else:
                print("drawing line (%d, %d) to (%d, %d)" % (binaryLines.lines[l].ix1,binaryLines.lines[l].iy1,binaryLines.lines[l].ix2,binaryLines.lines[l].iy2))
            widget.window.draw_line(xgc, x1, y1, x2, y2)
            pangolayout = widget.create_pango_layout("")
            pangolayout.set_text(binaryLines.statestring)
            print("w:%d h:%d scale0:%d" % (w, h, scale0) )
            widget.window.draw_layout( xgc, int(w*scale0/2), int(h*scale0/2), pangolayout)


    # Return True so we'll be called again:
    # sleep(4)
    print("line color (%d %d %d)" % (binaryLines.lr, binaryLines.lg, binaryLines.lb))
    print("w:%d h:%d scalestep:%0.5f scale0:%0.3f scale:%0.3f sizedir:%d sizedir0:%0.3f \n" % (w,h,scalestep,scale0,scale,sizedir,sizedir0))
    binaryLines.increment_state()
    return True

#################################################################################
def read_args():
#################################################################################
    parser = argparse.ArgumentParser(description='a binary line screen saver')
    parser.add_argument("--win", action='store_true', help="Run in windowed mode")
    parser.add_argument("--restart ", dest='size', type=int, help="Restart the map from scratch")
    parser.add_argument("--init", dest='state', type=int, help="Start from a given state (must be used with restart and a size)")
    return parser.parse_args()
#################################################################################
#################################################################################
## main
#################################################################################
#################################################################################


# create the data object
binaryLines = BinaryLines()
args = read_args()
if args.size == None :
    home = os.getenv('USERPROFILE') or os.getenv('HOME')
    try:
        f = open(home + "/.binarylines", 'r')
        binaryLines = pickle.load(f)
    except (EOFError, IOError):
        print "could not open file, using init"
        binaryLines.initialize(2)
    binaryLines.dump()
else:
    print("INITIALIZING")
    binaryLines.initialize( args.size )
    if args.state != None:
        binaryLines.set_state( args.state )

### init stuff ####
then = 0

# Create the main window:
win = gtk.Window()

# Organize widgets in a vertical box:
vbox = gtk.VBox()
win.add(vbox)

# Create an area to draw in:
drawing_area = gtk.DrawingArea()
drawing_area.set_size_request(300, 300)
drawing_area.add_events(Gtk.gdk.BUTTON_PRESS_MASK) 
drawing_area.connect('button-press-event', click_handler)
vbox.pack_start(drawing_area)

# set our drawing function
idle_id = gobject.idle_add(idle_handler, drawing_area)

drawing_area.show()

# Make a pushbutton:
# button = gtk.Button("Quit")

# When it's clicked, call our handler:
#button.connect("clicked", click_handler)

# Obey the window manager quit signal:
win.connect("destroy", gtk.main_quit)

vbox.show()
win.show_all()
if args.win == False:
    win.window.fullscreen()


gtk.main()


