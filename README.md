# async request via aiohttp
Use asynchronous request via aiohttp library in python.


## Requirements

asyncio

aiohttp

## Usage

```python
from async_request import Request


rq = Request()


if __name__ == '__main__':
    response = rq.request(method='GET', url='https://httpbin.org/get')
    print(response)
```
