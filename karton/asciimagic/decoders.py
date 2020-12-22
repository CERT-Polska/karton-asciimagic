import base64

from .asciiclassifier import AsciiType, clean_base64


def decode_base64(r_data, a_type):
    inp = r_data
    if a_type == AsciiType.BASE64_OBFUSCATED:
        inp = clean_base64(r_data)
    elif a_type == AsciiType.BASE64_REVERSED:
        inp = inp[::-1]
    return base64.b64decode(inp)


def decode_hex_ascii(r_data, a_type):
    if a_type == AsciiType.HEX_WITH_DASH:
        separator = b"-"
    elif a_type == AsciiType.HEX_WITH_SLASH:
        separator = b"\\x"
    else:
        raise RuntimeError("Unknown HEX type")
    inp = r_data.split(separator)
    return bytes(int(i, 16) for i in inp if i)


def decode_binary_ascii(r_data):
    inp = bytes(i for i in r_data if i in b"01")
    chunks = [inp[i : i + 8] for i in range(0, len(inp), 8)]
    return bytes(int(i, 2) for i in chunks if i)


def decode_decimal_ascii(r_data):
    inp = r_data.split(b",")
    return bytes(int(i) for i in inp if i)


class Decoder:
    def __init__(self, r_data, a_type):
        self.raw_data = r_data
        self.ascii_type = a_type
        self.decoded = b""

    def decode(self):
        if self.ascii_type == AsciiType.BINARY:
            self.decoded = decode_binary_ascii(self.raw_data)
        elif self.ascii_type == AsciiType.DECIMAL_COMMA_SEPARATED:
            self.decoded = decode_decimal_ascii(self.raw_data)
        elif self.ascii_type in [AsciiType.HEX_WITH_SLASH, AsciiType.HEX_WITH_DASH]:
            self.decoded = decode_hex_ascii(self.raw_data, self.ascii_type)
        elif self.ascii_type in [
            AsciiType.BASE64_PLAIN,
            AsciiType.BASE64_REVERSED,
            AsciiType.BASE64_OBFUSCATED,
        ]:
            self.decoded = decode_base64(self.raw_data, self.ascii_type)
        else:
            return

    def get_decoded(self):
        return self.decoded
