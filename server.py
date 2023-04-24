# Joshua Anthony Domantay
# Professor Senhua Yu
# COMP 429 - 16938
# 6 May 2023

import sys
import os
import _thread
import argparse
import time
from socket import *

my_id = -1
port = 0
servers = {}            # server_id : {ip, port} -> servers.get(server_id) = {"ip" : <ip_address>, "port" : <port_number>}
routing_table = {}      # From x to y link cost -> routing_table.get(x).get(y) = x to y cost. -1 = Infinity
neighbors = {}
packets = 0

def get_ip():
    hostname = gethostname()
    return gethostbyname(hostname)      # Return ip address

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

def valid_port(port):
    if(port.isdecimal()):
        n = int(port)
        if((n >= 0) and (n <= 65535)):
            return True
    return False

def check_connection(test_ip, test_port):
    try:
        test_socket = socket(AF_INET, SOCK_STREAM)
        test_socket.connect((test_ip, test_port))
        test_socket.close()
        return True
    except Exception as e:
        return False
    
def find_server_id(ip, port):
    for i in servers:
        if (str(servers.get(i).get("ip")) == str(ip)) and (int(servers.get(i).get("port")) == int(port)):
            return i
    return False
    
def parse_routing_table():
    val = ""
    for i in routing_table.get(my_id):
        val += "{}:{} ".format(i, routing_table.get(my_id).get(i))
    return val

def update_routing_table():
    for server in servers:
        if server != my_id:
            new_val = get_least_cost(server)
            if new_val != False:
                routing_table.get(my_id)[server] = new_val

def update_routing_table_received(id, data):
    for i in data:
        if len(i) > 0:
            data_val = i.split(":")
            routing_table.get(id)[int(data_val[0])] = int(data_val[1])

def fill_routing_table(server_ids):
    # Fill empty values of routing table
    for i in server_ids:
        if not routing_table.get(i):
            routing_table[i] = {}
        for j in server_ids:
            if (my_id == i) and (my_id == j):
                routing_table.get(i)[j] = 0     # Cost to self is 0
            elif not routing_table.get(i).get(j):
                routing_table.get(i)[j] = -1    # -1 = Infinity

# Bellman-Ford equation C(x,v)
def get_cost(server_id1, server_id2):
    return routing_table.get(server_id1)[server_id2]

# Bellman-Ford equation D_x(y) = min_v{c(x,v) + d_v(y)}
def get_least_cost(server_id2):
    all_cost = []
    for v in neighbors:
        val1 = neighbors.get(v)
        val2 = get_cost(v, server_id2)
        if (int(val1) != -1) and (int(val2) != -1):
            all_cost.append(neighbors.get(v) + get_cost(v, server_id2))
    if len(all_cost) > 0:
        return min(all_cost)
    return False

def read_topology(file_name):
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
    server_ids_recorded = []
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
            
            # Get my_id if ip and port matches
            if (server_ip == get_ip()) and (server_port == port):
                global my_id
                my_id = server_id

            # Check if data is already recorded
            for server in servers:
                # Check if server id is already recorded
                if server == int(server_id):
                    print("Topology file ERROR: Server id {} already contains an IP address and a port number".format(server_id))
                    return
                
                # Check if IP address and port number is already recorded
                if (servers.get(server).get("ip") == server_ip) and (servers.get(server).get("port") == server_port):
                    print("Topology file ERROR: Found duplicate IP address: {} and port number: {} for two server ids".format(server_ip, server_port))
                    return
                
            servers[server_id] = {"ip" : server_ip, "port" : server_port}
            num_servers -= 1

            server_ids_recorded.append(server_id)
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

            if server_id1 == my_id:
                neighbors[server_id2] = link_cost
            elif server_id2 == my_id:
                neighbors[server_id1] = link_cost

            routing_table.get(server_id1)[server_id2] = link_cost
            num_neighbors -= 1
        else:
            break       # Do not read other lines

    # If topology file is correct, num_neighbors should be 0
    # But program will still work even if num_neighbors > 0

    fill_routing_table(server_ids_recorded)

    return True

def create_topology(file_name):
    if not read_topology(file_name):    # Error reading topology file
        return False
    return True

def check_server_id_errors(server_id):
    if (not isinstance(server_id, int)) and (not server_id.isdigit()):
        return 2

    if not servers.get(server_id):
        return 1

    return 0
    
def check_server_id(server_id):
    error = check_server_id_errors(server_id)
    errorMsg = []
    if error == 2:
        errorMsg.append("Server id \"" + server_id + "\" is not a digit")
    elif error == 1:
        errorMsg.append("Cannot find server id \"" + server_id + "\"")
    else:
        return True
    return errorMsg

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
    print("help SUCCESS")

# Command update
def update(server_id1, server_id2, link_cost):
    # Check arguments for error
    valid = True
    errorMsg = []

    # Check if server_id1 is valid, else add to errorMsg
    check1 = check_server_id(int(server_id1))
    if check1 != True:
        for i in check1:
            errorMsg.append(i)
        valid = False

    # Check if server_id2 is valid, else add to errorMsg
    check2 = check_server_id(int(server_id2))
    if check2 != True:
        for i in check2:
            errorMsg.append(i)
        valid = False

    # Check if link_cost is valid
    if (not link_cost.isdigit()) and (link_cost.lower() != "inf"):
        errorMsg.append("Link cost must be a positive integer or infinity (inf)")
        valid = False

    if not valid:
        return errorMsg     # Return list of error messages
    
    # Update routing table
    val = link_cost
    if val.lower() == "inf":
        val = -1
    else:
        val = int(link_cost)
    routing_table.get(int(server_id1))[int(server_id2)] = val

    # Update neighbors
    if int(server_id1) == my_id:
        neighbors[int(server_id2)] = val
    else:
        send_msg(servers.get(int(server_id1)).get("ip"), servers.get(int(server_id1)).get("port"), "lcu", (str(server_id2) + " " + str(val)))
        
    if int(server_id2) == my_id:
        neighbors[int(server_id1)] = val
    else:
        send_msg(servers.get(int(server_id2)).get("ip"), servers.get(int(server_id2)).get("port"), "lcu", (str(server_id1) + " " + str(val)))

    return True

