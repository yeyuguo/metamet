#!/usr/bin/env python

# This code is found from http://kitchingroup.cheme.cmu.edu/software/python/matplotlib/interactive-data-browsing-in-matplotlib
# The original description including the possible author is as following:
# Here is another example of how to interact with data in graphs. I think this script came from John Hunter (matplotlib author). Note in this script that you can navigate through your data with key presses (n=next, p=previous) or by clicking on points. Each time you select a point, a new graph pops up containing some data that was used to derive the point. You could just as well use system calls to pop up a structure viewer, or print data to the command line.

import numpy as np
import matplotlib.pyplot as plt
import sys

class PointBrowser:
    def __init__(self,xs,ys):

        self.xs = np.array(xs)
        self.ys = np.array(ys)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.line, = self.ax.plot(self.xs,self.ys,'ro ', picker=5)

        self.lastind = 0

        self.text = self.ax.text(0.05, 0.95, 'Datapoint index selected: none',
                            transform=self.ax.transAxes, va='top')

        self.selected,  = self.ax.plot([self.xs[0]],
                                       [self.ys[0]], 'o', ms=12, alpha=0.4,
                                       color='yellow', visible=False)


        self.fig.canvas.mpl_connect('pick_event', self.onpick)
        self.fig.canvas.mpl_connect('key_press_event', self.onpress)



    def onpress(self, event):
        'define some key press events'
        if self.lastind is None: return

        if event.key in ('q','Q'): sys.exit()

        if event.key not in ('n', 'p'): return
        if event.key=='n': inc = 1
        else:  inc = -1


        self.lastind += inc
        self.lastind = clip(self.lastind, 0, len(self.xs)-1)
        self.update()

    def onpick(self, event):

        if event.artist!=self.line: return True

        N = len(event.ind)
        if not N: return True

        if N > 1:
            print '%i points found!' % N


        # the click locations
        x = event.mouseevent.xdata
        y = event.mouseevent.ydata

        dx = np.array(x-self.xs[event.ind],dtype=float)
        dy = np.array(y-self.ys[event.ind],dtype=float)

        distances = np.hypot(dx,dy)
        indmin = distances.argmin()
        dataind = event.ind[indmin]

        self.lastind = dataind
        self.update()

    def update(self):
        if self.lastind is None: return

        dataind = self.lastind

        self.selected.set_visible(True)
        self.selected.set_data(self.xs[dataind], self.ys[dataind])

        self.text.set_text('datapoint index selected: %d'%dataind)

        # put a user function in here!        
        self.userfunc(dataind)

        self.fig.canvas.draw()


    def userfunc(self,dataind):
#        print dataind
        pass


if __name__ == '__main__':


    X = np.random.rand(100, 200)
    xs = np.mean(X, axis=1)
    ys = np.std(X, axis=1)


    p = PointBrowser(xs,ys)

    def plot2(dataind):
        fig2 = plt.figure(2)
        ax2 = fig2.add_subplot(111)

        ax2.cla()
        ax2.plot(X[dataind])

        ax2.text(0.05, 0.9, 'mu=%1.3f\nsigma=%1.3f'%(xs[dataind], ys[dataind]),
                 transform=ax2.transAxes, va='top')
        ax2.set_ylim(-0.5, 1.5)

        fig2.canvas.draw()
    def printer(dataind):
        print dataind

#    p.userfunc = plot2
#    p.userfunc = printer

    plt.xlabel('$\mu$')
    plt.ylabel('$\sigma$')

    plt.show()
