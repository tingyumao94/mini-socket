import socket
import selectors
from .lib import ServerMessage
import traceback
import time, os
from .utils import append_to_txt

class Server(object):
    """ Multi-connection 
    Run server in Machine A.
    Run clinet in Machine B. 
    And mini-socket is able to build connect between A and B.

    In basic Client and Sever:
        B -> send data -> A -> save data in some files -> send reponse to B -> close.
        B -> requry data -> A -> parse query and send data back -> B recv data and send response to A -> close.
    
    """
    def __init__(self, host, port, save=True):
        super().__init__()
        self.host = host
        self.port = port
        self.save = save
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sel  = selectors.DefaultSelector()

        self.sock.bind((host, port))
        self.sock.listen()
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)
        if save:
            self._prefix = os.path.join("./_recv", time.strftime('%Y%m%d%H%M')+f"_P{port}")

    def accept_wrapper(self, accpet_sock):
        conn, addr = accpet_sock.accept()  
        print("accepted connection from", addr)
        conn.setblocking(False) 
        print(addr[0] )
        message = ServerMessage(self.sel, conn, addr)
        self.sel.register(conn, selectors.EVENT_READ, data=message)
    
    def run(self):
        try:
            while True:
                # waiting connection
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        message = key.data
                        try:
                            message.process_events(mask)
                            if self.save and mask==1:
                                # avoid repeat save
                                self.save_events(message)
                        except Exception:
                            print(
                                "main: error: exception for",
                                f"{message.addr}:\n{traceback.format_exc()}",
                            )
                            message.close()

        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting server")
        finally:
            self.sel.close()

    def save_events(self, message):
        try:
            content = message.request
            request_type = message.jsonheader.get("content-type")
            if "json" in request_type:
                raise NotImplementedError("Json is not support to save")
            print(type(content), request_type)
            str_content = content.decode("utf-8")
            val_content = str_content.split(">>")[-1][1:]
            self._filename = (self._prefix + "IP" + str(message.accept_ip) + ".txt")
            append_to_txt(self._filename, val_content)
            print(f"message append to {self._filename}")
        except NotImplementedError:
            print("Save failed, Only save recv data from client")
        finally:
            print("Exit saving message")
    
    @property
    def prefix(self):
        return self._prefix

    @property
    def latest_save_file(self):
        return self._filename


class MidServer(Server):
    """In some machine dont have access to run server backgroud, 
        most because the port is not allow to exposed.
       So we build MidServer: 

       Run Client in Machine A,
       Run Client in Machine B,
       Run MidServer in Machine C.

       Using Machine C to connet Machin A and Machine B.
    """

    pass