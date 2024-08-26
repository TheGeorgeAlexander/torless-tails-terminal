"""
This file implements a minimal SOCKS5 proxy that runs on port 9050.
Normally the Tor service runs on that port. Applications in Tails are
configured to use that port for the Tor proxy. To ensure these
applications still work without Tor, this proxy pretends to be Tor
but just sends out requests over the clearnet.
Tor has some SOCKS protocol extensions, so this custom script is
necessary instead of using a standard SOCKS5 proxy. Below is a URL
for more info on Tor SOCKS protocol extensions.
https://spec.torproject.org/socks-extensions.html
"""
import asyncio
import socket
import struct


class SOCKS5ProxyServer:
    def __init__(self, host='127.0.0.1', port=9050):
        self.host = host
        self.port = port


    async def handle_client(self, reader, writer):
        # Step 1: SOCKS5 handshake
        await self.socks5_handshake(reader, writer)

        # Step 2: Handle the SOCKS5 request (connect to the real destination)
        target_reader, target_writer = await self.socks5_connect(reader, writer)

        if target_writer is None:
            writer.close()
            await writer.wait_closed()
            return

        # Step 3: Forward data between the client and the destination
        try:
            await asyncio.gather(
                self.forward_data(reader, target_writer),
                self.forward_data(target_reader, writer)
            )
        except ConnectionResetError as e:
            pass
        except Exception as e:
            print(f"Network error: {e}")


    async def socks5_handshake(self, reader, writer):
        # Read and parse the handshake request
        data = await reader.read(2)
        version, nmethods = struct.unpack("!BB", data)
        methods = await reader.read(nmethods)
        
        # Check if the client supports no authentication (0x00)
        if 0x00 in methods:
            writer.write(b"\x05\x00")
            await writer.drain()
            
        # Otherwise, check if the client supports username/password authentication (0x02)
        elif 0x02 in methods:
            writer.write(b"\x05\x02")
            await writer.drain()

            # Handle the username/password authentication
            await self.socks5_auth(reader, writer)
            
        # Client doesn't support either 0x00 or 0x02
        else:
            writer.write(b"\x05\xFF") # No acceptable methods
            await writer.drain()


    async def socks5_auth(self, reader, writer):
        # Read and parse the authentication request
        version = await reader.read(1)
        username_len = await reader.read(1)
        username = await reader.read(username_len[0])
        password_len = await reader.read(1)
        password = await reader.read(password_len[0])

        # Ignore the actual username and password, always succeed
        writer.write(b"\x01\x00")  # Success response
        await writer.drain()


    async def socks5_connect(self, reader, writer):
        # Read and parse the SOCKS5 request
        data = await reader.read(4)
        version, cmd, _, address_type = struct.unpack("!BBBB", data)

        if cmd not in [0x01, 0xF0]:  # Support CONNECT and custom Tor command RESOLVE
            writer.write(b"\x05\x07\x00\x01" + socket.inet_aton('0.0.0.0') + struct.pack("!H", 0))
            await writer.drain()
            return None, None

        # Handle different address types
        if address_type == 0x01:  # IPv4
            address = socket.inet_ntoa(await reader.read(4))
        elif address_type == 0x03:  # Domain name
            length = await reader.read(1)
            address = (await reader.read(length[0])).decode()
        elif address_type == 0x04:  # IPv6
            address = socket.inet_ntop(socket.AF_INET6, await reader.read(16))
        else:
            writer.write(b"\x05\x08\x00\x01" + socket.inet_aton('0.0.0.0') + struct.pack("!H", 0))
            await writer.drain()
            return None, None

        # Read the port (only used for CONNECT command, not needed for RESOLVE)
        port = struct.unpack("!H", await reader.read(2))[0]

        # Handle the Tor-specific RESOLVE command
        if cmd == 0xF0:
            try:
                # Perform DNS lookup and send success response with resolved IP
                ip = await asyncio.get_running_loop().getaddrinfo(address, None, family=socket.AF_INET, type=socket.SOCK_STREAM)
                writer.write(b"\x05\x00\x00\x01" + socket.inet_aton(ip[0][4][0]) + struct.pack("!H", 0))
            except Exception:
                # Send failure response (Host unreachable)
                writer.write(b"\x05\x04\x00\x01" + socket.inet_aton('0.0.0.0') + struct.pack("!H", 0))
    
            await writer.drain()
            return None, None

        # Proceed with the CONNECT command
        try:
            target_reader, target_writer = await asyncio.open_connection(address, port)
        except Exception as e:
            writer.write(b"\x05\x01\x00\x01" + socket.inet_aton('0.0.0.0') + struct.pack("!H", 0))
            await writer.drain()
            return None, None

        # Send success response for CONNECT command
        writer.write(b"\x05\x00\x00\x01" + socket.inet_aton('0.0.0.0') + struct.pack("!H", 0))
        await writer.drain()

        return target_reader, target_writer


    async def forward_data(self, reader, writer):
        try:
            while not reader.at_eof():
                data = await reader.read(4096)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()


    def start(self):
        loop = asyncio.get_event_loop()
        server = asyncio.start_server(self.handle_client, self.host, self.port)
        loop.run_until_complete(server)
        loop.run_forever()


if __name__ == '__main__':
    proxy = SOCKS5ProxyServer()
    proxy.start()
