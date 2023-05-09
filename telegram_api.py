import asyncio
from telethon import TelegramClient
import asyncio
import tracemalloc
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
tracemalloc.start()

api_id = 'your_telegram_id'
api_hash = 'your_api_telegram_hash'
MTProto_server_test = '149.154.167.40:443'
PTProto_server_prod = '149.154.167.50:443'
client = TelegramClient(None, api_id, api_hash)

