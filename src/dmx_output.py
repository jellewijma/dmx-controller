from ola.ClientWrapper import ClientWrapper
import array
import subprocess
import re

# Global wrapper and client for sending DMX
_wrapper = None
_client = None

def _get_wrapper_client():
    global _wrapper, _client
    if _wrapper is None:
        _wrapper = ClientWrapper()
        _client = _wrapper.Client()
    return _wrapper, _client

def dmx_sent(state):
    if not state.Ok():
        print(f"Error sending DMX: {state.message}")

def send_dmx(data, universe=1):
    """Sends DMX data to the specified universe using OLA."""
    wrapper, client = _get_wrapper_client()
    
    dmx_data = array.array('B', data)
    
    client.SendDmx(universe, dmx_data, dmx_sent)
    # We are not running the wrapper here to avoid blocking
    # This is a fire-and-forget approach.
    # For more complex scenarios, a dedicated OLA client thread would be better.

def get_dmx_devices():
    """Returns a list of available DMX device names by parsing ola_dev_info output."""
    try:
        result = subprocess.run(['ola_dev_info'], capture_output=True, text=True, check=True, timeout=5)
        output = result.stdout
        
        device_names = []
        # Regex to find "Device X: Device Name"
        # Example: "Device 0: Art-Net Device"
        for line in output.splitlines():
            match = re.match(r"Device \d+: (.+)", line)
            if match:
                device_names.append(match.group(1).strip())
        return device_names
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"Error getting DMX devices: {e}")
        return []

def is_device_active(device_name):
    """Checks if a DMX device with the given name is active by checking ola_dev_info output."""
    return device_name in get_dmx_devices()