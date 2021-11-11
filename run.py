import argparse
from scripts import app

parser = argparse.ArgumentParser("Run streaming app")
parser.add_argument("--windows", help="Run with Windows socket interface", action="store_true")
args = parser.parse_args()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5700, debug=False, with_socket_client= args.windows)