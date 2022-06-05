from PIL import Image

signature_string = "M4d3by51m0nCyb3r53c"


def encode(image, data_string, output_filename):
    # type (Image, String, String) -> None

    # String to be encoded: Add signature before and after data
    data_string = signature_string + data_string + signature_string
    # Convert string into bytes
    data_bytes = bytearray(data_string, 'utf-8')

    print(f'number of characters: {len(data_string)}')
    print('bytes needed per character: 8')
    print(f'bytes predicted total: {len(data_string) * 8}')

    # Binary keys to get each bit of a byte
    keys = bytearray()
    keys.append(0b1)
    keys.append(0b10)
    keys.append(0b100)
    keys.append(0b1000)
    keys.append(0b10000)
    keys.append(0b100000)
    keys.append(0b1000000)
    keys.append(0b10000000)

    # Now generate one byte for each bit
    counter = 0
    data_bits = bytearray()
    for byte in data_bytes:
        pos = 0
        for key in keys:
            # 1) Get each bit by "byte AND one of the keys" --> 1 byte produces 8 bytes
            data_bits.append(byte & key)
            # 2) shift that bit to the first position
            data_bits[counter] = data_bits[counter] >> pos
            pos += 1
            counter += 1

    print(f'bytes final total: {len(data_bits)}')

    # We want to embed our data into the red channel of rgb image data
    # Get list of all rgb pixels. Later we write the new red values back into it.
    pixels_rgb = list(image.getdata())
    # Get the red channel
    pixels_red = list(image.getdata(0))

    # Embed our data into the red channel and write it back into the list with all channels
    for i in range(len(data_bits)):
        # Set last bit of red byte to zero
        new_red = pixels_red[i] & 0b11111110
        # Add our data to the last bit using OR-operator --> last bit contains one bit of one character of our data
        new_red = new_red | data_bits[i]

        # Convert the pixels_rgb-tuple to a list, because a tuple can't be changed
        pixel = list(pixels_rgb[i])
        # Set new red pixel value
        pixel[0] = new_red
        # Convert the pixel back into a tuple and then wright it back into the original rgb data
        pixels_rgb[i] = tuple(pixel)

    # Write all channels back to image
    image.putdata(pixels_rgb)
    # Save image
    if output_filename is not None:
        print("[+] Saving image " + output_filename + " ...")
        image.save(output_filename)
    else:
        print("[+] Saving image NewImage.png ...")
        image.save("NewImage.png")


def decode(image):
    # type (Image) -> None

    # Signature String in bytes
    signature_bytes = bytearray(signature_string, 'utf-8')

    # Get red channel of all pixels
    image_data_red = list(image.getdata(0))

    # Generate the raw data bytes.
    # Therefore take the last bit of each of the red bytes and shift them to their correct position
    raw_bytes = bytearray()
    pos = 0
    for i in range(len(image_data_red)):  # range(0, 24):
        # print("i = {}".format(i))

        # Get the last bit of a byte by using AND-operator together with 0b1
        raw_bytes.append(image_data_red[i] & 0b1)
        # print("raw = " + bin(raw_bytes[i]))

        # Shift the bit to its correct position
        raw_bytes[i] = raw_bytes[i] << pos
        # print("shifted raw = " + bin(raw_bytes[i]))

        # After eight bits set position counter back to zero
        pos += 1
        if pos == 8:
            pos = 0

    # Combine 8 bytes to on byte using OR operator
    data_bytes = bytearray()
    counter = 0
    temp_byte = raw_bytes[0]
    bytes_iterator = iter(raw_bytes)
    while bytes_iterator:
        try:
            temp_byte = temp_byte | next(bytes_iterator)
            counter += 1
            if counter == 8:
                data_bytes.append(temp_byte)
                counter = 0
                temp_byte = 0
        except StopIteration:
            break

    # Find the two signature strings in the array and get the values in between them (which is the data)
    position_start = data_bytes.find(signature_bytes)
    position_end = data_bytes.find(signature_bytes, position_start + 1)
    data_bytes = data_bytes[position_start + len(signature_bytes):position_end]

    # Print start and stop position for debugging
    # print(f'start: {position_start}, end: {position_end}')

    if position_start >= 0:
        # Convert bytes to a string
        decoded_data = ""
        for k in range(len(data_bytes)):
            char = chr(data_bytes[k])
            decoded_data += char

        return decoded_data
    else:
        print("No data found!")
        return None
