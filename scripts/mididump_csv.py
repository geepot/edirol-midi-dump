# This script takes a pasted MIDI Bulk Dump in the format of example_dump.txt, lists out each address and byte value in a nicely formatted list, and saves the output to a CSV file for easy parsing.
# If you prefer uppercase hexidecimal, make the changes to lines 52 and 60 as noted in the comments.

import csv

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
        if line == 'f0417f417f00000028122f7f000052f7': # Program will ignore this line and anything pasted after it
            break
    return input_lines

def save_memory_map_to_csv(memory_map, filename="memory_map.csv"):
    with open(filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Address", "Value"])
        for address, value in memory_map.items():
            csv_writer.writerow([f"{address:04x}", value]) # Change '04x' to '04X' for uppercase


midi_dump_lines = input_midi_dump()
memory_map = parse_midi_dump_input(midi_dump_lines)

print("Memory map:")
for address, value in memory_map.items():
    print(f"{address:04x}: {value}") # Change '04x' to '04X' for uppercase

save_memory_map_to_csv(memory_map)
print("Memory map saved to memory_map.csv")
