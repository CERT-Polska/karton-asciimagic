import re
from enum import Enum, auto, unique
from string import ascii_lowercase, ascii_uppercase, digits, hexdigits

BASE64_CHARS = (ascii_lowercase + ascii_uppercase + digits + "+/=").encode()


@unique
class AsciiType(Enum):
    BASE64_PLAIN = auto()
    BASE64_OBFUSCATED = auto()
    BASE64_REVERSED = auto()
    HEX_WITH_SLASH = auto()
    HEX_WITH_DASH = auto()
    BINARY = auto()
    DECIMAL_COMMA_SEPARATED = auto()
    UNKNOWN = auto()


def is_plain_base64(data):
    # Exclude reversed base64 with no padding
    if data[::-1][0:3] == b"TVq":
        return False
    return (
        re.match(b"([A-Za-z0-9+/]{4}){3,}([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?", data)
        and not len(data) % 4
    )


def clean_base64(data):
    bad_chars = set(data).difference(set(BASE64_CHARS))
    for i in bad_chars:
        data = data.replace(bytes([i]), b"A")
    return data


def is_obfuscated_base64(data):
    cleaned = clean_base64(data)
    return is_plain_base64(cleaned)


def is_reversed_base64(data):
    return is_plain_base64(data[::-1])


def is_decimal_ascii(chunk):
    return chunk.isdigit() and int(chunk) < 256


def is_hex_ascii(chunk):
    if len(chunk) != 2:
        return False
    return all(c in hexdigits.encode() for c in chunk)


def is_comma_separated_ascii(r_data, ascii_type):
    if ascii_type == AsciiType.DECIMAL_COMMA_SEPARATED:
        separator = b","
    elif ascii_type == AsciiType.HEX_WITH_SLASH:
        separator = b"\\x"
    elif ascii_type == AsciiType.HEX_WITH_DASH:
        separator = b"-"
    else:
        return False
    splitted = r_data.strip().split(separator)
    if len(splitted) <= 1:
        return False
    if ascii_type == AsciiType.DECIMAL_COMMA_SEPARATED:
        for i in splitted:
            if i and not is_decimal_ascii(i):
                return False
    else:
        for i in splitted:
            if i and not is_hex_ascii(i):
                return False
    return True


def is_binary(r_data):
    return all(c in b"01 " for c in r_data)


class AsciiClassifier:
    def __init__(self, r_data):
        self.raw_data = r_data
        self.verdict = AsciiType.UNKNOWN

    def classify(self):
        if is_binary(self.raw_data):
            self.verdict = AsciiType.BINARY
        elif is_comma_separated_ascii(self.raw_data, AsciiType.DECIMAL_COMMA_SEPARATED):
            self.verdict = AsciiType.DECIMAL_COMMA_SEPARATED
        elif is_comma_separated_ascii(self.raw_data, AsciiType.HEX_WITH_SLASH):
            self.verdict = AsciiType.HEX_WITH_SLASH
        elif is_comma_separated_ascii(self.raw_data, AsciiType.HEX_WITH_DASH):
            self.verdict = AsciiType.HEX_WITH_DASH
        elif is_plain_base64(self.raw_data):
            self.verdict = AsciiType.BASE64_PLAIN
        elif is_reversed_base64(self.raw_data):
            self.verdict = AsciiType.BASE64_REVERSED
        elif is_obfuscated_base64(self.raw_data):
            self.verdict = AsciiType.BASE64_OBFUSCATED
        else:
            return

    def get_verdict(self):
        return self.verdict
