#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import asyncio
import websockets
import csv
import os
import requests

from config import SEED, SIZE

def download_map_image():
    
    headers = {'Content-type': 'application/json'}
    url = 'https://rustmaps.com/api/v2/maps/{}/{}?staging=false&barren=false'.format(SEED, SIZE)
    r = requests.get(url, headers=headers)
    map_data = r.json()
    print(map_data)
    image_url = map_data['imageUrl']
    r = requests.get(image_url, headers=headers)
    with open('map.png', 'wb') as SRC:
        SRC.write(r.content)
        return True

async def ws_conn(msg, auth, identifier=1001):
    '''
    Для подключения по протоколу websocket.
    Принимает команду "msg" для сервера и данные для авторизации "auth".
    После чего возвращает ответ сервера, если всё прошло хорошо.
    '''
    MSG = {
            'Identifier': identifier,
            'Message': msg,
            'Name': 'WebRcon'
        }
    while True:
        async with websockets.connect(
                'ws://{ip}:{port}/{pswd}'.format(**auth), max_size=2 ** 30, read_limit=2 ** 30, write_limit=2 ** 30, close_timeout=0) as websocket:
            
            
            await websocket.send( json.dumps(MSG) )
            # try:
                # greeting = await asyncio.wait_for(websocket.recv(), timeout=2)
                # # print(greeting)
            # except asyncio.TimeoutError:
                # return '<' 
            result = await asyncio.wait_for(websocket.recv(), timeout=2)
            greeting = json.loads(result)
            message_identifier = greeting["Identifier"]
            if message_identifier == identifier:
                # иногда прилетает нулевой ID
                break
            print([result])
            
            # print(greeting["Message"])
    return greeting["Message"]

def dialog(command, auth_, identifier=1001):
    '''
    Промежуточная функция для передачи команды и данных аутентификации 
    к ws_conn.
    '''
    loop = asyncio.get_event_loop()
    answer = loop.run_until_complete(ws_conn(command, auth_, identifier))
    # print('Ansver', answer)
    return answer

def open_log(namefile):
    if os.path.exists(namefile):
        with open(namefile, 'rt', encoding='utf-8') as SRC:
            RDR = csv.reader( SRC )
            for result in RDR:
                yield result
    else:
        yield
