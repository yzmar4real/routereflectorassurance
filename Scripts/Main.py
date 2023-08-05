# Import necessary modules
import json
import pandas as pd
from unicon import Connection # Network device connection library
from genie.testbed import load # To load testbeds
from functions.routes import DeviceRoutes # Custom module for route handling

# Load the testbed from a YAML file.
# This is a predefined set of devices and credentials used for testing network configurations.
testbed_new = load('./Testbed/routes.yaml')

# Create an instance of the DeviceRoutes class
device_routes = DeviceRoutes()

# Check BGP (Border Gateway Protocol) peers in the testbed
# BGP is a protocol used to exchange routing information across the internet
# The function bgp_check_peers will return a list of BGP peers
bgp_peers = device_routes.bgp_check_peers(testbed_new)

# Collect routes from all devices in the testbed
# The function collect_routes will update the 'device_routes' instance with routes collected from all devices
device_routes.collect_routes(testbed_new)

# Compare the routes from all devices
# The function compare_routes will update the 'device_routes' instance with a comparison result of all routes
device_routes.compare_routes()

# Print out the route comparison result
print(device_routes.route_comparison)

# Create a DataFrame from the route comparison result
df = pd.DataFrame(device_routes.route_comparison)

# Save the DataFrame into a csv file named 'route_comparison.csv'
df.to_csv('route_comparison.csv', index=False)

# Save the bgp peers information into a JSON file named 'bgp_peers.json'
with open('bgp_peers.json', 'w') as f:
    json.dump(bgp_peers, f)
