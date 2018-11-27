import asyncio


async def on_client(client_reader: asyncio.StreamReader,
                    client_writer: asyncio.StreamWriter):
    print("Paf, a client")
    while True:
        line = await client_reader.readline()
        print(line)
        if client_reader.at_eof():
            client_writer.close()
            return


async def serve(path: str):
    print("Path: ", path)
    await asyncio.start_unix_server(on_client, path=path)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(serve("/tmp/dtq"))
    loop.run_forever()
    loop.close()
