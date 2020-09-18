import socket
import tqdm
import os
from threading import Thread


clients = []

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name

    # clean up
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        while True:
            received = self.sock.recv(BUFFER_SIZE).decode()
            if received:
                filename, filesize = received.split(SEPARATOR)
                filename = os.path.basename(filename)
                filesize = int(filesize)
                # changing name if found one with the same
                n = 1
                old_name = filename
                while os.path.isfile(f"{filename}"):
                    ind = old_name.rfind(".")
                    if ind != -1:
                        filename = old_name[:ind] + "_copy" + str(n) \
                                   + old_name[ind:]
                    else:
                        filename = old_name + "_copy" + str(n)
                    n += 1

                with open(filename, "wb") as f:
                    while True:
                        bytes_read = self.sock.recv(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        f.write(bytes_read)
                print(f"{filename} received from {self.name}")
            else:
                # if we got no data – client has disconnected
                self._close()
                # finish the thread
                return


def main():
    next_name = 1

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 8800))
    sock.listen()

    while True:
        con, addr = sock.accept()
        clients.append(con)
        name = 'u' + str(next_name)
        next_name += 1
        print(str(addr) + ' connected as ' + name)
        ClientListener(name, con).start()


if __name__ == "__main__":
    main()
