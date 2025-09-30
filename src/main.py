
from . import dmx_output
from . import midi_input
from . import gui

def main():
    """Main function to run the DMX controller."""
    gui.create_gui()

if __name__ == "__main__":
    main()
