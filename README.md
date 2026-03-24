# myproject

シンプルなPythonプロジェクトのテンプレートです。

## ディレクトリ構成

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── docs/
│   └── index.md
├── setup.py
├── requirements.txt
├── README.md
└── .gitignore
```

## セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/yourname/myproject.git
cd myproject

# 仮想環境を作成・有効化
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 開発モードでインストール
pip install -e ".[dev]"
```

## 使い方

```python
from myproject.main import greet

print(greet("World"))  # Hello, World!
```

## テスト実行

```bash
pytest
# カバレッジ付き
pytest --cov=myproject
```

## ライセンス

MIT
