import socket
import selectors
from .lib import SMessage, MidSMessage
import traceback
import time, os
from .utils import append_to_txt, save_json, load_json
import random
## add for demo 
def fake_time(net):
    return random.randint(1,100)

class Server(object):
    """ Multi-connection 
    Run server in Machine A.
    Run clinet in Machine B. 
    And mini-socket is able to build connect between A and B.

    In basic Client and Sever:
        B -> send data -> A -> save data in some files -> send reponse to B -> close.
        B -> requry data -> A -> parse query and send data back -> B recv data and send response to A -> close.
    
    demo mode: show the case in tutorial
    """
    def __init__(self, host, port, save=True, demo=False):
        super().__init__()
        self.host = host
        self.port = port
        self.save = save
        self._demo = demo
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sel  = selectors.DefaultSelector()

        self.sock.bind((host, port))
        self.sock.listen()
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)
        if save:
            self._prefix = os.path.join("./_recv", time.strftime('%Y%m%d%H%M')+"_P{}".format(port) )

    def accept_wrapper(self, accpet_sock):
        conn, addr = accpet_sock.accept()  
        print("accepted connection from", addr)
        conn.setblocking(False) 
        print(addr[0] )
        message = SMessage(self.sel, conn, addr)
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
                                self.save_events(message)
                        except Exception:
                            print(
                                "main: error: exception for",
                                "{}:\n{}".format(message.addr, traceback.format_exc()),
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
            # only return string  type data
            append_to_txt(self._filename, val_content) # 
            print("message append to {}".format(self._filename) ) 
            if self._demo:
                # cal latency
                latency = fake_time(val_content)
                all_request = load_json(message.request_file)
                all_request.update({val_content: latency})
                print(" \n recv new net latency, updating request file")
                save_json(message.request_file, all_request)
                
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
    def accept_wrapper(self, accpet_sock):
        conn, addr = accpet_sock.accept()  
        print("accepted connection from", addr)
        conn.setblocking(False) 
        print(addr[0] )
        message = MidSMessage(self.sel, conn, addr)
        self.sel.register(conn, selectors.EVENT_READ, data=message)
    
    def save_events(self, message):
        # alway flush request file
        try:
            content = message.request
            request_type = message.jsonheader.get("content-type")
            if "json" in request_type:
                raise NotImplementedError("Json is not support to save")
            str_content = content.decode("utf-8")
            split_content = str_content.split(">>")
            val_content = split_content[-1][1:]
            type_content = split_content[0][:-1]
            # according type_content to save val_content
            if type_content.lower() == "net":
                # to json, re-write the request file
                print(" \n >> Note: recv new nets, reflush  request file")
                val_content_dict = {"net": val_content}  # make sure query latest net
                save_json(message.request_file, val_content_dict)
            elif type_content.lower() == "lat":
                print(" \n >> recv latency")
                ori_request = load_json(message.request_file)
                str_net = ori_request["net"]
                val_content_dict = {str_net: val_content}
                print(" \n >> Note: recv net latency, reflushing request file")
                save_json(message.request_file, val_content_dict)
        except NotImplementedError:
            print("Save failed, Only save recv data from client")
        finally:
            print("Exit saving message")


    
    


    