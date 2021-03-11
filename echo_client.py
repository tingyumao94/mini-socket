from src.client import Client
import sys
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("usage:", sys.argv[0], "<host> <port> <action> <value>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    action, value = sys.argv[3], sys.argv[4]
    value = dict(a=1)
    client = Client(host, port, action, value)
    client.run()

