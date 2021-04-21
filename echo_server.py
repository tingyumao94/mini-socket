# from minisocket.server import MidServer as Server
from minisocket.server import Server as Server
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage:", sys.argv[0], "<host> <port>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    server = Server(host, port, demo=True)
    print("file will saving to  {}_*".format(server.prefix) )
    server.run()
