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

from tg_gui_core import *
from . import _imple as imple

class Rect(Widget):

    def __init__(self, radius=None, fill=None, **kwargs):
        super().__init__(**kwargs)

        self._fill_src = fill
        self._radius_src = radius

    def _place_(self, coord, dims):
        super()._place_(coord, dims)

        radius = self._radius_src
        if radius is None:
            radius = self._screen_.default.radius
        if isinstance(radius, DimensionSpecifier):
            radius = radius._calc_dim_()

        self._radius = min(radius, self.width//2, self.height//2)

        self._group = imple.RoundRect(
            *self._rel_placement_,
            r=self._radius,
        )

    def _render_(self):
        self._update_color()
        super()._render_()

    def _update_color(self):

        fill = self._fill_src
        # if isinstance(fill, StatefulAttribute):
        #     raise NotImplementedError
        if fill is None:
            fill = self._screen_.default._fill_color_
        elif isinstance(fill, State):
            fill = fill.getvalue(self, self._update_color)
        else:
            pass

        if self.isplaced():
            # if it is not placed then ._group will be None
            self._group.fill = fill

    def __del__(self):
        del self._fill_
