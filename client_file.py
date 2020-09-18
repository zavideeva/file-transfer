import socket
import os
import tqdm
import sys

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096


def main():
    host = str(sys.argv[2])
    port = int(sys.argv[3])
    filename = str(sys.argv[1])
    filesize = os.path.getsize(filename)

    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    progress = tqdm.tqdm(
        range(filesize),
        f"Sending {filename}",
        unit="B",
        unit_scale=True,
        unit_divisor=1024
    )
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))

    s.close()


if __name__ == "__main__":
    main()
