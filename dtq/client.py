import asyncio
import sys


async def client(path: str):
    r, w = await asyncio.open_unix_connection(path)
    msg = (" ".join(sys.argv[1:])).encode()
    print(msg)
    for msg in sys.argv[1:]:
        w.write(msg.encode())
        w.write(b"\n")
    w.write_eof()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client("/tmp/dtq"))
    loop.close()

