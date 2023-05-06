# This script takes two pasted MIDI Bulk Dumps in the format of example_dump.txt and outputs the changed bytes and their addresses.
# If you prefer uppercase hexidecimal, make the changes to lines 67 and 73 as noted in the comments.

import sys

def parse_midi_dump(midi_dump):
    discarded_string = "f0417f417f0000002812"
    if midi_dump.startswith(discarded_string):
        midi_dump = midi_dump[len(discarded_string):]

    starting_address = midi_dump[:6]
    midi_dump = midi_dump[6:]

    end_of_message_marker = "f7"
    end_of_message_index = midi_dump.find(end_of_message_marker)

    checksum = midi_dump[end_of_message_index - 2:end_of_message_index]
    data = midi_dump[:end_of_message_index - 2]

    return starting_address, data, checksum


def parse_midi_dump_input(input_lines):
    memory_map = {}
    for midi_dump in input_lines:
        starting_address, data, checksum = parse_midi_dump(midi_dump)
        address = int(starting_address, 16)
        data_bytes = [data[i:i+2] for i in range(0, len(data), 2)]
        for byte in data_bytes:
            memory_map[address] = byte
            address += 1
    return memory_map

def input_midi_dump():
    input_lines = []
    print("Please paste the MIDI dump and press Enter. The program will process the input once it encounters the end-of-dump marker:")
    while True:
        line = input().strip()
        input_lines.append(line)
        if line == 'f0417f417f00000028122f7f000052f7':
            break
    return input_lines

def compare_memory_maps(map1, map2):
    differing_addresses = set(map1.keys()) & set(map2.keys())
    differences = []
    for address in differing_addresses:
        if map1[address] != map2[address]:
            differences.append((address, map1[address], map2[address]))
    return differences

print("Enter the first MIDI dump:")
midi_dump_lines1 = input_midi_dump()
memory_map1 = parse_midi_dump_input(midi_dump_lines1)

print("Enter the second MIDI dump:")
midi_dump_lines2 = input_midi_dump()
memory_map2 = parse_midi_dump_input(midi_dump_lines2)

differences = compare_memory_maps(memory_map1, memory_map2)

if not differences:
    print("No differences found between the two memory maps.")
else:
    print("Differences found:")
    for address, value1, value2 in differences:
        print(f"Address: {address:04x}, Values: {value1} - {value2}") # Change '04x' to '04X' for uppercase

    setting_name = input("Enter the name of the setting: ")

    print(f"Address location and data value for '{setting_name}':") # Todo: make this output and append to a text file
    for address, value1, value2 in differences:
        print(f"Address: {address:04x}, Values: {value1} - {value2}") # Change '04x' to '04X' for uppercase