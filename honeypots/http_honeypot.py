print("HTTP HONEYPOT FILE LOADED")

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os
import random
from analytics.parser import log_attack

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "web", "templates")

USERS = {
    "admin": {"password": "malcoredomain", "role": "admin"},
    "Arbaz": {"password": "bihariboy", "role": "employee"},
    "Ahmed": {"password": "zameenchaat", "role": "employee"},
    "Altamash": {"password": "khanbaba", "role": "employee"}
}

NOTICES = []


def render_template(name, replacements=None):
    path = os.path.join(TEMPLATE_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("{{ERROR}}", "")

    if replacements:
        for key, value in replacements.items():
            content = content.replace(key, value)

    return content


def generate_fake_logs():
    employees = ["Arbaz", "Ahmed", "Altamash"]
    actions = [
        "Logged into SOC console",
        "Analyzed suspicious binary",
        "Reviewed malware sample",
        "Investigated phishing alert",
        "Updated firewall rules",
        "Performed PCAP traffic analysis"
    ]
    return "".join(
        f"<li class='list-group-item bg-dark text-white'>{random.choice(employees)}  {random.choice(actions)}</li>"
        for _ in range(10)
    )


class HoneypotHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith("/static/"):
            self.serve_static()
            return

        html = render_template("index.html", {"{{ERROR}}": ""})
        self.respond(html)

    def do_POST(self):

        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)
        parsed = urllib.parse.parse_qs(data.decode())

        username = parsed.get("username", [""])[0]
        password = parsed.get("password", [""])[0]

        admin_notice = parsed.get("admin_notice", [""])[0]
        message = parsed.get("message", [""])[0]

        # ---------------- ADMIN NOTICE ----------------
        if admin_notice == "true" and message:
            NOTICES.append(message)

            html = render_template("admin_dashboard.html", {
                "{{LOGS}}": generate_fake_logs(),
                "{{NOTICES}}": "".join(
                    f"<li class='list-group-item bg-dark text-white'>{n}</li>"
                    for n in NOTICES
                )
            })
            self.respond(html)
            return

        # ---------------- AUTHENTICATION ----------------
        if username in USERS and USERS[username]["password"] == password:

            role = USERS[username]["role"]

            if role == "admin":
                html = render_template("admin_dashboard.html", {
                    "{{LOGS}}": generate_fake_logs(),
                    "{{NOTICES}}": "".join(
                        f"<li class='list-group-item bg-dark text-white'>{n}</li>"
                        for n in NOTICES
                    )
                })
                self.respond(html)
                return

            else:
                html = render_template("employee_dashboard.html", {
                    "{{USERNAME}}": username,
                    "{{NOTICES}}": "".join(
                        f"<li class='list-group-item bg-dark text-white'>{n}</li>"
                        for n in NOTICES
                    )
                })
                self.respond(html)
                return

        # ---------------- FAILED LOGIN ONLY ----------------
        if username:
            log_attack(self.client_address[0], username, password, "HTTP")

        html = render_template("index.html", {
            "{{ERROR}}": "<div class='alert alert-danger text-center'>Incorrect ID or Password</div>"
        })
        self.respond(html)

    def serve_static(self):
        static_path = self.path.replace("/static/", "")
        file_path = os.path.join(BASE_DIR, "web", "static", static_path)

        if os.path.exists(file_path):
            self.send_response(200)
            if file_path.endswith(".css"):
                self.send_header("Content-type", "text/css")
            elif file_path.endswith(".js"):
                self.send_header("Content-type", "application/javascript")
            elif file_path.endswith(".mp4"):
                self.send_header("Content-type", "video/mp4")
            self.end_headers()
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def respond(self, html):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())


def start_http():
    server = HTTPServer(("0.0.0.0", 8000), HoneypotHandler)
    print("0xMalCore Portal running on port 8000")
    server.serve_forever()