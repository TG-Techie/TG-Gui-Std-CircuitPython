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

# TODO: make the knob aligned with the center of the
#   touch once the finger starts moving

class Slider(Widget):

    def __init__(self, *, state, palette=None, _debug=False, **kwargs):
        super().__init__(**kwargs)
        self._state = state # the state object to update
        self._palette = palette

        self._debug = _debug

        self._start_coord = None
        self._started_in_limits = None
        self._selected = False

    _selected_ = property(lambda self: self._selected)

    def _on_nest_(self):
        if self._palette is None:
            self._palette = self._screen_.palettes.primary

    def _place_(self, coord, dims, knob_dim=None):
        super()._place_(coord, dims)

        screen = self._screen_
        palette = self._palette
        debug = self._debug

        sx, sy, sw, sh = self._placement_
        rx, ry, rw, rh = self._rel_placement_

        if knob_dim is None:
            knob_dim = screen.min_size

        self._group = group = imple.Group(
            x=rx, y=ry, max_size=(3 if debug else 2)
        )


        self._bar = bar = imple.ProgressBar(
            0, rh//2 - 6, rw, 12, stroke = 0,
            bar_color=self._palette.fill_color
        )

        self._knob = knob = imple.RoundRect(
            0, rh//2 - knob_dim//2,
            width   = knob_dim,
            height  = knob_dim,
            r       = screen.default.radius,
            fill    = color.lightgray,
            stroke  = knob_dim//10,
            outline = color.gray,
        )

        group.append(bar)
        group.append(knob)

        self._knob_dim = knob_dim
        self._span = value_range = rw - knob_dim
        self._position = pos = int(value_range * self._state.getvalue(self, lambda: None))
        self._y_limits = (sh//2 - knob_dim//2, sh//2 + knob_dim//2)
        self._value = pos / value_range
        self._pos_on_prev_update = -10000
        self._update_position(pos)

        if debug:
            self._mark = mark = imple.RoundRect(
                0, rh//2 - knob_dim//2,
                width   = knob_dim*2,
                height  = knob_dim,
                r=0,
                fill    = color.red,
                stroke  = 0
            )
            group.append(mark)

    def _render_(self):
        #self._update_value(self._value) # formats group
        super()._render_()

    # #@micropython.native
    def _select_(self, coord):
        # TODO: ADD  EXPLANATION
        self._initial_position = init_pos = self._position
        knob_dim = self._knob_dim
        x_limits = xmin, xmax = (init_pos-knob_dim//2, init_pos + 3*knob_dim//2)
        ymin, ymax = self._y_limits
        x, y = coord
        self._init_x = init_x = clip(knob_dim//2, x, self._span + knob_dim//2)
        self._selected = bool((ymin <= y <= ymax) and (xmin <= x <= xmax))

        if self._debug:
            self._mark.x = xmin

    # #@micropython.native
    def _deselect_(self, coord):
        pass # self._start_coord = None

    # #@micropython.native
    def _update_coord_(self, coord):
        #print(self, coord)
        if self._selected:
            value = coord[0] - self._init_x + self._initial_position
            value = clip(0, value, self._span)
            self._update_position(value)

    # #@micropython.native
    def _update_position(self, new_pos):
        self._position = new_pos
        value = new_pos / self._span

        prev_pos = self._pos_on_prev_update
        if abs(prev_pos - new_pos) > 3:

            knob = self._knob
            bar = self._bar

            # updating state first makes the animation a little less tear-able
            self._state.update(value)
            self._value = value

        # print(self, prev_pos, new_pos, prev_pos - new_pos)
        # prev_pos = self._pos_on_prev_update
        # if abs(prev_pos - new_pos) > 3:
            knob.x = new_pos
            bar.progress = value
            self._pos_on_prev_update = new_pos