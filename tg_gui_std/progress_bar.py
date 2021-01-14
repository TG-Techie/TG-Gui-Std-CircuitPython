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


class ProgressBar(Widget):
    def __init__(self, *, progress, palette=None, _fill_space=False, **kwargs):
        super().__init__(**kwargs)

        self._fill_space = _fill_space
        self._prog_src = progress
        self._palette = None

    def _on_nest_(self):
        if self._palette is None:
            self._palette = self._screen_.palettes.primary

    def _place_(self, coord, dims):
        super()._place_(coord, dims)

        self._group = imple.Group(max_size=2)

        radius = self._phys_height_ // 2

        if self._fill_space:
            self._group = group = imple.ProgressBar(
                *self._rel_placement_,
                progress=0.0,
                stroke=1,
                bar_color=self._palette.fill_color,
            )
        else:
            self._group = group = imple.ProgressBar(
                x=self._rel_x_ + radius,
                y=self._rel_y_ + self._phys_height_ // 2 - 6,
                width=self._phys_width_ - 2 * radius,
                height=12,
                progress=0.0,
                stroke=1,
                bar_color=self._palette.fill_color,
            )

    def _render_(self):
        self._update_progress()
        super()._render_()

    def _update_progress(self):
        if self.isplaced():
            value = src_to_value(
                src=self._prog_src,
                widget=self,
                handler=self._update_progress,
                default=0.0,
            )
            self._group.progress = clip(0.0, value, 1.0)
