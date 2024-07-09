def parse_tlv(input_string):
    elements = {}

    while input_string:
        # Pierwsze dwa znaki to TAG
        tag = input_string[:2]

        # Kolejne dwa znaki to LENGTH
        length = int(input_string[2:4])

        # Następne length znaków to VALUE
        value = input_string[4:4 + length]

        # Sprawdzenie, czy wartość zawiera dalsze TLV
        if len(value) > 4 and value[2:4].isdigit():
            value = parse_tlv(value)

        # Dodanie elementu do słownika
        elements[f'SE{tag}'] = value

        # Usunięcie przetworzonego elementu z ciągu
        input_string = input_string[4 + length:]

    return elements


def parse_de048(input_string):
    # Pierwszy znak to TCC (Transaction Code Component)
    tcc = input_string[0]

    # Reszta ciągu to SUBELEMENTS
    subelements_str = input_string[1:]

    # Tworzenie struktury słownikowej
    de048 = {
        "TCC": {
            "SE001": tcc
        },
        "SUBELEMENTS": parse_tlv(subelements_str)
    }

    return de048


# Przykładowy ciąg
input_string = "R6645010110236635ffA72-05de-48ec-9517-4bef061c096a"

# Wywołanie funkcji
result = parse_de048(input_string)

# Wyświetlenie wyniku
import pprint

pprint.pprint(result)
