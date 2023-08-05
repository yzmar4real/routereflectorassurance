# routereflectorassurance
Using Cisco's PyATS framework to develop Network Assurance testing for BGP route reflectors.



## Solution Components
*Python
*Genie
*PYATS
*CML (You will require live routers to perform these tests on)
*IOS XE Routers

## Prerequisites 

Python3.6 and above

CML or live lab environment

## Toolbox

This tool leverages the power of Unicon and Genie libraries from Cisco, which provide a unified way to connect and interact with devices, and to load testbeds respectively. It uses a custom DeviceRoutes class, located in the functions.routes module, to handle route collection and comparison.

The script performs the following tasks:

Loading the Testbed: The testbed details are loaded from a predefined YAML file, enabling the script to access and interact with the devices.

Checking BGP Peers: It checks and collects the Border Gateway Protocol (BGP) peers from the devices in the testbed.

Collecting Routes: The script then collects route details from all the devices.

Comparing Routes: It performs a comparison of the collected routes and stores the result.

Printing and Storing Results: The comparison result is printed to the console and also stored as a Pandas DataFrame. This DataFrame is then exported to a CSV file for easy viewing and further analysis.

Storing BGP Peers: The BGP peers information is stored in a JSON file for future reference.

## Outputs

!(OutputScreenShot1.PNG)
(OutputScreenShot2.PNG)
!(OutputScreenShot3.PNG)
