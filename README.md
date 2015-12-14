# GoTimer
A simple external bomb-timer for CS:GO, written in Python.

## Demonstration
[![A simple video demo](http://img.youtube.com/vi/tEdAwi1Hqbk/0.jpg)](http://www.youtube.com/watch?v=tEdAwi1Hqbk)

Click image to see a small clip of GoTimer in action.

## How to use
You need Python 3, along with the following Python packages (pip install package-name)
* Flask
* Tkinter (if not installed)
* Requests

You also need to place the **gamestate_integration_go_timer.cfg** from the **listener folder** in your cfg folder. The path is typically  X:\PATH_TO_STEAM\steamapps\common\Counter-Strike Global Offensive\csgo\cfg .

With these in place, simply launch go_timer.py ("python go_timer.py")
For Windows users, you can also just click the supplied bat-file.

## Credits
The GameState-listener is inspired by [csgo-c4-hue](https://github.com/doobix/csgo-c4-hue).

I also got some valuable tips from the [Quick Start guide to CS:GO Game State Integration](https://github.com/tsuriga/csgo-gsi-qsguide).
