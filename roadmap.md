🛠️ Step-by-Step Coding Roadmap for a DMX MVP
Step 0 – Setup

Language: Python

Packages:

python-ola → send DMX via Open Lighting Architecture

mido → MIDI input

PyQt5 (or PySide6) → GUI sliders

Dev environment: Linux with OLA installed (apt install ola).

Prompt to AI:

“Generate a Python project skeleton with src/ and modules for dmx_output.py, midi_input.py, gui.py, and main.py. Add placeholder functions in each file.”

Step 1 – Hello World GUI

Goal: A PyQt GUI with 8 sliders (0–255) that print their values.

Prompt to AI:

“Write a PyQt5 GUI with 8 vertical sliders (0–255). Each slider should print its channel number and value when moved.”

✅ Run it → verify sliders appear and work.

Step 2 – DMX Output Basics

Goal: Send DMX data through OLA.

Prompt to AI:

“Write a function in dmx_output.py that uses ola.ClientWrapper to send values to Universe 1. Example: send 255 on channel 1, 0 on others.”

✅ Run test → if no dongle, use OLA’s dummy driver (ola_dev_info).

Step 3 – Connect GUI → DMX

Goal: Moving sliders updates DMX output.

Prompt to AI:

“Update the PyQt sliders so each change calls a function in dmx_output.py to update the corresponding channel on Universe 1. Make sure multiple sliders update the full DMX frame (512 values).”

✅ Test with dummy OLA universe.

Step 4 – MIDI Input Basics

Goal: Capture MIDI events.

Prompt to AI:

“Write a module midi_input.py using mido that listens to the first available MIDI device. Print note/fader values in real time.”

✅ Move a fader → confirm values print.

Step 5 – Map MIDI → GUI

Goal: MIDI fader updates slider in GUI.

Prompt to AI:

“Modify midi_input.py so MIDI CC values (0–127) scale to 0–255 and update the corresponding PyQt slider.”

✅ Test: moving MIDI controller updates GUI slider.

Step 6 – Persistence

Goal: Save/load channel values.

Prompt to AI:

“Add simple JSON save/load functions that store all channel values (512 max). Connect them to menu buttons in the GUI.”

✅ Test by saving, reopening app, and loading values.

🎯 At This Point = MVP

GUI sliders update DMX.

MIDI controller updates GUI/DMX.

Values can be saved/loaded.

That’s a working prototype you can demo.

Step 7 – Next Iterations (Post-MVP)

Add blackout button in GUI.

Add basic fixture grouping (e.g., link 3 channels into RGB).

Add cue system (save scenes with fade times).

Add MIDI learn (map any MIDI fader dynamically).
