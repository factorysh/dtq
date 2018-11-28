import asyncio
import pickle
import struct


class Envelope:
    def __init__(self, action="ping", args=None):
        self.action = action
        self.args = args


class Command:
    def __init__(self, line="", queue="default", env=None):
        self.queue = queue
        self.line = line
        if env is None:
            env = dict()
        self.env = env


async def dump(writer: asyncio.StreamWriter, msg: Envelope):
    blob = pickle.dumps(msg)
    writer.write(struct.pack("i", len(blob)))
    writer.write(blob)


async def load(reader: asyncio.StreamReader) -> Envelope:
    l = struct.unpack("i", await reader.readexactly(4))[0]
    return pickle.loads(await reader.readexactly(l))
