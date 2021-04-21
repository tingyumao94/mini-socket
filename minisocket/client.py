# copy to clinet end
import sys
import socket
import selectors
import traceback
from .lib import ClientMessage

class Client(object):
    def __init__(self, host, port, action, value):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sel = selectors.DefaultSelector()
        self.host = host
        self.port = port
        self.action = action
        self.value = value

    def create_request(self, action, value):
        if action == "search":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(action=action, value=value),
            )
        else:
            content = "{} >> {}".format(action, value)
            return dict(
                type="binary/custom-client-binary-type",
                encoding="binary",
                content=bytes(content, encoding="utf-8"),
            )
    
    def start_connection(self, host, port, action, value):
        request = self.create_request(action, value)
        self.sock.setblocking(False)
        addr = (host, port)
        self.sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE 
        message = ClientMessage(self.sel, self.sock, addr, request)
        self.sel.register(self.sock, events, data=message)

    def run(self):
        self.start_connection(self.host, self.port, self.action, self.value)
        try:
            while True:
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask)
                        self._recv_info = message.request_result
                    except Exception:
                        print(
                            "main: error: exception for",
                            "{}:\n{}".format(message.addr, traceback.format_exc() ),
                        )
                        message.close()
                # check socket being monitored to continue
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting client")
        finally:
            self.sel.close()
    

    @property
    def recv_info(self):
        return self._recv_info