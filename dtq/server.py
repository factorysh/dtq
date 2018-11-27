import asyncio
import struct
import pickle
from subprocess import PIPE

from message import Message


class Server:

    def __init__(self, path: str):
        self.path = path

    async def on_client(self, client_reader: asyncio.StreamReader,
                        client_writer: asyncio.StreamWriter):
        print("Paf, a client")
        l = struct.unpack("i", await client_reader.readexactly(4))[0]
        m = pickle.loads(await client_reader.readexactly(l))
        await self.queue.put(m)
        client_writer.close()

    async def action_loop(self):
        while True:
            m = await self.queue.get()
            p = await asyncio.create_subprocess_shell(m.msg, stdout=PIPE,
                                                      stderr=PIPE)
            await p.wait()
            while True:
                line = await p.stdout.readline()
                if len(line) == 0:
                    break
                print(line)

    async def serve(self):
        print("Path: ", self.path)
        self.queue = asyncio.Queue(maxsize=100)
        asyncio.gather(
            asyncio.start_unix_server(self.on_client, path=self.path),
            self.action_loop()
        )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    s = Server("/tmp/dtq")
    loop.run_until_complete(s.serve())
    loop.run_forever()
    loop.close()
