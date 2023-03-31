# Dollar_scraping_bot
This project consists of scraping a web page to extract the current dollar price and send it to a Telegram group via a bot. The goal is to automate the process of checking the dollar price and sharing it with a group of interested users.

# Requirements
```
anyio==3.6.2
autopep8==2.0.2
certifi==2022.12.7
charset-normalizer==3.1.0
h11==0.14.0
httpcore==0.16.3
httpx==0.23.3
idna==3.4
lxml==4.9.2
pycodestyle==2.10.0
python-dotenv==1.0.0
python-telegram-bot==20.2
requests==2.28.2
rfc3986==1.5.0
schedule==1.1.0
sniffio==1.3.0
tomli==2.0.1
urllib3==1.26.15
```

## Installation
### Create and activate an virtual env -> Ubuntu
```
python3 venv -m venv env
source env/bin/activate
```
### Clone and installation

```
git clone
cd dollar_scraping_bot
pip3 install -r requirements.txt
python3 scrapper.py
```

## Usage


### Create a .env file an add:

```
TELEGRAM_BOT_TOKEN= Your token telegram bot
TELEGRAM_CHAT_ID= Your chat or group ID

HOME_URL = 'https://www.cronista.com/MercadosOnline/dolar.html'
XPATH_LINKS = '//td[@class="name"]/a/@href'
XPATH_DOLLAR_TYPE = '//td[@class="name"]/a/text()'
XPATH_PRICE_SELL = '//td[@class="sell"]/a/div/div[@class="sell-value"]/text()'
XPATH_PRICE_BUY = '//td[@class="buy"]/a/div/div[@class="buy-value"]/text()'
XPATH_VARIATION = '//td[contains(@class,"percentage")]/a/span/text()'
XPATH_DATE = '//td[contains(@class,"date")]/a/text()'
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
