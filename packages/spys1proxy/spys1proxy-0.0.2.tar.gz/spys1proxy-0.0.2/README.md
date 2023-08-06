# How to use spys one proxy list


```   
    loop = asyncio.get_event_loop()
    spys = Spys()
    spys.countries.append('DE')
    loop.run_until_complete(spys.search())
    print(spys, spys.proxy_list)
```
        