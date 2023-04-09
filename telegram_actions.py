import asyncio
import time
# import re
import os


async def send_a_message(client, username, message):
    """
    Send a mesaage to a user
    """
    await client.send_message(username, message)


async def get_messages(client, username, total_of_sms=None):
    """
    Get the messages from any user
    """
    # from telethon import utils
    all_sms = []
    i = 0
    async for message in client.iter_messages(username):
        if total_of_sms and i < total_of_sms:
            all_sms.append(message.text)
        elif message.id != await client.get_me().username:
            all_sms.append(message.text)
        else:
            break
        i += 1
    return all_sms


async def start_action(client, any_action=''):
    """
    Perform any action selected by the user
    Return: option of the user
    """
    show_menu = True
    if show_menu:
        act = ('Send message', 'Get last messages', 'Search',
               'Balance of the account', 'Select IA', 'Reload modules')
        list_act = [item + f' ({i+1})' for i, item in enumerate(act)]
        prompt_ask = "--------MENU--------\nPlease, select an " \
            + "action:\nExit (0)\n" + '\n'.join(list_act) + '\n--------------'\
            '----' + '\nType the number of option: '
    with open('bot_loaded.txt', 'r', encoding='utf8') as file:
        username = file.read()
    print(f'The bot {username} is selected')
    if not any_action:
        action = input(f'The selected bot is: {username}\n' + prompt_ask)
    else:
        any_action = action
    # username = 'OpenAiChat_bot'
    while not action.isdigit() or int(action) not in tuple(range(len(list_act)
                                                                 + 1)):
        action = input(prompt_ask)
    if action == '1':
        username = input('Type username: ')
        sms = input('Type sms to send: ')
        await send_a_message(client, username, sms)
    elif action == '0':
        return 'y'
    elif action == '2':
        messages_limit = input('Please, type number of messages to get: ')
        while not messages_limit.isdigit():
            messages_limit = input('Please, type number of messages to get: ')
        all_sms = await get_messages(client, 'gpt3_unlim_chatbot',
                                     int(messages_limit))
        print('\n'.join([f'{item}' for i, item in enumerate(all_sms)]))
    elif action == '3':
        search = await action_search(client, username)
        if search == 'exit':
            show_menu = True
    elif action == '4':
        try:
            if username == 'OpenAiChat_bot':
                print("This Bot doesn't have balance option.\n"
                      "Sending hello...")
                search = '/a Hello'
            elif username == 'GPT4Telegrambot':
                search = '/account'
            elif username == 'gpt3_unlim_chatbot':
                search = 'My balance'
            response = await collect_info(client, username, search)
            print(response[0])
        except (SyntaxError, ValueError, KeyError, IndexError,
                TypeError) as error:
            print(error)
    elif action == '5':
        try:
            print('ChatGPTBot (1):\nChatGPT 3.5 (2)\nEvolveAI (3)'
                  ' (default option)')
            s_c = input("Please select a choice (1/2/3): ")
            while not s_c.isdigit() and int(s_c) not in (1,2,3):
                s_c = input("Please select a choice (1/2/3): ")
            chats = {'1': 'gpt3_unlim_chatbot',
                     '2': 'GPT4Telegrambot',
                     '3': 'OpenAiChat_bot'}
            username = chats.get(s_c)
            print(f'The chatbot {username} has been selected')
            with open('bot_loaded.txt', 'w') as file:
                file.write(username)
        except (SyntaxError, ValueError, KeyError, IndexError, TypeError, 
                AttributeError) as f:
            print(f)
    elif action == '6':
        return 'nr'
    return 'n'


async def action_search(client, username):
    """
    Perform the user search
    Return: option of the search
    """
    search = ''
    # me = await client.get_me()
    while search != 'exit':
        print('-------SEARCH---------')
        search = input('Please, type your question (ex or exit for exit, cl'
                       ' for clear):\n-> ')
        if search in ('ex', 'exit'):
            clear_console()
            break
        if search == 'cl':
            clear_console()
        elif search == '':
            pass
        else:
            if username == 'OpenAiChat_bot':
                search = f'/a {search}'
            await send_a_message(client, username, search)
            response = list()
            async for message in client.iter_messages(username, 1):
                response.append((message.id, message.text))
            while search == response[0][1]:
                time.sleep(5)
                response = list()
                async for message in client.iter_messages(username, 1):
                    response.append((message.id, message.text))
            print('\n\n------------RESPONSE--------------')
            print(''.join(response[0][1]).split('[Join EvolveAI]',
                                                maxsplit=1)[0])
    return search

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

async def run_concurrent_tasks(all_data: tuple):
    all_tasks = await asyncio.gather(all_data)
    return all_tasks


async def collect_info(client, username: str, search:str):
    await send_a_message(client, username, search)
    response = await get_messages(client, username, 1)
    while search in response[0] or 'Please wait' in response:
        time.sleep(5)
        response = await get_messages(client, username, 1)
    return response
