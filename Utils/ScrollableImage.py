import tkinter
import sys

# The entirety of this code is copied from the first answer in: https://stackoverflow.com/questions/56043767/show-large-image-using-scrollbar-in-python
class ScrollableImage(tkinter.Frame):
    def __init__(self, master=None, mapClickCallback=None, **kw):
        self.image = kw.pop('image', None)
        sw = kw.pop('scrollbarwidth', 10)
        super(ScrollableImage, self).__init__(master=master, **kw)
        self.cnvs = tkinter.Canvas(self, highlightthickness=0, **kw)
        self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
        # Vertical and Horizontal scrollbars
        self.v_scroll = tkinter.Scrollbar(self, orient='vertical', width=sw)
        self.h_scroll = tkinter.Scrollbar(self, orient='horizontal', width=sw)
        # Grid and configure weight.
        self.cnvs.grid(row=0, column=0,  sticky='nsew')
        self.h_scroll.grid(row=1, column=0, sticky='ew')
        self.v_scroll.grid(row=0, column=1, sticky='ns')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Set the scrollbars to the canvas
        self.cnvs.config(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        # Set canvas view to the scrollbars
        self.v_scroll.config(command=self.cnvs.yview)
        self.h_scroll.config(command=self.cnvs.xview)
        # Assign the region to be scrolled 
        self.cnvs.config(scrollregion=self.cnvs.bbox('all'))
        self.mapClickCallback = mapClickCallback
        self.cnvs.bind_class(self.cnvs, "<MouseWheel>", self.mouse_scroll)
        self.cnvs.bind_class(self.cnvs, "<Button-1>", self.print_location)

    def print_location(self, event):
        scrollBarLeft = self.h_scroll.get()[0]
        scrollBarRight = self.h_scroll.get()[1]
        maxOffsetX = self.image.width() - self.cnvs.winfo_width()
        offsetScalarX = scrollBarLeft / (1 - (scrollBarRight - scrollBarLeft))
        x = event.x + (maxOffsetX * offsetScalarX)
        
        scrollBarTop = self.v_scroll.get()[0]
        scrollBarBottom = self.v_scroll.get()[1]
        maxOffsetY = self.image.height() - self.cnvs.winfo_height()
        offsetScalarY = scrollBarTop / (1 - (scrollBarBottom - scrollBarTop))
        y = event.y + (maxOffsetY * offsetScalarY)

        self.mapClickCallback(x, y)

    def mouse_scroll(self, evt):
        self.cnvs.yview_scroll(-1*(evt.delta) // 65, 'units')