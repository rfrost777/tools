#!/usr/bin/env python3
##################################################
# CLI tool for base64 en-/decoding of strings
# using argparse is prob overkill, but anyways...
##################################################
import argparse
import base64


def main() -> None:
    mode = {
        "dec": "decode",
        "enc": "encode"
    }

    # set up parser and populate arguments...
    parser = argparse.ArgumentParser(description="Encode or decode base64.")
    parser.add_argument(
        "mode",
        type=str,
        choices=mode.keys(),
        help="Mode of operation."
    )
    parser.add_argument(
        "--urlsafe",
        action="store_true",
        dest="safe",
        help="Use filename/urlsafe mode."
    )
    parser.add_argument(
        "inputstring",
        type=str,
        help="Your string to encode/decode."
    )
    # parse arguments
    parsed_args = parser.parse_args()

    if parsed_args.mode == "enc":
        if parsed_args.safe:
            result = base64.urlsafe_b64encode(bytes(parsed_args.inputstring, "utf-8"))
        else:
            result = base64.b64encode(bytes(parsed_args.inputstring, 'utf-8'))

    else:
        if parsed_args.safe:
            result = base64.urlsafe_b64decode(bytes(parsed_args.inputstring, "utf-8"))
        else:
            result = base64.b64decode(bytes(parsed_args.inputstring, "utf-8"))

    print(f"Here's what I got: {result.decode()}")


if __name__ == '__main__':
    main()
