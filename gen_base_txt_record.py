def get_input(prompt):
    return input(prompt)

def write_lengths_to_file(filename, values):
    with open(filename, 'w') as file:
        for value in values:
            length_hex = format(len(value), '02x')  # Length in hex
            value_ascii_hex = ''.join(format(ord(c), '02x') for c in value)  # ASCII to hex for each character
            file.write(f'{value}')

def write_values_to_file(filename, values):
    with open(filename, 'w') as file:
        for value in values:
            file.write(f'"{value}" ')  # Write the value directly

def main():
    values = []
    descriptions = [
        "Total length of the TXT field",
        "Total length of the TLSA field",
        "Version number",
        "TLS version",
        "Validity start date",
        "Validity end date",
        "Select Siganture algorihm \n 0. dil2 \n 1. dil3 \n 2. dil5 \n 3. fal512 \n 4. fal1024\n"
    ]

    print("Please enter the values for the following fields:")
    for description in descriptions:
        prompt = f"{description}: "
        values.append(get_input(prompt))
    
    filename_with_length = "ebox-need_for_sign.txt"
    filename_without_length = "TXT_EBOX-proto.txt"
    
    write_lengths_to_file(filename_with_length, values)
    write_values_to_file(filename_without_length, values)
    
    print(f"Files have been written to {filename_with_length} and {filename_without_length}")

if __name__ == "__main__":
    main()
