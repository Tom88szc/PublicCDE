import yaml
import pprint

# Przykładowa zawartość YAML
yaml_content = """
TCC: {"len": "1", "format": "b-1", "desc": "Transaction Category Code"}
SE009: {
    "len": "2",
    "format": "an-9",
    "desc": "Virtual Card Number Data",
    "SF001": {"len": "1", "format": "an-1", "desc": "Virtual Card Number Indicator"},
    "SF002": {"len": "LLVAR", "format": "n-19", "desc": "Virtual Card Number"},
    "SF003": {"len": "10", "format": "n-10", "desc": "Virtual Card Number Expiration Date"}
}
"""

# Wczytywanie zawartości YAML do słownika Pythona
data = yaml.safe_load(yaml_content)


class TLVParser:
    def __init__(self, tlv_string, schema):
        self.tlv_string = tlv_string
        self.schema = schema
        self.position = 0

    def parse(self):
        result = {}
        try:
            while self.position < len(self.tlv_string):
                tag = self.tlv_string[self.position:self.position + 4]
                self.position += 4
                if tag in self.schema:
                    length, value = self.parse_value(tag, self.schema[tag]['format'])
                    if tag == 'SE009':  # Jeśli to jest SE009, parsujemy jego sub-elementy
                        sub_elements = self.parse_sub_elements(value, self.schema[tag])
                        result[tag] = sub_elements
                    else:
                        result[tag] = value
                else:
                    raise ValueError(f"Unknown tag: {tag}")
            return result
        except Exception as e:
            print(f"Error parsing TLV string: {e}")
            return None

    def parse_value(self, tag, format):
        if format == 'LLVAR':
            length = int(self.tlv_string[self.position:self.position + 2], 16)
            self.position += 2
        elif format == 'LLLVAR':
            length = int(self.tlv_string[self.position:self.position + 3], 16)
            self.position += 3
        else:
            length = int(self.tlv_string[self.position:self.position + 2], 16)
            self.position += 2
        value = self.tlv_string[self.position:self.position + length * 2]
        self.position += length * 2
        return length, value

    def parse_sub_elements(self, value, schema):
        sub_result = {}
        sub_position = 0
        while sub_position < len(value):
            sub_tag = value[sub_position:sub_position + 5]
            sub_position += 5
            if sub_tag in schema:
                sub_length, sub_value = self.parse_sub_value(value, sub_position, schema[sub_tag]['format'])
                sub_result[sub_tag] = sub_value
                sub_position += sub_length * 2
            else:
                raise ValueError(f"Unknown sub-tag: {sub_tag}")
        return sub_result

    def parse_sub_value(self, value, sub_position, format):
        if format == 'LLVAR':
            length = int(value[sub_position:sub_position + 2], 16)
            sub_position += 2
        elif format == 'LLLVAR':
            length = int(value[sub_position:sub_position + 3], 16)
            sub_position += 3
        else:
            length = int(value[sub_position:sub_position + 2], 16)
            sub_position += 2
        sub_value = value[sub_position:sub_position + length * 2]
        return length, sub_value


# Przykładowy ciąg TLV
tlv_string = "TCC1000001SE009100SF001F131SF002LL19XXXXXXXXXXXXXXXXXXXXXXSF00300000000000000"

# Tworzenie instancji TLVParser i parsowanie danych
parser = TLVParser(tlv_string, data)
parsed_data = parser.parse()

# Wyświetlanie przetworzonych danych
pprint.pprint(parsed_data)


class TLVParser:
    def __init__(self, tlv_string):
        self.tlv_string = tlv_string
        self.position = 0

    def parse(self):
        result = {}
        while self.position < len(self.tlv_string):
            tag = self.tlv_string[self.position:self.position + 2]
            self.position += 2
            length = int(self.tlv_string[self.position:self.position + 2], 16)
            self.position += 2
            value = self.tlv_string[self.position:self.position + length * 2]
            self.position += length * 2
            result[tag] = {
                'length': length,
                'value': value
            }
        return result


# Example TLV string
tlv_string = "010300DEADBE020105031234"

# Create a TLVParser instance and parse the TLV string
parser = TLVParser(tlv_string)
parsed_data = parser.parse()

# Display the parsed data
import pprint

pprint.pprint(parsed_data)


def parse_tlv(input_string):
    """
    Parses a string in TLV (Tag-Length-Value) format.

    Args:
    input_string (str): The string to parse in TLV format.

    Returns:
    dict: A dictionary containing parsed TLV elements.

    TLV Format:
    - TAG: The first two characters indicating the type of subelement.
    - LENGTH: The next two characters indicating the length of the subelement's value.
    - VALUE: The value of the subelement with the length specified by LENGTH.
    """
    elements = {}

    while input_string:
        # First two characters are the TAG
        tag = input_string[:2]

        # Next two characters are the LENGTH
        length = int(input_string[2:4])

        # Next length characters are the VALUE
        value = input_string[4:4 + length]

        # Check if the value contains further TLV elements
        if len(value) > 4 and value[2:4].isdigit():
            value = parse_tlv(value)

        # Add the element to the dictionary
        elements[f'SE{tag}'] = value

        # Remove the processed element from the string
        input_string = input_string[4 + length:]

    return elements


def parse_de048(input_string):
    """
    Parses the DE048 field from an ISO 8583 message.

    Args:
    input_string (str): The string in DE048 format to parse.

    Returns:
    dict: A dictionary containing parsed elements of the DE048 field.

    DE048 Field Structure:
    - The first character is the TCC (Transaction Code Component), stored as SE001.
    - The remaining part is SUBELEMENTS, parsed as nested TLV structures.
    """
    # The first character is the TCC (Transaction Code Component)
    tcc = input_string[0]

    # The rest of the string is SUBELEMENTS
    subelements_str = input_string[1:]

    # Create the dictionary structure
    de048 = {
        "TCC": {
            "SE001": tcc
        },
        "SUBELEMENTS": parse_tlv(subelements_str)
    }

    return de048


# Example string
input_string = "R6645010110236635ffA72-05de-48ec-9517-4bef061c096a"

# Call the function
result = parse_de048(input_string)

# Print the result
import pprint

pprint.pprint(result)
