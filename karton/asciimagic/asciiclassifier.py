from .checks import *


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
