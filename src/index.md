# myproject ドキュメント

## 概要

myproject の使い方とAPIリファレンスです。

## インストール

```bash
pip install -e .
```

## クイックスタート

```python
from myproject.main import greet

print(greet("World"))  # Hello, World!
```

## API リファレンス

### `greet(name: str) -> str`

引数 `name` に挨拶を返します。

| 引数 | 型 | 説明 |
|------|----|------|
| `name` | `str` | 挨拶する相手の名前 |

**戻り値**: `"Hello, {name}!"` 形式の文字列
