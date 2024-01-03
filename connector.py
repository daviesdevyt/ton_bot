from pytonconnect import TonConnect

import config
from tc_storage import TcStorage
import asyncio

class Connector(TonConnect):
    def __init__(self, chat_id: int):
        super().__init__(config.manifest_url, storage=TcStorage(chat_id))

    def connect(self, wallet: str):
        return asyncio.run(super().connect(wallet))

    def restore_connection(self):
        return asyncio.run(super().restore_connection())

