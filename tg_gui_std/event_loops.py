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


# #@micropython.native
def has_phys_coord_in(widget, coord, _print=False):
    #
    minx, miny = widget._phys_coord_
    x, y = coord
    maxx, maxy = widget._phys_end_coord
    return (minx <= x <= maxx) and (miny <= y <= maxy)


class SinglePointEventLoop:
    def __init__(self, *, screen, update_coord):
        self._update_coord = update_coord
        self._screen = screen

        # initial state of the loop
        self._was_touched = False
        self._last_coord = (-0x1701D, -0x1701D)  # ;-)

        self._selected = None
        self._found_pressable = None
        self._found_updateable = None

    def loop(self):

        # get previous data
        was_touched = self._was_touched
        last_coord = self._last_coord

        # get current data
        coord = self._update_coord()
        is_touched = bool(coord is not None)
        # if is_touched:
        #   print(coord)

        if is_touched and not was_touched:  # if finger down
            #
            # scan thought all pointable widgets

            screen = self._screen
            for widget in screen._selectbles_:
                # if the point being touched is a in the widget
                if has_phys_coord_in(widget, coord):

                    widget._select_()
                    self._selected = widget
                    break

            for widget in screen._pressables_:
                if has_phys_coord_in(widget, coord):

                    self._found_pressable = widget
                    break

            for widget in screen._updateables_:
                if has_phys_coord_in(widget, coord, _print=True):

                    widget._start_coord_(adjust_phys_to_rel(widget, coord))
                    self._found_updateable = widget
                    break

        elif not is_touched and was_touched:  # if finger raised

            if self._selected is not None:

                self._selected._deselect_()
                self._selected = None

            if self._found_pressable is not None:

                self._found_pressable._press_()
                self._found_pressable = None

            updateable = self._found_updateable
            if updateable is not None:

                updateable._last_coord_(
                    adjust_phys_to_rel(updateable, self._last_coord)
                )
                self._found_updateable = None
        elif is_touched:  # and self._found_updateable is not None:
            updateable = self._found_updateable
            if updateable is not None:
                updateable._update_coord_(adjust_phys_to_rel(updateable, coord))
        else:
            pass

        # store current data as next loop's last data
        self._was_touched = is_touched
        self._last_coord = coord
