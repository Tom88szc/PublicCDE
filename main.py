class BnetDe048Parser:
    def __init__(self):
        # Inicjalizacja słownika de_048_dict z definicjami struktur TLV
        self.de_048_dict = {
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
            },
            'SE42': {
                "len": "2", "format": "n-7", "desc": "Electronic Commerce Indicators",
                'SF01': {
                    "len": "2", "format": "n-3",
                    "desc": "Electronic Commerce Security Level Indicator and UCAF Collection Indicator",
                    'P01': {"len": "1", "format": "n-1", "desc": "Security Protocol"},
                    'P02': {"len": "1", "format": "n-1", "desc": "Cardholder Authentication"},
                    'P03': {"len": "1", "format": "n-1", "desc": "UCAF Collection Indicator"}
                },
                'SF02': {
                    "len": "2", "format": "n-3",
                    "desc": "Original Electronic Commerce Security Level Indicator and UCAF Collection Indicator",
                    'P01': {"len": "1", "format": "n-1", "desc": "Security Protocol"},
                    'P02': {"len": "1", "format": "n-1", "desc": "Cardholder Authentication"},
                    'P03': {"len": "1", "format": "n-1", "desc": "UCAF Collection Indicator"}
                },
                'SF03': {
                    "len": "2", "format": "n-1", "desc": "Reason for UCAF Collection Indicator Downgrade"
                }
            },
            'SE66': {
                'len': 'LLVAR',
                'format': 'an-45',
                'desc': 'PAN Mapping File Information',
                'SF01': {'len': '2', 'format': 'an-1', 'desc': 'Account Number Indicator'},
                'SF02': {'len': '2', 'format': 'ans-36', 'desc': 'Account Number'},
            },
        }

    def parse_tlv(self, input_string):
        """
        Parsuje string w formacie TLV (Tag-Length-Value) na podstawie podanej struktury słownika.

        Args:
            input_string (str): String do parsowania w formacie TLV.

        Returns:
            dict: Słownik zawierający sparsowane elementy TLV.

        Format TLV:
        - TAG: Pierwsze dwa znaki wskazujące typ podskładnika.
        - LENGTH: Kolejne dwa znaki wskazujące długość wartości podskładnika.
        - VALUE: Wartość podskładnika o długości określonej przez LENGTH.
        """
        elements = {}

        while input_string:
            # Pierwsze dwa znaki to TAG
            tag = input_string[:2]

            # Kolejne dwa znaki to LENGTH
            length = int(input_string[2:4])

            # Kolejne znaki o długości LENGTH to VALUE
            value = input_string[4:4 + length]

            # Dodanie elementu do słownika
            elements[f'SE{tag}'] = value

            # Usunięcie przetworzonego elementu ze stringa
            input_string = input_string[4 + length:]

        return elements

    def parse_subelements(self, subelements):
        """
        Parsuje podskładniki na podstawie struktury zdefiniowanej w słowniku de_048_dict.

        Args:
            subelements (dict): Słownik zawierający podskładniki do parsowania.

        Returns:
            dict: Słownik zawierający sparsowane podskładniki.
        """
        parsed_elements = {}
        for key, value in subelements.items():
            if key in self.de_048_dict:
                element_structure = self.de_048_dict[key]
                if isinstance(element_structure, dict) and len(element_structure) > 3:
                    nested_elements = self.parse_tlv(value)
                    parsed_elements[key] = nested_elements
                else:
                    parsed_elements[key] = value
            else:
                parsed_elements[key] = value
        return parsed_elements

    def parse_de048(self, input_string):
        """
        Parsuje string DE048 na słownik zawierający TCC i podskładniki.

        Args:
            input_string (str): String do parsowania.

        Returns:
            dict: Słownik zawierający TCC i podskładniki.
        """
        # Pierwszy znak to TCC (Transaction Code Component)
        tcc = input_string[0]

        # Reszta stringa to SUBELEMENTS
        subelements_str = input_string[1:]

        # Parsowanie podskładników
        subelements = self.parse_tlv(subelements_str)

        # Tworzenie struktury słownika
        de048 = {
            "TCC": {
                "SE001": tcc
            },
            "SUBELEMENTS": self.parse_subelements(subelements)
        }
        print(de048)
        return de048

    def dict_to_tlv(self, data_dict):
        """
        Konwertuje słownik z powrotem na string w formacie TLV.

        Args:
            data_dict (dict): Słownik do konwersji.

        Returns:
            str: String w formacie TLV.
        """
        def serialize_dict(d):
            """
            Rekurencyjnie konwertuje zagnieżdżone słowniki na string TLV.

            Args:
                d (dict): Zagnieżdżony słownik do konwersji.

            Returns:
                str: String w formacie TLV.
            """
            result = ""
            for k, v in d.items():
                if isinstance(v, dict):
                    nested_tlv = serialize_dict(v)
                    length = f"{len(nested_tlv):02}"
                    result += f"{k[2:]}{length}{nested_tlv}"
                else:
                    length = f"{len(v):02}"
                    result += f"{k[2:]}{length}{v}"
            return result

        tcc = data_dict['TCC']['SE001']
        subelements = data_dict['SUBELEMENTS']
        subelements_tlv = serialize_dict(subelements)
        return f"{tcc}{subelements_tlv}"


if __name__ == '__main__':
    input_dict = {
        'TCC': {'SE001': 'T'},
        'SUBELEMENTS': {
            'SE42': {'SE01': '212'},
            'SE43': 'kBRIUXRJAAAAAAAAAAAAAAAAAAAA',
            'SE66': {'SE01': '2', 'SE02': 'ab87147c-3844-46d5-9455-9d8d2c696dcf'}
        }
    }

    parser = BnetDe048Parser()
    tlv_string = parser.dict_to_tlv(input_dict)
    print(tlv_string)



    def create_message(self):
        bitmap = self.fields_to_bitmaps()
        message_data = ''
        for field, value in self.fields.items():
            if not isinstance(value, str):
                value = str(value)
            if field == 'DE001':
                continue
            field_info = PARSER_MESSAGE.get(field)
            if field_info is None:
                continue
            if field == 'DE048':
                # Jeśli pole to DE048, przekonwertuj wartość na string TLV
                value = self.dict_to_tlv(value)
            if field_info['len'].isnumeric():
                # Pole o stałej długości
                message_data += value
            else:
                # Pole o zmiennej długości
                length_indicator = str(len(value))
                if 'LLVAR' in field_info['len']:
                    message_data += length_indicator.zfill(2)
                elif 'LLLVAR' in field_info['len']:
                    message_data += length_indicator.zfill(3)
                message_data += value

        # Złączenie MTI, bitmap i danych polowych
        full_message = self.ascii_to_ebcdic(self.mtid) + bitmap + self.ascii_to_ebcdic(str(message_data).upper())
        return self.calculate_length_in_hex(full_message) + full_message