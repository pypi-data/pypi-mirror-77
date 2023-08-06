# python-moneyspace

A simple python class to assist connecting to the moneyspace.net payment gateway.

Note: this is only tested with QR code payments, however other types should work.

Example:

```
from pythonmoneyspace.moneyspace import MoneySpace

ms = MoneySpace('<MY_SECRET_ID>', '<MY_SECRET_KEY')

# dict
ms.create_transaction(
    'qrnone',  # payment_type
    'someone@example.net',  # customer's email
    150, # amount
    'MY_REF_1',  # order_id
    'https://example.com/my-success-url',
    'https://example.com/my-fail-url',
    'https://example.com/my-cancel-url',
    1 # agreement
)

# dict
ms.check_order_id('MY_REF_1')

# dict
ms.check_payment('MSTRFxxxxxxxxxxxxxx')

# string
ms.get_qr_image_url('MSTRFxxxxxxxxxxxxxx')

# boolean
ms.webhook_is_valid(
    '150.00',
    'OK',
    'MY_REF_1',
    'MSTRFxxxxxxxxxxxxxx',
    '4bfff360bf1bd83f44848a59ee3e2cd1fe77f067501e2ad4de4fd4135068160d'
)
```
