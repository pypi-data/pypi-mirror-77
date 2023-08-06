# scrapy-umeng

## 安裝方法

使用 pip 安裝

    $ pip install scrapy-umeng

或者使用 pipenv 安装

    $ pipenv install scrapy-umeng

## 配置

1. 配置友盟相關參數

        UMENG_API_KEY = {api_key}
        UMENG_API_SECRET = '{api_secret}'
        UMENG_API_SERVER = 'gateway.open.umeng.com'

3. 在 Scrapy 中的 settings.py 配置中间件：

        DOWNLOADER_MIDDLEWARES = {
            'umeng.UmengDownloaderMiddleware.UmengDownloaderMiddleware': 800,
        }

    或者在 Spider 的 custom_settings 中配置：

        custom_settings = {
            'DOWNLOADER_MIDDLEWARES': {
                'umeng.UmengDownloaderMiddleware.UmengDownloaderMiddleware': 800
            }
        }

4. 在 Spider 中使用 UmengRequest 抓取数据，API：

        from umeng.UmengRequest import UmengRequest
        ...
        ...
        
        class Umeng(scrapy.Spider):
            def start_requests(self):
                yield UmengRequest(api='UmengUappGetActiveUsersRequest', callback=self.parse)
        ...
        ...