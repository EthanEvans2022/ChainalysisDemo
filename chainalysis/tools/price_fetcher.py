#!/usr/bin/env python3
import shrimpy
public_key="4120ad4bc0a5e079bd1bebdca2d43d531074bb8605ed334a5ab81a5f651469d7"
#TO-DO: GET KEY HERE WHILE ENCRYPTED if have time
secret_key="DUMMY123"
client = shrimpy.ShrimpyApiClient(public_key, secret_key)
supported_exchanges = client.get_supported_exchanges()
for exchange in supported_exchanges:
    print(exchange["exchange"])
