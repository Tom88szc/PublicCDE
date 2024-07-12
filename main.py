def parse_tlv(input_string, structure_dict=None):
    """
    Parses a string in TLV (Tag-Length-Value) format based on the provided structure dictionary.

    Args:
    input_string (str): The string to parse in TLV format.
    structure_dict (dict): The dictionary defining the structure of the TLV elements.

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

        # Add the element to the dictionary
        elements[f'SE{tag}'] = value

        # Remove the processed element from the string
        input_string = input_string[4 + length:]

    return elements


def parse_subelements(subelements, structure_dict):
    parsed_elements = {}
    for key, value in subelements.items():
        if key in structure_dict:
            element_structure = structure_dict[key]
            if isinstance(element_structure, dict):
                nested_elements = parse_tlv(value, element_structure)
                parsed_elements[key] = nested_elements
            else:
                parsed_elements[key] = value
        else:
            parsed_elements[key] = value
    return parsed_elements


def parse_de048(input_string, structure_dict):
    """
    Parses the DE048 field from an ISO 8583 message.

    Args:
    input_string (str): The string in DE048 format to parse.
    structure_dict (dict): The dictionary defining the structure of the DE048 field.

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

    # Parse the subelements
    subelements = parse_tlv(subelements_str)

    # Create the dictionary structure
    de048 = {
        "TCC": {
            "SE001": tcc
        },
        "SUBELEMENTS": parse_subelements(subelements, structure_dict)
    }

    return de048


# Define the DE048 structure
de048_dict = {
    'SE33': {
        'len': 'LLVAR',
        'format': 'an-93',
        'desc': 'PAN Mapping File Information',
        'SF01': {'len': '1', 'format': 'an-1', 'desc': 'Account Number Indicator'},
        'SF02': {'len': 'LLVAR', 'format': 'n-19', 'desc': 'Account Number'},
        'SF03': {'len': '2', 'format': 'an-4', 'desc': 'Expiration Date'},
        'SF04': {'len': '2', 'format': 'an-3', 'desc': 'Product Code'},
        'SF05': {'len': '2', 'format': 'n-2', 'desc': 'Token Assurance Method'},
        'SF06': {'len': '2', 'format': 'n-11', 'desc': 'Token Requestor ID'},
        'SF07': {'len': 'LLVAR', 'format': 'n-19', 'desc': 'Primary Account Number, Account Range'},
        'SF08': {'len': '2', 'format': 'an-2', 'desc': 'Storage Technology'}
    }
}

# Example input string in DE048 format
input_string = "T230201260321633260101H0611012345678900802039203857"

# Call the parse_de048 function with the DE048 structure
result = parse_de048(input_string, de048_dict)

# Print the result using pprint for better readability
import pprint
pprint.pprint(result)

########################################################################################################################

def build_tlv(elements, structure_dict=None):
    """
    Builds a TLV string from a dictionary of elements based on the provided structure dictionary.

    Args:
    elements (dict): The dictionary of elements to convert to TLV format.
    structure_dict (dict): The dictionary defining the structure of the TLV elements.

    Returns:
    str: The TLV string representation of the elements.
    """
    tlv_string = ""
    for key, value in elements.items():
        tag = key[2:]  # Remove 'SE' prefix
        if isinstance(value, dict):
            # Handle nested structure
            sub_tlv = build_tlv(value, structure_dict.get(key, {}))
            length = len(sub_tlv)
            tlv_string += f"{tag}{length:02d}{sub_tlv}"
        else:
            length = len(value)
            tlv_string += f"{tag}{length:02d}{value}"
    return tlv_string

def build_de048(de048_dict, structure_dict):
    """
    Builds a DE048 TLV string from a dictionary of DE048 elements.

    Args:
    de048_dict (dict): The dictionary of DE048 elements to convert to TLV format.
    structure_dict (dict): The dictionary defining the structure of the DE048 field.

    Returns:
    str: The DE048 TLV string representation of the elements.
    """
    tcc = de048_dict["TCC"]["SE001"]
    subelements = de048_dict["SUBELEMENTS"]
    subelements_tlv = build_tlv(subelements, structure_dict)
    return f"{tcc}{subelements_tlv}"

# Define the DE048 structure
de048_dict_structure = {
    'SE33': {
        'len': 'LLVAR',
        'format': 'an-93',
        'desc': 'PAN Mapping File Information',
        'SF01': {'len': '1', 'format': 'an-1', 'desc': 'Account Number Indicator'},
        'SF02': {'len': 'LLVAR', 'format': 'n-19', 'desc': 'Account Number'},
        'SF03': {'len': '2', 'format': 'an-4', 'desc': 'Expiration Date'},
        'SF04': {'len': '2', 'format': 'an-3', 'desc': 'Product Code'},
        'SF05': {'len': '2', 'format': 'n-2', 'desc': 'Token Assurance Method'},
        'SF06': {'len': '2', 'format': 'n-11', 'desc': 'Token Requestor ID'},
        'SF07': {'len': 'LLVAR', 'format': 'n-19', 'desc': 'Primary Account Number, Account Range'},
        'SF08': {'len': '2', 'format': 'an-2', 'desc': 'Storage Technology'}
    }
}

# Example dictionary input
de048_dict = {
    'SUBELEMENTS': {
        'SE23': '01',
        'SE26': '216',
        'SE33': {'SE01': 'H', 'SE06': '01234567890', 'SE08': '03'},
        'SE92': '857'
    },
    'TCC': {'SE001': 'T'}
}

# Convert the dictionary back to a TLV string
tlv_string = build_de048(de048_dict, de048_dict_structure)
print(tlv_string)


#######################################################################################################


def parse_subelements(self, subelements):
    parsed_elements = {}

    for se, se_value in subelements.items():
        if se in self.de_048_dict:
            element_structure = self.de_048_dict[se]

            if isinstance(element_structure, dict):
                # Rozpoznawanie SE
                nested_elements = self.parse_tlv_sub(se_value, self.de_048_dict[se]['len'])
                parsed_elements[se] = nested_elements

                # Przetwarzanie subfields (SF)
                for sf, sf_value in nested_elements.items():
                    if sf.startswith("SF"):
                        subfield_structure = self.de_048_dict[se][sf]
                        if isinstance(subfield_structure, dict):
                            parsed_elements[sf] = self.parse_tlv_sub(sf_value, subfield_structure['len'])
                        else:
                            parsed_elements[sf] = sf_value
            else:
                parsed_elements[se] = se_value
        else:
            parsed_elements[se] = se_value

    return parsed_elements
