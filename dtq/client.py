import asyncio
import sys
import pickle
import struct

from message import Message


async def client(path: str):
    r, w = await asyncio.open_unix_connection(path)
    msg = (" ".join(sys.argv[1:])).encode()
    print(msg)
    m = Message(msg)
    blob = pickle.dumps(m)
    w.write(struct.pack("i", len(blob)))
    w.write(blob)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client("/tmp/dtq"))
    loop.close()

