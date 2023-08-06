python-moneyspace
=================

A simple python class to assist connecting to the moneyspace.net payment gateway.

Note: this is only tested with QR code payments, however other types should work.

Example:

```
from moneyspace import MoneySpace

ms = MoneySpace('<MY_SECRET_ID>', '<MY_SECRET_KEY')

ms.create_transaction(
    'qrnone',  # payment_type
    'someone@example.net',  # customer's email
    150, # amount
    'MY_REF_1',  # order_id
    'https://api.yaksri.com/success',
    'https://api.yaksri.com/fail',
    'https://api.yaksri.com/cancel',
    1 # agreement
)

ms.check_order_id('MY_REF_1')

ms.check_payment('MSTRFxxxxxxxxxxxxxx')

ms.webhook_validator(
    '150.00',
    'OK',
    'MY_REF_1',
    'MSTRFxxxxxxxxxxxxxx',
    '4bfff360bf1bd83f44848a59ee3e2cd1fe77f067501e2ad4de4fd4135068160d'
)
```