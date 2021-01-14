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


def adjust_phys_to_rel(ref_wid, coord):
    x, y = coord
    px, py = ref_wid._phys_coord_
    return (x - px, y - py)


class SinglePointEventLoop:
    def __init__(self, *, screen, update_coord):
        self._update_coord = update_coord
        self._screen = screen

        # initial state of the loop
        self._was_touched = False
        self._last_coord = (-0x1701D, -0x1701D)  # ;-)
        self._selected = None
        self._supports_updating = False

    def loop(self):

        # get previous data
        was_touched = self._was_touched
        last_coord = self._last_coord

        # get current data
        coord = self._update_coord()
        is_touched = bool(coord is not None)

        if is_touched and not was_touched:  # if finger down
            # print('event_loop', coord)
            # scan thought all pointable widgets
            for widget in self._screen._pressables_:
                # if the point being touched is a in the widget
                if widget._has_phys_coord_in_(coord):
                    # then select teh widget
                    widget._select_(adjust_phys_to_rel(widget, coord))
                    # save this widget for the next
                    self._selected = widget
                    self._supports_updating = hasattr(widget, "_update_coord_")
                    break
        elif not is_touched and was_touched:  # if finger raised
            selected = self._selected
            # if an item is selected
            if selected is not None:
                # than deselect it
                selected._deselect_(adjust_phys_to_rel(selected, last_coord))
                # if the widget can be pressed, press it
                if selected._has_phys_coord_in_(last_coord) and hasattr(
                    selected, "_press_"
                ):
                    selected._press_()
                # remove the reference to it
                self._selected = None
                self._supports_updating = False
        elif is_touched and self._supports_updating:  # than update it
            selected = self._selected
            if selected is not None:
                selected._update_coord_(adjust_phys_to_rel(selected, coord))
        else:
            pass

        # store current data as next loop's last data
        self._was_touched = is_touched
        self._last_coord = coord
