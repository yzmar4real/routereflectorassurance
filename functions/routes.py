import logging
import sys
from pyats.log.utils import banner

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
log = logging.getLogger()


# Define a dictionary to map device types to their respective BGP commands
bgp_commands = {
    'ios': 'show ip bgp summary',
    'iosxe': 'show bgp ipv4 unicast summary',
    'nxos': 'show bgp ipv4 unicast summary',
    'iosxr': 'show bgp ipv4 unicast summary'
}

class DeviceRoutes:
    def __init__(self):
        self.devices_routes = {}


    def bgp_check_peers(self, testbed):
        output_outcome = []
        for dev_name,dev in testbed.devices.items():
            nei_outcome = []
            checker_outcome = {}
            try:
                log.debug(f"Connection being made to {dev_name}")
                dev.connect(learn_hostname=True, init_exec_commands=[], init_config_commands=[], log_stdout=True)
                connected = True
            except Exception as e:
                log.error(f"Device {dev_name} cannot be logged into:', str{e}")
                connected = False

            if connected is True: 
                routes = {}
                peer_count = 0
                log.debug(f"Checking peers for Device {dev_name}")

                try:
                    if dev.type in bgp_commands:
                        bgp_cmd = bgp_commands[dev.type]
                        routes = dev.parse(bgp_cmd)
                    else:
                        log.warning('Unsupported device type.')
                        # You can choose to raise an exception or handle it accordingly.
                except:
                    log.error('Error running this command')
            
                peer_count = len(routes['vrf']['default']['neighbor'].keys())
                log.info(banner(f"Device {dev_name} has {peer_count} BGP Peers"))

                bgp_outcome = routes['vrf']['default']['neighbor']

                for nei in bgp_outcome:
                    up_down = bgp_outcome[nei]['address_family']['ipv4 unicast']['up_down']
                    state_pfxrcd = bgp_outcome[nei]['address_family']['ipv4 unicast']['state_pfxrcd']
                    
                    nei_outcome.append({ nei :{'up_down': up_down, 'State': state_pfxrcd} })
                
            checker_outcome = {'Device': dev_name, 'Peer': peer_count, 'Outcome': nei_outcome}
            output_outcome.append(checker_outcome)
        
        return (output_outcome)



    def collect_routes(self, testbed):
        try:
            for dev_name,dev in testbed.devices.items():
                print(f"Connection to {dev_name}")
                dev.connect(learn_hostname=True, init_exec_commands=[], init_config_commands=[], log_stdout=True)
                print(f"Collecting routes from to {dev_name}")
                routes = dev.api.get_routes()
                print(f"Routes from {dev_name} : {routes}")
                self.devices_routes[dev_name] = routes

        except Exception as e:
            print('Failure:', str(e))

    def compare_routes(self):
        all_routes = set(route for routes in self.devices_routes.values() for route in routes)
        route_comparison = []
        for dev_name, routes in self.devices_routes.items():
            missing_routes = all_routes.difference(routes)
            route_comparison.append({
                'Device Name': dev_name,
                'Routes Missing': missing_routes
            })
        self.route_comparison = route_comparison

