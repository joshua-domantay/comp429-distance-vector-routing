# Simulating Distance Vector Routing Protocol
Project for COMP 429 Computer Network Software. Simplified version of the Distance Vector Routing Protocol

## Setting Up Topology Files
The topology file will have the following layout:
```
<number of servers = x>
<number of neighbors = y>

<server_id_1> <ip_address_for_server_id_1> <port_number_for_server_id_1>
<server_id_2> <ip_address_for_server_id_2> <port_number_for_server_id_2>
...
<server_id_x>

<own_server_id> <neighbor_server_id_1> <link_cost_between_server_to_neighbor_1>
<own_server_id> <neighbor_server_id_2> <link_cost_between_server_to_neighbor_2>
...
<own_server_id> <neighbor_server_id_y> <link_cost_between_server_to_neighbor_y>
```
First line will be the number of servers in the network.<br>
Second line will be the number of neighbors from the server using the topology file.<br>
The next lines will be the information for each server in the network. Each line should consist of:<br>
1. Unique server id<br>
2. IP address of server<br>
3. Port number used by server<br>

The next lines setup the link costs between neighboring servers. Each line should consist of:<br>
1. Server id used by the server
2. Server id of neighbor
3. Link cost between the two servers

## Example Topology
![alt text](https://github.com/joshua-domantay/comp429-distance-vector-routing/blob/main/topology_example.png?raw=true)<br>
The topology files `topology1.txt`, `topology2.txt`, `topology3.txt`, and `topology4.txt` will setup the network topology shown above.<br>
The number of the topology file corresponds to the server id:<br>
- So `topology1.txt` is the toplogy file for server 1,<br>
- `topology2.txt` is for server 2,<br>
- and so on.<br>

## Demo Video
The video below shows the program being used to simulate the example topology.<br>
[![Watch the video](https://img.youtube.com/vi/xmpdT7G13QE/maxresdefault.jpg)](https://youtu.be/xmpdT7G13QE)<br>

## Installation
Install the latest version of Python. The version we used for this project is 3.11.2.<br>
Python modules such as sys, _thread, and socket should be included with the Python installation.<br>

## How to Run the Program
1. Open the terminal in the directory where `server.py` is stored.<br>
2. Make sure Python is installed by running `python --version`. The output should be `Python <version_number>`.<br>
3. Enter `python server.py -p <listening_port_number> -t <topology_file> -i <update_interval>` in the terminal. Alternatively, using `python server.py --help` will provide more information.<br>
4. After successfully running the command, use the `help` command to learn more how to use the program.<br>
