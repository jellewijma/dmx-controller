
import os
import json

class FixtureLibrary:
    def __init__(self, fixture_directory="fixtures"):
        self.fixtures = []
        self.fixture_directory = fixture_directory
        self._load_fixtures()

    def _load_fixtures(self):
        if not os.path.exists(self.fixture_directory):
            os.makedirs(self.fixture_directory)
            
        for filename in os.listdir(self.fixture_directory):
            if filename.endswith(".json"):
                filepath = os.path.join(self.fixture_directory, filename)
                with open(filepath, 'r') as f:
                    try:
                        fixture_data = json.load(f)
                        self.fixtures.append(fixture_data)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from {filepath}")

    def get_fixture(self, manufacturer, model):
        for fixture in self.fixtures:
            if fixture.get('manufacturer') == manufacturer and fixture.get('model') == model:
                return fixture
        return None

# Example Usage:
if __name__ == '__main__':
    # Create a dummy fixture file for testing
    dummy_fixture = {
        "manufacturer": "Robe",
        "model": "Pointe",
        "modes": [
            {
                "name": "16-channel",
                "channels": [
                    "pan", "tilt", "speed", "dimmer", "strobe", "color_wheel", "gobo_wheel", "gobo_rotation",
                    "prism", "prism_rotation", "focus", "zoom", "frost", "reset", "lamp_control", "extra"
                ]
            }
        ],
        "channels": {
            "pan": {"name": "Pan", "type": "pan"},
            "tilt": {"name": "Tilt", "type": "tilt"},
            "speed": {"name": "Pan/Tilt Speed", "type": "other"},
            "dimmer": {"name": "Dimmer", "type": "dimmer"},
            "strobe": {"name": "Strobe", "type": "strobe"},
            "color_wheel": {"name": "Color Wheel", "type": "color"},
            "gobo_wheel": {"name": "Gobo Wheel", "type": "gobo"},
            "gobo_rotation": {"name": "Gobo Rotation", "type": "gobo"},
            "prism": {"name": "Prism", "type": "other"},
            "prism_rotation": {"name": "Prism Rotation", "type": "other"},
            "focus": {"name": "Focus", "type": "focus"},
            "zoom": {"name": "Zoom", "type": "zoom"},
            "frost": {"name": "Frost", "type": "other"},
            "reset": {"name": "Reset", "type": "other"},
            "lamp_control": {"name": "Lamp Control", "type": "other"},
            "extra": {"name": "Extra Functions", "type": "other"}
        }
    }

    if not os.path.exists("fixtures"):
        os.makedirs("fixtures")

    with open("fixtures/robe_pointe.json", 'w') as f:
        json.dump(dummy_fixture, f, indent=4)

    library = FixtureLibrary()
    pointe = library.get_fixture("Robe", "Pointe")
    if pointe:
        print("Fixture found:")
        print(json.dumps(pointe, indent=4))
    else:
        print("Fixture not found.")
