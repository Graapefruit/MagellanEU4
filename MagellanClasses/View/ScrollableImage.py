import tkinter

SCROLL_WHEEL_WIDTH = 16

# This code is copied (and modified as was needed) from the first answer in: https://stackoverflow.com/questions/56043767/show-large-image-using-scrollbar-in-python
class ScrollableImage(tkinter.Frame):
    def __init__(self, master=None, **kw):
        super(ScrollableImage, self).__init__(master=master, **kw)
        self.cnvs = tkinter.Canvas(self, highlightthickness=0, **kw)
        self.onLeftClick = self.doNothing
        self.onRightClick = self.doNothing
        self.v_scroll = tkinter.Scrollbar(self, width=SCROLL_WHEEL_WIDTH, orient='vertical')
        self.h_scroll = tkinter.Scrollbar(self, width=SCROLL_WHEEL_WIDTH, orient='horizontal')
        self.cnvs.bind_class(self.cnvs, "<MouseWheel>", self.mouseScroll)
        self.cnvs.bind_class(self.cnvs, "<Button-1>", (lambda event : self.onLeftClick(self.getPixelCoordinateX(event.x), self.getPixelCoordinateY(event.y))))
        self.cnvs.bind_class(self.cnvs, "<Button-3>", (lambda event : self.onRightClick(self.getPixelCoordinateX(event.x), self.getPixelCoordinateY(event.y))))

    def updateImage(self, newImage):
        self.image = newImage
        self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
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

    def getPixelCoordinateX(self, x):
        scrollBarLeft = self.h_scroll.get()[0]
        scrollBarRight = self.h_scroll.get()[1]
        maxOffsetX = self.image.width() - self.cnvs.winfo_width()
        offsetScalarX = scrollBarLeft / (1 - (scrollBarRight - scrollBarLeft))
        return x + round(maxOffsetX * offsetScalarX)

    def getPixelCoordinateY(self, y):
        scrollBarTop = self.v_scroll.get()[0]
        scrollBarBottom = self.v_scroll.get()[1]
        maxOffsetY = self.image.height() - self.cnvs.winfo_height()
        offsetScalarY = scrollBarTop / (1 - (scrollBarBottom - scrollBarTop))
        return y + round(maxOffsetY * offsetScalarY)

    def doNothing(*args):
        print("Function doNothing invoked with args: {}".format(args))

    def mouseScroll(self, evt):
        self.cnvs.yview_scroll(-1*(evt.delta) // 65, 'units')