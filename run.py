import argparse
from scripts import app

PORT_DEFAULT = 5700
PORT_ALT = 5705

parser = argparse.ArgumentParser("Run streaming app")
parser.add_argument("--windows", help="Run with Windows socket interface", action="store_true")
parser.add_argument("--alt", help=f"Run on alternative port {PORT_ALT}", action="store_true")
args = parser.parse_args()

port = PORT_DEFAULT if not args.alt else PORT_ALT
app.with_socket_client = args.windows

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=port, debug=False)