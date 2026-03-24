# Git ブランチ戦略

Gitのブランチ戦略とは、チームでコードを管理する際のブランチの作り方・運用ルールのことです。代表的な戦略を解説します。

---

## 1. Git Flow

最も広く知られた戦略です。リリースサイクルが明確なプロジェクトに向いています。

### ブランチ構成

| ブランチ | 役割 |
|----------|------|
| `main` | 本番リリース済みのコード |
| `develop` | 開発の統合ブランチ |
| `feature/*` | 新機能の開発 |
| `release/*` | リリース準備（バグ修正・バージョン更新） |
| `hotfix/*` | 本番の緊急バグ修正 |

### フロー図

```
main ────────────────────────────────────────●── (v1.1)
  \                                          /
   hotfix/fix-login ──────────────────────●

develop ──────────────────────────────●───────
           \              /      \   /
            feature/login        release/1.1
```

### 手順

```bash
# 新機能の開発
git checkout develop
git checkout -b feature/my-feature
# ... 開発 ...
git checkout develop
git merge --no-ff feature/my-feature

# リリース準備
git checkout -b release/1.0 develop
# ... バージョン番号の更新など ...
git checkout main
git merge --no-ff release/1.0
git tag -a v1.0

# 緊急修正
git checkout -b hotfix/critical-bug main
# ... 修正 ...
git checkout main
git merge --no-ff hotfix/critical-bug
git checkout develop
git merge --no-ff hotfix/critical-bug
```

### 向いているケース
- 定期リリース（週次・月次など）のプロジェクト
- 複数バージョンを同時にサポートする必要がある場合

---

## 2. GitHub Flow

シンプルさを重視した戦略です。継続的デプロイ（CD）との相性が良いです。

### ブランチ構成

| ブランチ | 役割 |
|----------|------|
| `main` | 常にデプロイ可能な状態を保つ |
| `feature/*` | すべての作業はここで行う |

### フロー図

```
main ──────────────────────────────────────────●──
          \                                   /
           feature/add-search ───────────────
                              (Pull Request)
```

### 手順

```bash
# ブランチを切る
git checkout -b feature/add-search

# 開発・コミット
git add .
git commit -m "Add search functionality"

# プッシュしてPull Requestを作成
git push origin feature/add-search
# → GitHub でPull Requestを作成してレビュー → main にマージ
```

### ルール
1. `main` は常にデプロイ可能な状態に保つ
2. 作業は必ずブランチで行う
3. プルリクエスト（PR）を通じてレビューしてからマージする

### 向いているケース
- 小〜中規模チーム
- 頻繁にデプロイするWebサービス

---

## 3. GitLab Flow

GitHub Flow に「環境ブランチ」を加えた戦略です。

### ブランチ構成

| ブランチ | 役割 |
|----------|------|
| `main` | 開発の統合ブランチ |
| `staging` | ステージング環境 |
| `production` | 本番環境 |
| `feature/*` | 機能開発 |

### フロー

```
feature/* → main → staging → production
```

### 向いているケース
- 複数の環境（dev / staging / prod）を持つプロジェクト
- デプロイを段階的に進めたい場合

---

## 4. Trunk Based Development

ブランチをほとんど作らず、全員が `main`（trunk）に直接コミットする戦略です。

### 特徴
- ブランチの寿命は最長でも1〜2日
- フィーチャーフラグで未完成機能を隠す
- 非常に高頻度のCIが前提

### 向いているケース
- 大規模チーム（Googleなどが採用）
- CI/CDが高度に整備された環境

---

## 戦略の選び方

| 条件 | 推奨戦略 |
|------|----------|
| 小規模チーム・高頻度デプロイ | GitHub Flow |
| 定期リリース・バージョン管理が必要 | Git Flow |
| 複数環境（staging/prod）がある | GitLab Flow |
| 大規模・高度なCI/CD環境 | Trunk Based Development |

---

## ブランチ命名規則の例

```
feature/  → 新機能         例: feature/user-auth
fix/      → バグ修正       例: fix/login-error
hotfix/   → 緊急修正       例: hotfix/payment-bug
release/  → リリース準備   例: release/2.1.0
chore/    → 設定・ドキュメント等  例: chore/update-deps
```

---

## コミットメッセージの慣例（Conventional Commits）

```
feat:     ユーザー認証機能を追加
fix:      ログイン時のエラーを修正
docs:     READMEを更新
chore:    依存パッケージを更新
refactor: 認証ロジックをリファクタリング
test:     ユーザーサービスのテストを追加
```
