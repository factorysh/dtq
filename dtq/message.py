import asyncio
import pickle
import struct


class Message:
    def __init__(self, msg="", queue="default"):
        self.queue = queue
        self.msg = msg


async def dump(writer: asyncio.StreamWriter, msg: Message):
    blob = pickle.dumps(msg)
    writer.write(struct.pack("i", len(blob)))
    writer.write(blob)


async def load(reader: asyncio.StreamReader) -> Message:
    l = struct.unpack("i", await reader.readexactly(4))[0]
    return pickle.loads(await reader.readexactly(l))
