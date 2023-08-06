
**Apigram** – Python Telegram Bot API wrapper

* [Examples](./examples) (python3)
* [Telegram Bot API Manual](https://core.telegram.org/bots/api)

```python
import apigram

bot = apigram.session('123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11')
api = apigram.get_api(bot)

print(api.getMe())
```

Install
------------
    $ pip install apigram
