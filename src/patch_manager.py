
import json

class PatchManager:
    def __init__(self):
        self.patched_fixtures = {}
        self.dmx_frames = {}
        self._next_fixture_id = 1 # Initialize fixture ID counter

    def add_fixture(self, fixture, universe, address, fixture_id=None):
        if universe not in self.patched_fixtures:
            self.patched_fixtures[universe] = []
            self.dmx_frames[universe] = [0] * 512

        if fixture_id is None:
            fixture_id = self._next_fixture_id
            self._next_fixture_id += 1
        else:
            # Ensure manually provided ID is unique and update counter if necessary
            for uni_fixtures in self.patched_fixtures.values():
                for pf in uni_fixtures:
                    if pf.get('id') == fixture_id:
                        raise ValueError(f"Fixture ID {fixture_id} already exists.")
            if fixture_id >= self._next_fixture_id:
                self._next_fixture_id = fixture_id + 1

        patch_info = {
            'id': fixture_id,
            'fixture': fixture,
            'address': address,
            'channel_map': {},
        }

        # Assuming the first mode is the one to be used
        mode = fixture['modes'][0]
        for i, channel_name in enumerate(mode['channels']):
            patch_info['channel_map'][channel_name] = i

        self.patched_fixtures[universe].append(patch_info)

    def set_parameter(self, universe, address, parameter_name, value):
        if universe not in self.patched_fixtures:
            return

        for patch_info in self.patched_fixtures[universe]:
            if patch_info['address'] == address:
                if parameter_name in patch_info['channel_map']:
                    channel_offset = patch_info['channel_map'][parameter_name]
                    dmx_channel = patch_info['address'] + channel_offset - 1
                    if 0 <= dmx_channel < 512:
                        self.dmx_frames[universe][dmx_channel] = value
                return

    def get_dmx_frame(self, universe):
        return self.dmx_frames.get(universe, [0] * 512)

    def get_fixture_by_id(self, fixture_id):
        for universe, fixtures in self.patched_fixtures.items():
            for patch_info in fixtures:
                if patch_info.get('id') == fixture_id:
                    return patch_info
        return None

    def clear_patch(self):
        self.patched_fixtures = {}
        self.dmx_frames = {}
        self._next_fixture_id = 1 # Reset ID counter on clear
# Example Usage:
if __name__ == '__main__':
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

    patch_manager = PatchManager()
    patch_manager.add_fixture(dummy_fixture, 1, 1)

    patch_manager.set_parameter(1, 1, "dimmer", 255)
    patch_manager.set_parameter(1, 1, "pan", 128)

    dmx_frame = patch_manager.get_dmx_frame(1)

    print("DMX Frame for Universe 1:")
    print(dmx_frame)

    # Verify the values
    assert dmx_frame[0] == 128 # Pan is the first channel (address 1)
    assert dmx_frame[3] == 255 # Dimmer is the fourth channel (address 4)
    print("\nVerification successful!")
