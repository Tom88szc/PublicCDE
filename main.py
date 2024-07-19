def create_message(self):
    bitmap = self.fields_to_bitmaps()
    message_data = ''
    for field, value in self.fields.items():
        if field == 'DE001':
            continue
        field_info = PARSER_MESSAGE.get(field)
        if field_info is None:
            continue
        if isinstance(value, dict):
            # Jeśli wartość jest słownikiem, przekonwertuj ją na string TLV
            value = self.dict_to_tlv_fields(value, field)
        if field_info['len'].isnumeric():
            # Pole o stałej długości
            message_data += value
        else:
            # Pole o zmiennej długości
            length_indicator = str(len(value))
            if field_info['len'] == 'LLVAR':
                message_data += length_indicator.zfill(2)
            elif field_info['len'] == 'LLLVAR':
                message_data += length_indicator.zfill(3)
            message_data += value

    # Złączenie MTI, bitmap i danych polowych
    full_message = self.ascii_to_ebcdic(self.mtid) + bitmap + self.ascii_to_ebcdic(str(message_data).upper())
    return self.calculate_length_in_hex(full_message) + full_message
