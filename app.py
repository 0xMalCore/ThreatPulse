from analytics.parser import init_db
from honeypots.ssh_honeypot import start_ssh
from honeypots.http_honeypot import start_http
import threading
import socket


def get_local_ip():
    """Get local IP address for display"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


if __name__ == "__main__":
    init_db()

    # Start SSH Honeypot
    threading.Thread(target=start_ssh, daemon=True).start()

    # Start HTTP Honeypot
    threading.Thread(target=start_http, daemon=True).start()

    local_ip = get_local_ip()

    print("\n" + "=" * 60)
    print(" Intelligent Honeypot System Running ")
    print("=" * 60)
    print(f" SSH Honeypot  : ssh user@{local_ip} -p 2222")
    print(f" HTTP Honeypot : http://{local_ip}:8000")
    print(f" Dashboard     : http://{local_ip}:8050")
    print("=" * 60)
    print("Press CTRL+C to stop the system\n")

    # Keep main thread alive
    while True:
        pass
