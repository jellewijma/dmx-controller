
import json

def save_show(filename, dmx_frame, patch_manager):
    """Saves the show data (DMX frame and patch) to a JSON file."""
    serializable_patch = {}
    for universe, fixtures in patch_manager.patched_fixtures.items():
        serializable_patch[universe] = []
        for patch_info in fixtures:
            serializable_patch[universe].append({
                'manufacturer': patch_info['fixture']['manufacturer'],
                'model': patch_info['fixture']['model'],
                'address': patch_info['address'],
            })

    show_data = {
        'dmx_frame': dmx_frame,
        'patched_fixtures': serializable_patch
    }
    with open(filename, 'w') as f:
        json.dump(show_data, f, indent=4)

def load_show(filename, fixture_library):
    """Loads the show data from a JSON file."""
    try:
        with open(filename, 'r') as f:
            show_data = json.load(f)
            dmx_frame = show_data.get('dmx_frame', [0] * 512)
            patched_fixtures_data = show_data.get('patched_fixtures', {})
            
            # Reconstruct patched_fixtures into a format usable by PatchManager
            reconstructed_patched_fixtures = {}
            for universe_str, fixtures_data in patched_fixtures_data.items():
                universe = int(universe_str)
                reconstructed_patched_fixtures[universe] = []
                for patch_data in fixtures_data:
                    fixture = fixture_library.get_fixture(patch_data['manufacturer'], patch_data['model'])
                    if fixture:
                        patch_info = {
                            'fixture': fixture,
                            'address': patch_data['address'],
                            'channel_map': {},
                        }
                        mode = fixture['modes'][0] # Assuming the first mode
                        for i, channel_name in enumerate(mode['channels']):
                            patch_info['channel_map'][channel_name] = i
                        reconstructed_patched_fixtures[universe].append(patch_info)

            return dmx_frame, reconstructed_patched_fixtures
    except (FileNotFoundError, json.JSONDecodeError):
        return [0] * 512, {}
