from pytonconnect import TonConnect

import config
from tc_storage import TcStorage

def get_connector(chat_id):
    return TonConnect(config.manifest_url, storage=TcStorage(chat_id))
    
