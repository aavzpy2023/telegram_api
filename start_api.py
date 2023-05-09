"""
Module to start api
"""
import importlib
import sys
from my_telegram_api import client

ex = 'n'


async def main():
    """
    Beging the process to start the api
    Return: the answer from the api execution
    """
    # me = await client.get_me()
    try:
        ex_response = await start_action(client)
        return ex_response
    except (SyntaxError, ValueError, KeyError, IndexError, AttributeError,
            TypeError, KeyboardInterrupt) as f:
        print(f)
    return 'n'

if __name__ == "__main__":
    ex = 'n'
    while ex != 'y':
        from telegram_actions import start_action
        with client:
            ex = client.loop.run_until_complete(main())
        # ex = input('Do you want to exit y/n/no and reload modules(nr)?')
        if ex == 'nr':
            print("Reloading modules ...")
            importlib.reload(sys.modules['telegram_actions'])
