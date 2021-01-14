# Introduction

![docs](https://readthedocs.org/projects/circuitpython-tg-gui-std/badge/?version=latest)
![chat](https://img.shields.io/discord/327254708534116352.svg)
![build badge](https://github.com/TG-Techie/CircuitPython_TG-Gui-Std/workflows/Build%20CI/badge.svg)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)

This is an implementation of the TG-Gui standard library using displayio as a backend for easy embedded GUIs.
This supplies a bunch for useful widgets like buttons, sliders, and labels that inegrate with circuitpython's native UI library.


## Dependencies
This library depends on:

- [TG-Techie's TG-Gui-Core](https://github.com/TG-Techie/TG-Gui-Core)
- [Adafruit CircuitPython 6.0+](https://github.com/adafruit/circuitpython)
- [Adafruit CircuitPython Display Shapes](https://github.com/adafruit/Adafruit_CircuitPython_Display_Shapes)
- [Adafruit CircuitPython Display Text](https://github.com/adafruit/Adafruit_CircuitPython_Display_Text)
- [Adafruit CircuitPython ProgressBar](https://github.com/adafruit/Adafruit_CircuitPython_ProgressBar)

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading the circuitpython drivers from
[the Adafruit library and driver bundle](https://circuitpython.org/libraries)
and the gui core from [TG-Gui-Core](https://github.com/TG-Techie/TG-Gui-Core).

## Usage Example

```python
from tg_gui_std.all import *
from <some startup module> import appwrapper, run_even_loop

@appwrapper
class my_app(Layout):

    button = Button(text="Press me...", press=self.on_press)

    def _any_(self):
        self.button((0, center), (self.width, self.height//4)

    def on_press(self):
        print("pressed!", time.monotonic())

     def _loop_(self):
        pass

if __name__ == '__main__:
    run_even_loop()
```

# Contributing
Contributions are welcome! Please read the circuitpython [Code of Conduct](https://github.com/TG-Techie/TG-Gui-Std-CircuitPython/blob/master/CODE_OF_CONDUCT.md)
before contributing to help this project stay welcoming.

You may also reach out on discord if you have more specific questions: `@TG-Techie#5402`.

# Documentation
For information on building library documentation, please check out (adafruit's guide)(https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1).
