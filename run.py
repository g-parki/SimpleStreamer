import argparse
import os
from scripts import app

PORT_DEFAULT = 5700
PORT_ALT = 5705

parser = argparse.ArgumentParser("Run streaming app")
parser.add_argument("--socket", help="Run with socket interface", action="store_true")
parser.add_argument("--alt", help=f"Run on alternative port {PORT_ALT}", action="store_true")
args = parser.parse_args()

if args.alt or os.environ.get("ALT") == "True":
    port = PORT_ALT
else: 
    port = PORT_DEFAULT

if args.socket or os.environ.get('SOCKET') == "True":
    app.with_socket_client = True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)