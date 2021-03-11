from src.server import MidServer as Server
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage:", sys.argv[0], "<host> <port>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    server = Server(host, port)
    print(f"file will saving to  {server.prefix}_*")
    server.run()
