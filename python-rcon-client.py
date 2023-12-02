import socket
import struct
import datetime

class RCONClient:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.socket = None

    def __enter__(self):
        self.connect()
        self.login()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self):
        """
        Establishes a TCP connection to the RCON server.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)  # Set timeout to 5 seconds
        try:
            self.socket.connect((self.host, self.port))
        except ConnectionRefusedError:
            print("Server is not reachable. Connection refused.")

    def login(self):
        """
        Performs login/authentication with the RCON server using the provided password.
        """
        if self.socket:
            try:
                packet = struct.pack('<3i', 10 + len(self.password), 0, 3) + self.password.encode('utf-8') + b'\x00\x00'
                self.socket.send(packet)
                response = self.socket.recv(4096)
                self.handle_response(response)
            except (socket.timeout, ConnectionAbortedError) as e:
                print(f"Error during login: {e}")

    def command(self, cmd):
        """
        Sends a command to the RCON server and processes the response.
        """
        try:
            packet = struct.pack('<3i', 10 + len(cmd), 0, 2) + cmd.encode('utf-8') + b'\x00\x00'
            self.socket.send(packet)
            response = self.socket.recv(4096)
            self.handle_response_with_log(cmd, response)
        except (socket.timeout, ConnectionAbortedError) as e:
            print(f"Error during command execution: {e}")

    def handle_response(self, response):
        """
        Handles the response received from the RCON server.
        """
        if response:
            try:
                decoded_response = response.decode('utf-8')
                print(decoded_response)
            except UnicodeDecodeError:
                print("Unable to decode response as UTF-8, printing hexadecimal representation:")
                print(response.hex())

    def handle_response_with_log(self, command, response):
        """
        Handles the response from the server and logs it with timestamp and command information.
        """
        if response:
            try:
                decoded_response = response.decode('utf-8').strip()
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{current_time} - Command: {command}\nResponse: {decoded_response}")
            except UnicodeDecodeError:
                hex_response = response.hex()
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{current_time} - Command: {command}\nUnable to decode response as UTF-8, printing hexadecimal representation:\n{hex_response}")

    def close(self):
        """
        Closes the socket connection to the RCON server.
        """
        if self.socket:
            self.socket.close()

# Usage example:
if __name__ == "__main__":
    with RCONClient('localhost', 27020, '12345') as rcon_client:
        rcon_client.command('listplayers')
