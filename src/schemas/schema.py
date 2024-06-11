import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from lxml import html
from tortoise import Tortoise
from tortoise.transactions import atomic, in_transaction
from models.model import Currency, CurrencyIn

ua = UserAgent()

url = 'https://halykbank.kz/exchange-rates'

async def fetch_currency_data():
    url = 'https://back.halykbank.kz/common/currency-history'
    headers = {'User-Agent': ua.random}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

async def save_to_database(data):
    async with in_transaction():
        for item in data:
            existing_currency = await Currency.filter(currency_pair=item['currency_pair']).first()
            if existing_currency:
                existing_currency.buy = item['buy']
                existing_currency.sell = item['sell']
                await existing_currency.save()
                print(f"Updated data: {item}")
            else:
                await Currency.create(**item)
                print(f"Saved new data: {item}")


async def data():
    currency_data = await fetch_currency_data()
    
    if currency_data and currency_data['result']:
        currency_history = currency_data['data']['currencyHistory']
        
        if currency_history:
            latest_data = currency_history[0]  

            date = latest_data['date']
            date_title = latest_data['dateTitle']
            private_persons = latest_data['privatePersons']

            data = []
            for currency_pair, rates in private_persons.items():
                data.append({
                    "currency_pair": currency_pair,
                    "buy": rates['buy'],
                    "sell": rates['sell']
                })

            return data
        else:
            print("Currency history is empty.")
            return []
    else:
        print("Error fetching currency data or result is False.")
        return []

async def get_currency_pair(currency_pair: str):
    currency_data = await Currency.filter(currency_pair=currency_pair).first()
    if currency_data:
        return {"sell": currency_data.sell, "buy": currency_data.buy}
    else:
        return {"error": "Currency pair not found"}

async def fetch_url(url: str, headers: dict) -> str:
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        response = await loop.run_in_executor(pool, requests.get, url, headers)
    return response.content
    
async def check_url():
    global url
    headers = {'User-Agent': ua.random}
    response_content = await fetch_url(url, headers)
    return response_content.decode('utf-8')