import asyncio
import sys

from message import Message, dump


async def client(path: str):
    r, w = await asyncio.open_unix_connection(path)
    msg = (" ".join(sys.argv[1:])).encode()
    print(msg)
    m = Message(msg)
    await dump(w, m)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client("/tmp/dtq"))
    loop.close()

