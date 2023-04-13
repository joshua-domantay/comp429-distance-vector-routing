# Joshua Anthony Domantay
# Professor Senhua Yu
# COMP 429 - 16938
# 6 May 2023

import sys
import os
import argparse

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
    if (not link_cost.isdigit()):
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
            print("Topology file must be specified (-t)")
        if args.update_interval is None:
            print("Routing update interval must be specified (-i)")
        valid = False
    
    # Check if topology file exists
    if (args.topology_file_name) and (not os.path.exists(args.topology_file_name)):
        print("Topology file is missing")
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
