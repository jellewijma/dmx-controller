
from src.fixture_library import FixtureLibrary
from src.patch_manager import PatchManager
from src import gui

def main():
    """Main function to run the DMX controller."""
    fixture_library = FixtureLibrary()
    patch_manager = PatchManager()
    gui.create_gui(patch_manager, fixture_library)

if __name__ == "__main__":
    main()
