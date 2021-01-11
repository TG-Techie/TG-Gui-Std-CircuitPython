Introduction
============

.. image:: https://readthedocs.org/projects/circuitpython-tg-gui-std/badge/?version=latest
    :target: https://circuitpython-tg-gui-std.readthedocs.io/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/TG-Techie/CircuitPython_TG-Gui-Std/workflows/Build%20CI/badge.svg
    :target: https://github.com/TG-Techie/CircuitPython_TG-Gui-Std/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

An implementation of the TG-Gui standard library using displayio as a backend for easy embedded GUIs. 
This supplies a bunch for useful widgets like buttons, sliders, and labels that inegrate with circuitpython's native UI library.


Dependencies
=============
This driver depends on:

* `TG-Techie's TG-Gui-Core <https://github.com/TG-Techie/TG-Gui-Core>`_
* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Adafruit CircuitPython Display Shapes <https://github.com/adafruit/Adafruit_CircuitPython_Display_Shapes>`_
* `Adafruit CircuitPython Display Text<https://github.com/adafruit/Adafruit_CircuitPython_Display_Text>`_
* `Adafruit CircuitPython ProgressBar <https://github.com/adafruit/Adafruit_CircuitPython_ProgressBar>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading the circuitpython drivers from
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
and TG-Gui-Core .

Usage Example
=============

.. code-block:: python
    import time
    
    from tg_gui_std import *
    from <some startup code> import mainapp, run_even_loop
    
    @mainapp
    class my_app(Layout):
    
        button = Button(text="Press me...", press=self.on_press)
        
        def _any_(self): 
            self.button((0, center), (self.width, self.height//4)
        
        def on_press(self):
            print("pressed!", time.monotonic())
           
         def _loop_(self):
            pass

Contributing
============

Contributions are welcome! Please read the circuitpython `Code of Conduct
<https://github.com/TG-Techie/TG-Gui-Std-CircuitPython/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `adafruit's guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
