import asyncio
import sys
import os

from message import Envelope, dump


async def client(path: str):
    r, w = await asyncio.open_unix_connection(path)
    msg = (" ".join(sys.argv[1:])).encode()
    print(msg)
    env = dict()

    #await dump(w, Envelope(action="hello", args=dict(name="Bob")))
    m = Envelope(action="command", args=dict(line=msg,
                                             env=dict(os.environ.items())))
    await dump(w, m)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client("/tmp/dtq"))
    loop.close()

