from tkinter import Canvas, BOTH
from tkinter.ttk import Frame
from typing import Optional
from app.helpers.point import Point
from config import AnchorTypes


class TKCanvas:
    __canvas: Canvas
    __container: Frame
    canvas_config = {}

    def __init__(self):
        super().__init__()

    @property
    def canvas(self):
        try:
            self.__canvas
        except:
            self.__canvas = Canvas(self.__container)

        return self.__canvas

    @property
    def canvas_size(self):
        try:
            self.__canvas
        except:
            ...

        self.__canvas.update()
        return (self.__canvas.winfo_width(), self.__canvas.winfo_height())

    def init_canvas(self, container: Frame, canvas_config: dict):
        self.canvas_config = canvas_config
        self.__container = container
        self.canvas.configure(
            background=self.canvas_config["background"],
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.pack(fill=BOTH, expand=1)

    def calc_widget_position(
        self,
        anchor: Optional[AnchorTypes] = None,
        widget_width: Optional[int] = None,
        widget_height: Optional[int] = None,
        margin_x: Optional[int | tuple[int, int]] = None,
        margin_y: Optional[int | tuple[int, int]] = None,
    ):
        max_w, max_h = self.canvas_size
        anchor = anchor if anchor else "TL"

        mx: tuple[int | None, int | None] = (None, None)
        if margin_x:
            if isinstance(margin_x, int):
                mx = (margin_x, margin_x)
            else:
                mx = margin_x

        my = (None, None)
        if margin_y:
            if isinstance(margin_y, int):
                my = (margin_y, margin_y)
            else:
                my = margin_y

        # max_w         [____________________]
        # width         [       xxxxxx       ]
        # spacing_x     [_______      _______]
        # ml            [_______xxxxxx       ]
        # mr            [       xxxxxx_______]
        # tl.x          [       Oxxxxx       ]
        # br.x          [       xxxxxO       ]

        # anchor=l
        #       tl.x = ml
        #       br.x = ml + width
        # anchor=r
        #       tl.x = max_w - width - mr
        #       br.x = max_w - mr

        tl = Point()
        br = Point()

        ml, mr = mx
        ml = ml if ml else 0
        mr = mr if mr else 0

        if widget_width is not None:
            width = widget_width
            spacing_x = max_w - width

            if not ml and not mr:
                mx_auto = spacing_x // 2
                ml, mr = (mx_auto, mx_auto)
        else:
            width = max_w - ml - mr

        # Normalize x
        if anchor == "TL" or anchor == "BL":
            tl.x = ml
            br.x = ml + width

        elif anchor == "TR" or anchor == "BR":
            # [   Oxxxxx______] tl.x = max_w - mr - width
            ml = max_w - width - mr
            tl.x = ml
            br.x = ml + width

        # print(max_w, widget_width, width, tl.x, br.x)

        mt, mb = my
        mt = mt if mt else 0
        mb = mb if mb else 0

        if widget_height:
            height = widget_height
            spacing_y = max_h - height

            if not mt and not mb:
                my_auto = spacing_y // 2
                mt, mb = (my_auto, my_auto)
        else:
            height = max_h - mt - mb

        # Normalize y
        if anchor == "TL" or anchor == "TR":
            tl.y = mt
            br.y = mt + height

        elif anchor == "BL" or anchor == "BR":
            mt = max_h - height - mb
            tl.y = mt
            br.y = mt + height

        return (tl, br)
