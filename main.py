import socket
import time

class BnetConnection:
    def send_logon_first(self, conn, addr):
        while True:
            try:
                for i in range(3):
                    conn.settimeout(10)
                    try:
                        data = conn.recv(1024)
                        if data:
                            hex_data_trimmed = data[4:]
                            bnet = BnetParserMessage(hex_data_trimmed)
                            print("send_messages")
                            encoded_message = bytes.fromhex(data)
                            conn.send(encoded_message)
                            return  # Zakończ, jeśli otrzymano odpowiedź
                    except socket.timeout:
                        print("brak odpowiedzi w ciągu 10 sekund, wysyłanie '0800'")
                        self.send_message(conn, self.mc_logon_request_0800())
                        time.sleep(10)  # Opcjonalnie dodaj opóźnienie między wiadomościami
                print("Koniec działania skryptu po trzykrotnym wysłaniu 'logon'")
                break
            except Exception as e:
                self.logger.error(f"Error sending message to {addr}: {e}")
                break

    def send_message(self, conn, hex_message):
        try:
            conn.sendall(hex_message)
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")

class BnetParserMessage:
    def __init__(self, data):
        # Twoja implementacja parsowania wiadomości
        pass

    def extract_fields(self):
        # Twoja implementacja ekstrakcji pól
        pass

# Przykład użycia
if __name__ == "__main__":
    server_address = ('localhost', 65432)
    message = b'0800'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(server_address)
        connection = BnetConnection()
        connection.send_logon_first(sock, server_address)
