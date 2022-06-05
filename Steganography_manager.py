import argparse
import pathlib
from pathlib import Path
from PIL import Image
import base64
from PNGgraphy import *


def process(args, parser):
    """
    Process parsed commandline arguments.
    """
    # Default output file name
    default_filename = "NewCyberSec"

    # Calculate the number of bytes that can be embedded into the image
    image_byte_capacity = 0
    if args.image is not None:
        with Image.open(args.image) as image:
            print(f'image: {image.filename}')
            print(f'format: {image.format}')
            print(f'mode: {image.mode}')
            width, height = image.size
            print(f'width: {width}, height: {height}')

            image_byte_capacity = width * height
            print(f'image byte capacity: {image_byte_capacity}')

    # Data type is either 'm' for message or 'f' for file
    # Default input type and data
    input_type = 'm'
    input_data = ''

    # Check if encoding or decoding is specified
    if args.encode is True:

        # ---------------------------------------------------
        # ENCODING START
        # ---------------------------------------------------

        if args.message is not None:
            # Check if the message length is too big. 1 byte of data needs 8 bytes of the image
            if len(args.message) * 8 > image_byte_capacity:
                print("ERROR: Message is too long!")
                exit(1)
            else:
                # input data is "m" + the message
                input_type = 'm'
                input_data = input_type + args.message

        elif args.file is not None:
            input_type = 'f'

            # Check if file exists
            if Path(args.file).is_file():
                print("Input file exists")

                # Check if the file size is too big. 1 byte of data needs 8 bytes of the image
                if Path(args.file).stat().st_size * 8 > image_byte_capacity:
                    print("ERROR: Input file size is too big!")
                    exit(1)
                else:
                    # Open file in binary mode. Convert bytes to base64
                    with open(args.file, 'rb') as binary_file:
                        input_bytes = binary_file.read()
                        base64_encoded_bytes = base64.b64encode(input_bytes)
                        base64_message = base64_encoded_bytes.decode('utf-8')
                        # The input data is the data_type "f" + the above base64 string
                        input_data = input_type + base64_message
            else:
                print("ERROR: Input file does not exist")
                exit(1)
        else:
            print("ERROR: Specify the data to embed using -m or -f!")
            exit(1)

        if len(input_data) > 3:
            print("Input data: ")
            print(input_data[0])
            print(input_data[1])
            print(input_data[2])
            print(input_data[3])
        else:
            print("Input data bla blub")

        # ---------------------------------------------------
        # So now we got the input data and are able to encode
        # ---------------------------------------------------
        with Image.open(args.image) as image:
            print("[+] Encoding ...")
            if args.output is not None:
                encode(image, input_data, args.output)
            else:
                encode(image, input_data, default_filename+".png")
            print("[+] Done")

        # ---------------------------------------------------
        # ENCODING END
        # ---------------------------------------------------

    elif args.decode is True:

        # ---------------------------------------------------
        # DECODING START
        # ---------------------------------------------------
        decoded_data = ""
        with Image.open(args.image) as image:
            print("[+] Decoding ...")
            decoded_data = decode(image)
            print("[+] Done")
            print("[+] Analysing ...")

        if decoded_data is not None:

            # We got a simple message
            if decoded_data[0] == "m":
                print("We got a simple message")
                if args.output is not None:
                    with open(args.output, 'a') as out:
                        out.write(decoded_data[1:] + '\n')
                else:
                    print(decoded_data[1:])

            # We got a file
            elif decoded_data[0] == "f":
                print("We got a file")
                # Convert base64 to binary
                base64_encoded_bytes = decoded_data[1:].encode('utf-8')
                decoded_bytes = base64.decodebytes(base64_encoded_bytes)
                if args.output is not None:
                    with open(args.output, 'wb') as file_to_save:
                        file_to_save.write(decoded_bytes)
                else:
                    with open(default_filename+".txt", 'wb') as file_to_save:
                        file_to_save.write(decoded_bytes)
            else:
                print("ERROR: No file type specified!")
                print("Data gets dumped into error_log.txt")
                with open("error_log.txt", 'a') as out:
                    out.write(decoded_data + '\n')

        else:
            print("No data found!")

    else:
        parser.print_help()

    return 0


def steganography():
    # type () -> int
    parser = argparse.ArgumentParser()
    group1 = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument("image",
                        type=str,
                        help="image file")

    group1.add_argument("-e",
                        "--encode",
                        action='store_true',
                        help="encode")
    group1.add_argument("-d",
                        "--decode",
                        action='store_true',
                        help="decode")

    # parser.add_argument("-i",
    #                     "--image",
    #                     type=str,
    #                     required=True,
    #                     help="input image name or filepath")

    parser.add_argument("-o",
                        "--output",
                        type=str,
                        help="output image name or filepath")

    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument("-m",
                        "--message",
                        type=str,
                        help="message to be encoded.")
    group2.add_argument("-f",
                        "--file",
                        type=pathlib.Path,
                        help="file (name/path) to be encoded.")

    # Parse commandline arguments.
    args = parser.parse_args()

    return process(args, parser)
