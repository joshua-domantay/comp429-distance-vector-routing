# Joshua Anthony Domantay
# Professor Senhua Yu
# COMP 429 - 16938
# 6 May 2023

import sys
import os
import argparse

servers = {}            # server_id : (ip, port) -> servers.get(server_id) = (IP address, port number)
routing_table = {}      # From x to y link cost -> routing_table.get(x).get(y) = x to y cost

def valid_ip(ip_addr):
    ip_addr_split = ip_addr.split(".")
    if len(ip_addr_split) != 4:
        return False
    for i in ip_addr_split:
        if not i.isdigit():
            return False
        if int(i) > 255:
            return False
    return True

def create_topology(file_name):
    topology_file = open(file_name, 'r')
    topology_file_contents = []
    for line in topology_file.readlines():
        topology_file_contents.append(line.strip())
    topology_file.close()
    
    # Error checking for number of servers and number of edges/neighbors
    if not topology_file_contents[0].isdigit():
        print("Topology file ERROR: Expected positive integer for number of servers")
        return
    if not topology_file_contents[1].isdigit():
        print("Topology file ERROR: Expected positive integer for number of edges neighbors")
        return
    
    num_servers = int(topology_file_contents[0])
    num_neighbors = int(topology_file_contents[1])
    for i in range(2, len(topology_file_contents)):
        line = topology_file_contents[i]
        if num_servers > 0:
            server_ip_port = line.split(" ")

            # Check if line follows format <server_id> <ip_address> <port_number>
            if (len(server_ip_port) != 3) or (not server_ip_port[0].isdigit()) or (not valid_ip(server_ip_port[1])) or (not server_ip_port[2].isdigit()):
                print("Topology file ERROR: Line {} should contain <server_id> <ip_address> <port_number>".format(i + 1))
                return
            
            server_id = int(server_ip_port[0])
            server_ip = server_ip_port[1]
            server_port = int(server_ip_port[2])
            
            # Check connection
            # TODO: socket
            #     print("Topology file ERROR: Cannot connect to IP address: {} with port number: {}".format())
            #     return

            for server in servers:
                # Check if server id is already recorded
                if server == int(server_id):
                    print("Topology file ERROR: Server id {} already contains an IP address and a port number".format(server_id))
                    return
                
                # Check if IP address and port number is already recorded
                if (servers.get(server)[0] == server_ip) and (servers.get(server)[1] == server_port):
                    print("Topology file ERROR: Found duplicate IP address: {} and port number: {} for two server ids".format(server_ip, server_port))
                    return
                
            servers[server_id] = (server_ip, server_port)
            num_servers -= 1
        elif num_neighbors > 0:
            server1_server2_cost = line.split(" ")

            # Check if line follows format <server_id1> <server_id2> <link_cost>
            if (len(server1_server2_cost) != 3) or (not server1_server2_cost[0].isdigit()) or (not server1_server2_cost[1].isdigit()) or (not server1_server2_cost[2].isdigit()):
                print("Topology file ERROR: Line {} should contain <server_id1> <server_id2> <link_cost>".format(i + 1))
                return
            
            server_id1 = int(server1_server2_cost[0])
            server_id2 = int(server1_server2_cost[1])
            link_cost = int(server1_server2_cost[2])

            # Check if server id 1 and server id 2 already have link cost
            if routing_table.get(server_id1):
                if routing_table.get(server_id1).get(server_id2):
                    print("Topology file ERROR: Server id {} already has link cost to server id {}".format(server_id1, server_id2))
                    return
            else:
                routing_table[server_id1] = {}      # Make new row

            routing_table.get(server_id1)[server_id2] = link_cost
            num_neighbors -= 1
        else:
            break       # Do not read other lines

    # If topology file is correct, num_neighbors should be 0
    # But program will still work even if num_neighbors > 0
    return True

def check_server_id_errors(server_id):
    if not server_id.isdigit():
        return 2

    # TODO: Check if server_id is in topology
    # if
    # return 1

    return 0
    
def check_server_id(server_id):
    error = check_server_id_errors(server_id)
    if error == 2:
        print("Server id \"" + server_id + "\" is not a digit")
    elif error == 1:
        print("Cannot find server id \"" + server_id + "\"")
    else:
        return True

# Command help
def list_commands():
    print("update <server_id1> <server_id2> <link_cost>")
    print("  > Set the link cost between server_id1 and server_id2 to link_cost. Link cost must be a positive integer or infinity (inf)")
    print("step")
    print("  > Send routing update to neighbors")
    print("packets")
    print("  > Display the number of distance vector (packets) this server has received since last invocation of this information")
    print("display")
    print("  > Display the current routing table, including current and neighboring nodes' distance vector")
    print("disable <server_id>")
    print("  > Disable the link to a given server")
    print("crash")
    print("  > Close all connections on all links (simulate server crashes)")
    print()

# Command update
def update(server_id1, server_id2, link_cost):
    # Check arguments
    valid = True
    if not check_server_id(server_id1):
        valid = False
    if not check_server_id(server_id2):
        valid = False
    if not link_cost.isdigit():
        print("Link cost must be a positive integer or infinity (inf)")
        valid = False
    if not valid:
        return
    
    print("update <server_id1> <server_id2> <link_cost>")

# Command step
def send_routing_update():
    print("step")

# Command packets
def display_packets():
    print("packets")

# Command display
def display_routing_table():
    print("display")

# Command disable
def disable_server(server_id):
    if not check_server_id(server_id):
        return
    print("disable <server_id>")

# Command crash
def crash():
    print("crash")

def handle_input():
    while True:
        user_input = input(">> ")
        user_input = user_input.lower().split(" ")
        if user_input[0] == "help":
            list_commands()
        if user_input[0] == "update":
            if len(user_input) == 4:
                update(user_input[1], user_input[2], user_input[3])
            else:
                print("Please provide two server ids and link cost. Use \"help\" for more info")
        if user_input[0] == "step":
            send_routing_update()
        if user_input[0] == "packets":
            display_packets()
        if user_input[0] == "display":
            display_routing_table()
        if user_input[0] == "disable":
            if len(user_input) == 2:
                disable_server(user_input[1])
            else:
                print("Please provide server id. Use \"help\" for more info")
        if user_input[0] == "crash":
            crash()
        print()

def valid_args(args):
    valid = True    # Instead of returning immediately, use boolean so it prints all errors

    # Check if all args satisfied
    if (args.topology_file_name is None) or (args.update_interval is None):
        if args.topology_file_name is None:
            print("Topology file name must be specified (-t)")
        if args.update_interval is None:
            print("Routing update interval must be specified (-i)")
        valid = False
    
    # Check if topology file exists
    if args.topology_file_name:
        # Check if provided topology file has extension ".txt"
        if args.topology_file_name[(len(args.topology_file_name) - 4):] != ".txt":
            args.topology_file_name = (args.topology_file_name + ".txt")

        if not os.path.exists(args.topology_file_name):
            print("Topology file cannot be found")
            valid = False

    # Check if update interval is digit
    if args.update_interval:
        try:
            float(args.update_interval)
        except:
            print("Time interval must be a number")
            valid = False

    return valid

def main(args):
    # Check if argument is missing
    if not valid_args(args):
        return 1
    if not create_topology(args.topology_file_name):
        return 1
    handle_input()
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t",
                        dest="topology_file_name",
                        help="topology file that contains initial topology configuration and link cost to neighbors")
    parser.add_argument("-i",
                        dest="update_interval",
                        help="time interval between routing updates in seconds")
    args = parser.parse_args()
    sys.exit(main(args))
