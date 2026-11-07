---
max_turns: 4
allowed_tools: [Read, Glob, Grep, Skill]
---

Prune the tests with the PruneTests skill: audit this file for tests that can never fail. Do not open a pull request, just give me the audit.

`pricing.py`:

```python
from pricing_client import client


class Price:
    def __init__(self, amount):
        self.amount = amount


def fetch_rate(currency):
    return client.get_rate(currency)


def apply_discount(price, percent):
    return Price(price.amount * (100 - percent) / 100)
```

`tests/test_pricing.py`:

```python
from unittest.mock import patch

import pricing
from pricing import Price, apply_discount, fetch_rate


def test_price_is_price():
    assert isinstance(Price(10), Price)


def test_legacy_coupon_removed():
    assert not hasattr(pricing, "legacy_coupon")


@patch("pricing.client.get_rate", return_value=1.25)
def test_fetch_rate_returns_client_value(mock_get_rate):
    assert fetch_rate("EUR") == 1.25


def test_apply_discount():
    result = apply_discount(Price(100), percent=10)
    assert result is not None
```

Reply with one line per test in the form `<test name>: <delete, keep, or repair> - <reason>`. For each repair, say how you will show that the new assertion can fail. Then give the final test file in one code block.
