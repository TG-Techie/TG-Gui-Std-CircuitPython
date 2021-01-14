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

class Button(Widget):

    @StatefulAttribute(lambda self: False)
    def _selected_(self):
        self._update_colors()

    def _press_(self):
        #if self._press is not None:
        self._press()

    def __init__(self, *,
        text, press,#=None,
        size=None, palette=None,
        radius=None, _alignment=align.center,
        **kwargs
    ):
        super().__init__(**kwargs)

        self._radius_src = radius

        self._text_src = text
        self._alignment = _alignment
        self._size = size

        self._press = press
        self._palette = palette

    def _select_(self, coord):
        self._selected_ = True

    def _deselect_(self, coord):
        self._selected_ = False

    def _on_nest_(self):
        screen = self._screen_
        palette = self._palette
        if palette is None:
            self._palette = screen.palettes.primary

    def _place_(self, coord, dims):
        global imple
        super()._place_(coord, dims)

        press = self._press
        if isinstance(press, MethodSpecifier):
            self._press = press.getmethod(self)

        size = self._size
        if size is None:
            size = self._screen_.default.font_size

        radius = self._radius_src
        if radius is None:
            radius = self._screen_.default.radius
        if isinstance(radius, DimensionSpecifier):
            radius = radius._calc_dim_()

        radius = min(radius, self.width//2, self.height//2)

        self._group = group = imple.Group(max_size=2)

        self._rect = rect = imple.RoundRect(
            *self._rel_placement_,
            r=radius
        )
        self._label = label = imple.Label(
            text=' ',
            color=0xffffff,
            coord=self._rel_coord_,
            dims=self._phys_dims_,
            alignment = self._alignment,
            scale=size,
        )

        group.append(rect)
        group.append(label)

    def _render_(self):
        self._update_colors()
        self._update_text()
        super()._render_()

    def _update_text(self):
        self._label.text = src_to_value(
            src=self._text_src,
            widget=self,
            handler=self._update_text,
            default=' ',
        )

    def _update_colors(self):
        selected = self._selected_
        palette = self._palette
        self._rect.fill = (
            palette.selected_fill if selected else palette.fill_color
        )
        self._label.color = (
            palette.selected_text if selected else palette.text_color
        )