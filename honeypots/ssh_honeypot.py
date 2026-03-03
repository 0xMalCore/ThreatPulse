import socket
import threading
import paramiko
from analytics.parser import log_attack

HOST = "0.0.0.0"
PORT = 2222


class Server(paramiko.ServerInterface):

    def __init__(self, client_ip):
        self.client_ip = client_ip

    def check_auth_password(self, username, password):
        log_attack(self.client_ip, username, password, "SSH")
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    # 🔥 Allow PTY allocation
    def check_channel_pty_request(self, channel, term, width, height,
                                  pixelwidth, pixelheight, modes):
        return True

    # 🔥 Allow shell request
    def check_channel_shell_request(self, channel):
        return True


def fake_shell(channel, client_ip):
    channel.send("Welcome to Ubuntu 22.04 LTS (GNU/Linux x86_64)\r\n")
    channel.send("Last login: Thu Jun 20 12:45:23 2025\r\n")
    channel.send("root@server:~# ")

    buffer = ""

    while True:
        try:
            data = channel.recv(1024).decode("utf-8", errors="ignore")

            if not data:
                break

            for char in data:
                # Enter pressed
                if char == "\r" or char == "\n":
                    command = buffer.strip()
                    buffer = ""

                    if command:
                        log_attack(client_ip, "COMMAND", command, "SSH_CMD")

                        if command == "ls":
                            channel.send("\r\nbin  boot  dev  etc  home  var\r\n")

                        elif command == "whoami":
                            channel.send("\r\nroot\r\n")

                        elif command == "pwd":
                            channel.send("\r\n/root\r\n")

                        elif command.startswith("cat /etc/passwd"):
                            channel.send("\r\nroot:x:0:0:root:/root:/bin/bash\r\n")

                        elif command in ["exit", "logout"]:
                            channel.send("\r\nlogout\r\n")
                            channel.close()
                            return

                        else:
                            channel.send(f"\r\nbash: {command}: command not found\r\n")

                    channel.send("root@server:~# ")

                # Backspace handling
                elif char == "\x7f":
                    buffer = buffer[:-1]
                    channel.send("\b \b")

                else:
                    buffer += char
                    channel.send(char)

        except:
            break

    channel.close()


def handle_client(client, addr):
    transport = paramiko.Transport(client)

    # Generate temporary key (can make persistent later)
    host_key = paramiko.RSAKey.generate(2048)
    transport.add_server_key(host_key)

    server = Server(addr[0])

    try:
        transport.start_server(server=server)
        channel = transport.accept(20)

        if channel is None:
            return

        fake_shell(channel, addr[0])

    except Exception as e:
        print(f"[SSH ERROR] {e}")
    finally:
        transport.close()


def start_ssh():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(100)

    print(f"SSH Honeypot running on port {PORT}")

    while True:
        client, addr = sock.accept()
        threading.Thread(target=handle_client, args=(client, addr)).start()