# The MIT License (MIT)
#
# Copyright (c) 2021 Jonah Yolles-Murphy (TG-Techie)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
"""

import gc
import displayio
import terminalio
import math

from tg_gui_core import *

from adafruit_display_text.label import Label as Dispio_Label

from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.polygon import Polygon

from adafruit_progressbar import ProgressBar

_DEBUG_FILE = True

if not _DEBUG_FILE:
    Group = displayio.Group
else:

    class Group(displayio.Group):

        max_size = property(lambda self: self._max_size)

        def __init__(self, max_size=10, owner=None, **kwargs):
            super().__init__(max_size=max_size, **kwargs)
            self._owner = owner
            self._max_size = max_size

        def __repr__(self):
            owner = self._owner
            owner_str = " " + repr(owner) if owner is not None else ""
            return f"<Group ({self._max_size}){owner_str}>"

        def _repr_with_children(self):
            return f"<Group ({self._max_size}){[self[index] for index in range(len(self))]}>"

        def append(self, wid):
            if _DEBUG_FILE and False:
                print("group.append", wid)
            super().append(wid)


class LightRoundRect(displayio.TileGrid):  # displayio.Group):
    def __init__(self, x, y, width, height, r=0, fill=0xFF0000):

        r = min(r, width // 2, height // 2)
        p = displayio.Palette(2)
        s = displayio.Shape(width, height)  # , mirror_x=True, mirror_y=True)
        super().__init__(s, pixel_shader=p, x=x, y=y)

        p.make_transparent(0)
        # p.make_opaque(1)
        p[1] = fill

        self._palette = p
        self._shape = s
        self._radius = r

        self._x = x
        self._y = y
        self._width = width
        self._height = height

        # apply the radius
        rsqrd = r ** 2
        for rowy in range(0, r):
            indent = r - round(math.sqrt(rsqrd - (rowy - r) ** 2))
            right_indent = width - indent - 1
            s.set_boundary(rowy, indent, right_indent)
            s.set_boundary(height - rowy - 1, indent, right_indent)

    @property
    def fill(self):
        return self._palette[1]

    @fill.setter
    def fill(self, value: int):
        self._palette[1] = value


class Label(displayio.Group):
    def __init__(
        self,
        *,
        coord,
        dims,
        alignment=align.center,
        text="<text>",
        color=0xFFFFFF,
        scale=1,
    ):
        super().__init__(
            max_size=1,
            x=coord[0],
            y=coord[1],
        )

        self._coord = coord
        self._dims = dims

        self._text = text
        self._scale = scale
        self._color = color
        self._alignment = alignment

        self.append(displayio.Group())
        # self._new_native()
        self._native = Dispio_Label(terminalio.FONT, text=" ")

    # @property
    # def bound_size

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._native.color = value
        self._color = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):

        if len(value) <= len(self._text):
            self._text = value
            self._native._update_text(value)
            self._position_native()
        else:
            self._text = value

            # make new native display group item
            self._native = native = Dispio_Label(
                terminalio.FONT,
                text=self._text,
                scale=self._scale,
                color=self._color,
            )
            self._position_native()
            # swap out for the new one (relies on being the last more item)
            self.pop(0)
            self.append(native)

    def _position_native(self):
        global align
        width, height = self._dims
        native = self._native
        alignment = self._alignment
        native.y = height // 2
        if alignment is align.center:
            native.x = (width // 2) - (self._scale * native.bounding_box[2] // 2)
        elif alignment is align.leading:
            native.x = 0
        elif alignment is align.trailing:
            native.x = width - (self._scale * native.bounding_box[2])
        else:
            raise ValueError(
                f"{alignment} is not a valid value, must be `align.center`, `align.leading`, or `align.trailing`"
            )

    def _new_native(self):
        # TODO: no longer used, consider removing
        self._native = native = Dispio_Label(
            terminalio.FONT,
            text=self._text,
            scale=self._scale,
            color=self._color,
        )

        self._position_native()
        self.pop(0)
        self.append(native)
