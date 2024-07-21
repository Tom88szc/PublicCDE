from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad


def create_iso_0_pin_block(pin, pan):
    # Sprawdzenie długości PIN-u
    if not (4 <= len(pin) <= 12):
        raise ValueError("PIN musi mieć od 4 do 12 cyfr")

    # Sprawdzenie długości PAN-u
    if len(pan) < 13:
        raise ValueError("PAN musi mieć co najmniej 13 cyfr")

    # Utworzenie bloku PIN
    pin_block = f"{len(pin):X}{pin}".ljust(16, 'F')

    # Wyciągnięcie 12 ostatnich cyfr PAN-u (bez ostatniej cyfry kontrolnej)
    pan_part = f"0000{pan[-13:-1]}"

    # XORowanie bloku PIN i PAN
    pin_block_int = int(pin_block, 16)
    pan_part_int = int(pan_part, 16)
    result = pin_block_int ^ pan_part_int

    # Konwersja wyniku do formatu heksadecymalnego
    return f"{result:016X}"


# Testowanie funkcji
pin = "1234"
pan = "5432101234567891"
print(create_iso_0_pin_block(pin, pan))


def encrypt_pin_block(pin_block, key):
    # Konwersja klucza i bloku PIN do postaci bajtowej
    key_bytes = bytes.fromhex(key)
    pin_block_bytes = bytes.fromhex(pin_block)

    # Utworzenie obiektu szyfrującego 3DES
    cipher = DES3.new(key_bytes, DES3.MODE_ECB)

    # Szyfrowanie bloku PIN z dopełnieniem
    encrypted_pin_block = cipher.encrypt(pad(pin_block_bytes, DES3.block_size))

    # Konwersja zaszyfrowanego bloku PIN do postaci heksadecymalnej
    return encrypted_pin_block.hex().upper()


# Testowanie funkcji
pin_block = create_iso_0_pin_block("1234", "5432101234567891")
key = "0123456789ABCDEFFEDCBA9876543210"
encrypted_pin_block = encrypt_pin_block(pin_block, key)
print(encrypted_pin_block)


def decrypt_pin_block(encrypted_pin_block, key):
    # Konwersja klucza i zaszyfrowanego bloku PIN do postaci bajtowej
    key_bytes = bytes.fromhex(key)
    encrypted_pin_block_bytes = bytes.fromhex(encrypted_pin_block)

    # Utworzenie obiektu deszyfrującego 3DES
    cipher = DES3.new(key_bytes, DES3.MODE_ECB)

    # Deszyfrowanie bloku PIN
    decrypted_pin_block_bytes = unpad(cipher.decrypt(encrypted_pin_block_bytes), DES3.block_size)

    # Konwersja odszyfrowanego bloku PIN do postaci heksadecymalnej
    return decrypted_pin_block_bytes.hex().upper()

# Testowanie funkcji
decrypted_pin_block = decrypt_pin_block(encrypted_pin_block, key)
print(decrypted_pin_block)
