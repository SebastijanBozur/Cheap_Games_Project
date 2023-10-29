import requests
import json
import sys
import datetime as dt
from os.path import join, getmtime, exists


games_data = []

def game_deals(store, page):
    url = f"https://www.cheapshark.com/api/1.0/deals?storeID={store}&upperPrice=15&pageNumber={page}"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

def save_response(store_id, page_number):
    data_cached = True
    file_path = join('cache', 'storeid_' + str(store_id) + '_page_' + str(page_number))
    if not exists(file_path):
        data_cached = False
    elif dt.datetime.fromtimestamp(getmtime(file_path)) < dt.datetime.now() - dt.timedelta(hours=24):
        data_cached = False
    if data_cached:
        print('cached')
        with open(file_path, 'w') as f:
            f.write(game_deals(getstore(store_id), getpage(page_number)))


def getstore(store_id):
    if store_id == 'steam' or 'Steam':
        store_id = 1
        return store_id
    if store_id == 'GamersGate' or 'gamersgate':
        store_id = 2
        return store_id
    if store_id == 'GreenManGaming' or 'greenmangaming':
        store_id = 3
        return store_id
    if store_id == 'gog' or 'goodoldgames':
        store_id = 7
        return store_id
    if store_id == 'Humble Store' or 'humble store':
        store_id = 11
        return store_id
    if store_id == 'Fanatical' or 'fanatical':
        store_id = 15
        return store_id
    if store_id == 'WinGameStore' or 'wingamestore':
        store_id = 21
        return store_id
    if store_id == 'GameBillet' or 'gamebillet':
        store_id = 23
        return store_id
    if store_id == 'Epic Games Store' or 'epic':
        store_id = 25
        return store_id
    if store_id == 'Gamesplanet' or 'gamesplanet':
        store_id = 27
        return store_id
    else:
        print('Invalid store name or store not available')

def getpage(page_number):
    if 0 <= page_number >= 100:
        print('Invalid page range or value: ')
    elif not page_number:
        print('Please enter a number value')
    else:
        return page_number


store_id = input('Enter store: ').lower().strip()
page_number = int(input("Enter deals page number: "))
print(game_deals(getstore(store_id), getpage(page_number)))