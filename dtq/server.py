import asyncio
from subprocess import PIPE

from message import load


async def do_command(line="", env=None):
    "Execute shell command"
    if env is None:
        env = dict()
    p = await asyncio.create_subprocess_shell(line, stdout=PIPE, stderr=PIPE,
                                              env=env)
    await p.wait()
    while True:
        line = await p.stdout.readline()
        if len(line) == 0:
            break
        print(line)


class Server:

    def __init__(self, path: str, actions: dict = None):
        self.path = path
        self.actions = dict()
        if actions is not None:
            for name, action in actions.items():
                self.register(name, action)

    def register(self, name, action):
        assert asyncio.iscoroutinefunction(action)
        self.actions[name] = action

    def action(self, name):
        def decorate(func):
            self.register(name, func)
            return func
        return decorate

    async def on_client(self, client_reader: asyncio.StreamReader,
                        client_writer: asyncio.StreamWriter):
        print("Paf, a client")
        m = await load(client_reader)
        await self.queue.put(m)
        client_writer.close()

    async def action_loop(self):
        while True:
            envelope = await self.queue.get()
            # Routing the envelope to a registered action
            if envelope.action not in self.actions:
                print("Action unknown: ", envelope.action)
                continue
            await self.actions[envelope.action](**envelope.args)

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
    s.register("command", do_command)

    @s.action("hello")
    async def hello(name: str = ""):
        print("Hello ", name)

    loop.run_until_complete(s.serve())
    loop.run_forever()
    loop.close()
