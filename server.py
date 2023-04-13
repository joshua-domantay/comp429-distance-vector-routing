# Joshua Anthony Domantay
# Professor Senhua Yu
# COMP 429 - 16938
# 6 May 2023

import sys
import os
import argparse

# Help command
def list_commands():
    pass

def handle_input():
    while True:
        user_input = input(">> ")
        user_input = user_input.lower().split(" ")

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
    print("SUCCESS")
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