# Command step
def send_routing_update(server_call):
    update_routing_table()

    for i in servers:
        server_ip = servers.get(i).get("ip")
        server_port = servers.get(i).get("port")
        if (server_ip != get_ip()) or (server_port != port):    # Do not check self
            send_msg(server_ip, server_port, "pkt", parse_routing_table())

    if not server_call:
        print("step SUCCESS")

def send_msg(send_to_ip, send_to_port, msg_type, msg):
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((send_to_ip, send_to_port))
        msg = msg_type + " " + str(port) + " " + msg
        client_socket.send(msg.encode())
        client_socket.close()
    except Exception as e:
        pass    # TODO: Update routing table if no change after three update interval

# Command packets
def display_packets():
    print("Number of packets received: {}".format(packets))
    print("packets SUCCESS")

# Command display
def display_routing_table():
    # Print header
    print("".ljust(6), end="")
    for i in routing_table:
        print(str(i).ljust(6), end="")
    print()
    
    for i in routing_table:
        print(str(i).ljust(6), end="")
        for j in routing_table:
            val = routing_table.get(i)[j]
            if val == -1:
                val = "inf"
            print(str(val).ljust(6), end="")
        print()

    print("display SUCCESS")

# Command disable
def disable_server(server_id):
    checkId = check_server_id(server_id)
    if checkId != True:
        return checkId
    
    print("disable <server_id>")

# Command crash
def crash():
    print("crash SUCCESS")

def handle_input():
    while True:
        user_input = input(">> ")
        user_input = user_input.lower().split(" ")
        if user_input[0] == "help":
            list_commands()
        if user_input[0] == "update":
            if len(user_input) == 4:
                updated = update(user_input[1], user_input[2], user_input[3])
                if updated == True:
                    print("update SUCCESS")
                else:
                    print("update " + ". ".join(updated))
            else:
                print("update Please provide two server ids and link cost. Use \"help\" for more info")
        if user_input[0] == "step":
            send_routing_update(False)
        if user_input[0] == "packets":
            display_packets()
        if user_input[0] == "display":
            display_routing_table()
        if user_input[0] == "disable":
            if len(user_input) == 2:
                disabled = disable_server(user_input[1])
                if disabled == True:
                    print("disable SUCCESS")
                else:
                    print("disable " + ". ".join(disabled))
            else:
                print("disable Please provide server id. Use \"help\" for more info")
        if user_input[0] == "crash":
            crash()
            break
        print()

def setup_server():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((get_ip(), port))
    server_socket.listen(1)
    while True:
        conn_socket, addr = server_socket.accept()
        msg = conn_socket.recv(1024).decode()

        # Notify server and get routing table update
        msg = msg.split(" ")
        msg_type = msg[0]
        if msg_type == "pkt":
            rt_update = msg[2:]
            server_id = find_server_id(addr[0], msg[1])
            if server_id == False:
                server_id = "unknown server id"
            else:
                # Update routing_table with data received
                update_routing_table_received(server_id, rt_update)
                global packets
                packets += 1
            print("\nRECEIVED A MESSAGE FROM SERVER {}\n\n>> ".format(server_id), end="")
        elif msg_type == "lcu":
            server_id = int(msg[2])
            link_cost = int(msg[3])
            neighbors[int(server_id)] = link_cost
            print(neighbors)

        conn_socket.close()

def periodic_update(interval):
    last_update = time.time()
    while True:
        curr = time.time()
        if (curr - last_update) >= interval:
            send_routing_update(True)
            last_update = curr

def valid_args(args):
    valid = True    # Instead of returning immediately, use boolean so it prints all errors

    # Check first if args contain port number
    if args.port_number is None:
        print("Port number is missing")
        valid = False
    elif not valid_port(args.port_number):    # Check if port number is valid
        print("Port number is invalid")
        valid = False

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

def check_args(args):
    has_args = valid_args(args)
    if not has_args:        # Args not satisfied
        return False
    
    # Set port
    global port
    port = int(args.port_number)

    # Check if there is already a server in provided port number
    if check_connection(get_ip(), port):
        print("Port number is already being used")
        return False

    # Read topology file
    if not create_topology(args.topology_file_name):
        return False
    return True

def main(args):
    # Check if there are arguments
    if not check_args(args):
        print("Use -h or --help for more information")
        return 1
    interval = int(args.update_interval)
    _thread.start_new_thread(periodic_update, (interval,))      # Thread for periodic update
    _thread.start_new_thread(setup_server, ())                  # Thread for server (listening)
    handle_input()
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p",
                        dest="port_number",
                        help="port number for server")
    parser.add_argument("-t",
                        dest="topology_file_name",
                        help="topology file that contains initial topology configuration and link cost to neighbors")
    parser.add_argument("-i",
                        dest="update_interval",
                        help="time interval between routing updates in seconds")
    args = parser.parse_args()
    sys.exit(main(args))
