---
max_turns: 4
allowed_tools: [Read, Glob, Grep, Skill]
---

Use the PruneTests skill to clean up the test suite in `tests/test_sync.py`. `test_sync_pushes_changes` is slow and fails about one run in five on network timing, so it goes first. What else can go? Do not open a pull request, just tell me what to do with each test.

```python
from unittest.mock import MagicMock

from sync import SyncClient, sync


def test_client_is_client():
    assert isinstance(SyncClient("https://example.test"), SyncClient)


def test_sync_returns_mock_result():
    client = MagicMock()
    client.push.return_value = "ok"
    assert client.push() == "ok"


def test_sync_pushes_changes(live_server):
    client = SyncClient(live_server.url)
    sync(client, changes=["a", "b"])
    assert live_server.received == ["a", "b"]
```

Reply with one line per test in the form `<test name>: <delete, keep, or repair> - <reason>`.
