from ola.ClientWrapper import ClientWrapper
import array

def dmx_sent(state):
    if not state.Ok():
        print(f"Error sending DMX: {state.message}")

def send_dmx(data, universe=1):
    """Sends DMX data to the specified universe using OLA."""
    wrapper = ClientWrapper()
    client = wrapper.Client()
    
    dmx_data = array.array('B', data)
    
    client.SendDmx(universe, dmx_data, dmx_sent)
    # We are not running the wrapper here to avoid blocking
    # This is a fire-and-forget approach.
    # For more complex scenarios, a dedicated OLA client thread would be better.