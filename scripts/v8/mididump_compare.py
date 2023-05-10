import mido
import csv
from collections import OrderedDict

def get_midi_device():
    input_names = mido.get_input_names()
    print("Available MIDI devices:")

    for i, name in enumerate(input_names, start=1):
        print(f"{i}. {name}")

    device_index = int(input("Enter the number of the MIDI device you'd like to use: ")) - 1

    return mido.open_input(input_names[device_index])

def get_midi_dump(port):
    midi_dump = ""
    raw_dump = []
    print("Waiting for MIDI dump...")
    while True:
        msg = port.receive()
        # print("[DEBUG] Received MIDI message:", msg)
        if msg.type == 'sysex':
            hex_msg = ''.join(f"{byte:02X}" for byte in msg.data)
            print(hex_msg)
            if hex_msg == '417F000028122F7F000052':
                break
            midi_dump += hex_msg + "\n"  # Add newline after each message
    return midi_dump

def send_midi_dump(raw_dump, midi_port): # This is definitely still broken
    for msg in raw_dump:
        message = mido.Message.from_hex(msg)
        print(message)
    
    # print('sysex', bytes.from_hex("417F000028122F7F000052"))
    # midi_port.send(mido.Message.from_hex())

def parse_midi_dump(midi_dump):
    dump_lines = midi_dump.strip().split("\n")
    parsed_lines = []

    for line in dump_lines:
        if not line.startswith("417F00002812"):
            continue
        parsed_line = []
        for i in range(12, len(line) - 2, 2):
            parsed_line.append(int(line[i : i + 2], 16))
            # print("[DEBUG] parsed_line: ", parsed_line)
        parsed_lines.append(parsed_line)

    return parsed_lines

def map_memory_space(parsed_dump):
    memory_space = OrderedDict()
    for line in parsed_dump:
        # print("[DEBUG] Line: ", line)
        address = (line[0] << 16) | (line[1] << 8) | line[2] # Calculate starting address based on first three bytes of the line
        # print("[DEBUG] Address: ", hex(address))
        for value in line[3:-1]:
            memory_space[address] = value
            address += 1
    return memory_space

def save_setting_to_csv(setting_name, addresses, original_values, min_values, max_values, special_notes, filename="settings.csv"):
    with open(filename, "a", newline="") as csvfile:
        fieldnames = ["Setting", "Address", "Original", "Minimum", "Maximum", "Special Notes"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for address, original, minimum, maximum, note in zip(addresses, original_values, min_values, max_values, special_notes):
            writer.writerow({
                "Setting": setting_name,
                "Address": f"{address:06X}",
                "Original": f"{original:02X}",
                "Minimum": f"{minimum:02X}",
                "Maximum": f"{maximum:02X}",
                "Special Notes": note
            })

# Main program
midi_port = get_midi_device()

print("\nDo not modify any settings, this dump will be used as a baseline for comparison.")      
original_dump = get_midi_dump(midi_port)

original_memory_space = map_memory_space(parse_midi_dump(original_dump))

while True:
    setting_name = input("Enter the name of the setting you want to record: ")
    print("\nPlease set the setting at its minimum value.")
    min_value_dump = get_midi_dump(midi_port)
    min_memory_space = map_memory_space(parse_midi_dump(min_value_dump))

    print("\nPlease set the setting at its maximum value.")
    max_value_dump = get_midi_dump(midi_port)
    max_memory_space = map_memory_space(parse_midi_dump(max_value_dump))

    changed_addresses = []
    original_values = []
    min_values = []
    max_values = []
    
    for address in original_memory_space.keys():
        if original_memory_space[address] != min_memory_space[address] or original_memory_space[address] != max_memory_space[address]:
            changed_addresses.append(address)
            original_values.append(original_memory_space[address])
            min_values.append(min_memory_space[address])
            max_values.append(max_memory_space[address])

    special_notes = []
    for address, original, minimum, maximum in zip(changed_addresses, original_values, min_values, max_values):
        print(f"Address: {address:06X}, Original: {original:02X}, Minimum: {minimum:02X}, Maximum: {maximum:02X}")
        note = input("Enter any special notes for this address (leave empty if none): ")
        special_notes.append(note)

    print("\nSaving the following information to the CSV file:")
    print("Setting:", setting_name)
    for address, original, minimum, maximum, note in zip(changed_addresses, original_values, min_values, max_values, special_notes):
        print(f"Address: {address:06X}, Original: {original:02X}, Minimum: {minimum:02X}, Maximum: {maximum:02X}, Special Notes: {note}")

    correct = input("Is this information correct? (y/n): ")
    if correct.lower() == 'y':
        save_setting_to_csv(setting_name, changed_addresses, original_values, min_values, max_values, special_notes)

    another_setting = input("Do you want to record another setting? (y/n): ")
    if another_setting.lower() != "y":
        ### BROKEN ###
        # write_back = input("Do you want to write back your original settings? (y/n): ")
        # if write_back.lower() == "y":
        #     send_midi_dump(original_dump, midi_port)
        break