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

from ._imple import *

class DisplayioScreen(Screen):

    _nest_count_override = 1

    def __init__(self, *, display, **kwargs):
        self._display_ = display
        if not isinstance(display, displayio.Display):
            raise TypeError(f"screen must be of type 'Display', found '{type(self).__name__}'")
        super().__init__(**kwargs)

        self._pressables_ = []

    # #@micropython.native
    def on_widget_nest_in(_, wid:Widget):
        if not hasattr(wid, '_group'):
            wid._group = None

    # #@micropython.native
    def on_widget_render(self, wid:Widget):
        # print('on_widget_render:', repr(wid._superior_), wid)
        if wid._group is not None:
            # print(wid, wid._group)
            sgroup = wid._superior_._group
            # print('on_widget_render', wid, wid._group, sgroup.str_children() if sgroup is not None else repr(None))
            group = wid._group
            #if group not in sgroup:
            wid._superior_._group.append(group)

        if hasattr(wid, '_selected_'):
            self._pressables_.append(wid)

    # #@micropython.native
    def on_widget_derender(self, wid:Widget):
        if wid._group is None:
            return
        while wid._group in wid._superior_._group:
            wid._superior_._group.remove(wid._group)

        pressables = self._pressables_
        if wid in pressables:
            pressables.remove(wid)

    # #@micropython.native
    def on_container_place(_, wid:Widget):
        # print('on_container_place:', self, wid)
        if hasattr(wid, '_nest_count_override'):
            wid._group = Group(
                x=wid._rel_x_,
                y=wid._rel_y_,
                max_size=max(wid._nest_count_override)
            )
        else:
            wid._group = Group(
                x=wid._rel_x_,
                y=wid._rel_y_,
                max_size=max(1, len(wid._nested_))
            )

    # #@micropython.native
    def on_container_pickup(_, wid:Widget):
        wid._group = None

class DisplayioRootWrapper(RootWrapper):

    def __init__(self, *, display, screen, **kwargs):
        assert isinstance(display, displayio.Display)
        self._display = display
        display.auto_refresh = False

        if not isinstance(screen, DisplayioScreen):
            raise TypeError(f"screen must be of type 'DisplayioScreen', found '{type(screen).__name__}'")

        super().__init__(screen=screen, **kwargs)

        self._group = group = Group(max_size=1) # only has one child
        self._display.show(group)

    # def _std_startup_(self, cls):
    #     super()._std_startup_(cls)
    #     gc.collect()
    #     # self._display.auto_refresh = True
