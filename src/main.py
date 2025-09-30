
import os
from src.fixture_library import FixtureLibrary
from src.patch_manager import PatchManager
from src import gui
from src.show_file import load_show

LAST_SHOW_FILE_PATH = "last_show_path.txt"

def main():
    """Main function to run the DMX controller."""
    fixture_library = FixtureLibrary()
    patch_manager = PatchManager()

    initial_dmx_frame = [0] * 512
    initial_patched_fixtures = {}
    last_show_file = None

    if os.path.exists(LAST_SHOW_FILE_PATH):
        with open(LAST_SHOW_FILE_PATH, 'r') as f:
            last_show_file = f.read().strip()

    if last_show_file and os.path.exists(last_show_file):
        initial_dmx_frame, initial_patched_fixtures = load_show(last_show_file, fixture_library)
        print(f"Automatically loaded last show from {last_show_file}")

    gui.create_gui(patch_manager, fixture_library, initial_dmx_frame, initial_patched_fixtures)

if __name__ == "__main__":
    main()
