"""Main logic of server program."""
import shlex
import asyncio

from common import *


def parse_create_chat(args: list):
    try:
        assert args[0] is str

        result = {
            'name': args[0],
            'limit': None,
            'security_mode': False,
            'password': None,
            'autoright': Rights.EDITOR
        }

        for i in range(1, len(args)):
            match args[i]:
                case '-l' | '--limit':
                    assert type(args[i + 1]) in [int, None]
                    result['limit'] = args[i + 1]
                case '-s' | '--security_mode':
                    assert args[i + 1] is bool
                    result['security_mode'] = args[i + 1]
                case '-p' | '--password':
                    result['security_mode'] = True
                    result['password'] = args[i + 1]
                case '-a' | '--autoright':
                    assert args[i + 1] in ['Administrator', 'Editor', 'Reader', 0, 1, 2]
                    result['autoright'] = Rights(args[i + 1])
                case _:
                    continue
    except Exception:
        return {}

    return result


async def handler(reader, writer):
    """Async logic of handler."""
    client = writer.get_extra_info("peername")
    print(f'New Client on {client}')
    my_user = User(user_id=hash(client), username='_')

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(my_user.queue.get())

    while not reader.at_eof():
        done, pending = await asyncio.wait(
            [send, receive],
            return_when=asyncio.FIRST_COMPLETED)

        for request in done:
            if request is send:
                send = asyncio.create_task(reader.readline())
                print(f'{client}: {request.result()}')
                if (not request.result()):
                    break

                cmd, *args = shlex.split(request.result().decode())
                print("LOG: ", client, request.result().decode())
                print("LOG: ", args)
                answer = ""

                match cmd:
                    case 'entrance':
                        args = shlex.join(args)
                        my_user.username = args
                        answer = f"Welcome to Terminal Messenger, {my_user.username}"

                    case 'show_chatlist':
                        Avaliable = []
                        Hidden = []
                        Avaliable.append('Avaliable chats:')
                        Avaliable.append('_' * 20 + '\n')
                        Hidden.append('Hidden chats:')
                        Hidden.append('_' * 20 + '\n')

                        response = my_user.show_chatlist()
                        Avaliable.append(
                            '\n'.join(
                                [
                                    f" - {chat['name']} {chat['rights'] if chat['rights'] else ''}"
                                    for chat in response[0]
                                ]
                            )
                        )
                        Hidden.append(
                            '\n'.join(
                                [
                                    f" - {chat['name']} {chat['rights'] if chat['rights'] else ''}"
                                    for chat in response[1]
                                ]
                            )
                        )

                        answer = '\n'.join(Avaliable + Hidden)

                    case 'open_chat':
                        name, *password = args
                        chat: Chat = TM_chats[name]

                        if chat.security_mode:
                            access = chat.check_password(password_to_check=password)

                        if not access:
                            answer = "No access to chat"
                        else:
                            my_user.open_chat(name)

                        # TODO: message to chat about your join

                        answer = '{0:_^30}'.format(name.upper())

                    case 'create_chat':
                        chat_statistics = parse_create_chat(args)
                        my_user.create_chat(
                            name=chat_statistics["name"],
                            limit=chat_statistics["limit"],
                            security_mode=chat_statistics["security_mode"],
                            password=chat_statistics["password"],
                            autoright=chat_statistics["autoright"]
                        )

                        # TODO: message to chat about your creation

                        answer = '{0: ^30}'.format('You successfully create new chat')

                    case 'add_to_chat':
                        pass
                    case 'quit_chat':
                        pass
                    case 'delete_chat':
                        pass
                    case _:
                        continue

                print(f"~~~{answer}~~~")
                writer.write(answer.encode())

            if request is receive:
                receive = asyncio.create_task(my_user.queue.get())
                writer.write(f"{request.result()}\n".encode())
                await writer.drain()

    send.cancel()
    receive.cancel()
    del TM_users[my_user._user_id]
    writer.close()
    await writer.wait_closed()
    print(f'{client} left')


async def main(port=1337):
    """Async logic of server."""
    print('Start working')
    server = await asyncio.start_server(handler, '0.0.0.0', port)
    print('activate server')
    async with server:
        print('Server Forever')
        await server.serve_forever()


def start(port=1337):
    """Start the server"""
    asyncio.run(main(port))