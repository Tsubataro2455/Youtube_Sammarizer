# YouTube Summarizer 🎞️

Claude AIを使用して、YouTube動画の字幕を自動的に日本語で要約する強力なStreamlitウェブアプリケーション。

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.63+-red)
![LangChain](https://img.shields.io/badge/LangChain-1.4+-green)
![Claude](https://img.shields.io/badge/Claude-API-blueviolet)

## 特徴

- 🎯 **自動要約** - 長いYouTube字幕を簡潔な日本語の要約に変換
- 🤖 **Claude AI搭載** - 最先端のClaudeモデル（Haiku & Sonnet）を使用
- 🎚️ **モデル選択** - Haiku（高速・低コスト）またはSonnet（高精度）を選択可能
- 📺 **動画メタデータ** - 動画タイトルと投稿者を自動表示
- 🔄 **Map-Reduceアルゴリズム** - 長い字幕を独立して要約し、結合する戦略
- 🐳 **Docker対応** - Docker & Docker Composeで簡単にデプロイ可能
- 🌐 **Webインターフェース** - 使いやすいStreamlitのUI

## 必要な環境

- Docker & Docker Compose
- Anthropic API キー ([こちらから取得](https://console.anthropic.com))
- インターネット接続

## クイックスタート

### 1. リポジトリをクローン
```bash
git clone https://github.com/yourusername/youtube-summarizer.git
cd youtube-summarizer
```

### 2. APIキーを設定
```bash
cp .env.example .env
# .envファイルを編集してAnthropic APIキーを追加
# ANTHROPIC_API_KEY=sk-ant-...
```

### 3. アプリケーションを起動
```bash
docker compose up -d
```

### 4. アプリにアクセス
ブラウザで以下のURLにアクセス: **http://localhost:8501**

## 使用方法

1. **YouTube URLを入力** - 任意のYouTube動画URLを入力フィールドに貼り付け
2. **モデルを選択** - Claude Haiku（高速）またはClaude Sonnet（より詳細）を選択
3. **要約を生成** - AIが字幕を要約するのを待つ
4. **結果を表示** - 要約と元のテキストを表示

## 技術スタック

- **フロントエンド**: [Streamlit](https://streamlit.io/) - Pythonウェブアプリ開発フレームワーク
- **LLM**: [Claude API](https://www.anthropic.com/api) (Anthropic提供)
- **フレームワーク**: [LangChain](https://www.langchain.com/) - LLMオーケストレーション
- **コンテナ化**: Docker & Docker Compose
- **ライブラリ**:
  - `langchain-anthropic` - Claude統合
  - `langchain-community` - YouTube字幕ローダー
  - `langchain-text-splitters` - インテリジェントなテキスト分割
  - `youtube-transcript-api` - 動画字幕抽出
  - `requests` - メタデータスクレイピング用HTTPクライアント

## プロジェクト構成

```
youtube-summarizer/
├── src/
│   └── main.py           # メインのStreamlitアプリケーション
├── docker-compose.yml    # Docker Compose設定
├── Dockerfile           # Dockerイメージ仕様
├── requirements.txt     # Python依存関係
├── .env                 # 環境変数（APIキー）
├── .env.example         # 環境変数テンプレート
├── .gitignore          # Git無視ルール
├── CLAUDE.md           # 開発ガイド
├── LICENSE             # MITライセンス
└── README.md           # このファイル
```

## 動作原理

### アーキテクチャ
このアプリは **Map-Reduce要約戦略** を使用して、任意の長さの動画に対応します:

1. **読み込み** - LangChainのYoutubeLoaderを使用してYouTube字幕を取得
2. **分割** - 字幕を最適処理のため4000文字のチャンクに分割
3. **Map** - Claudeで各チャンクを独立して要約
4. **Reduce** - 個別の要約を1つの一貫性のある要約に結合
5. **表示** - 動画メタデータ、要約、元のテキストを表示

### 主な設計決定
- **pytube エラー回避**: `add_video_info=False`を使用してpytubeの内部エラーを防止
- **文字ベースのチャンク分割**: 重いtiktokenの依存を避ける
- **個別メタデータ取得**: JSON-LDスクレイピングでタイトルと投稿者を抽出
- **固定チャンクサイズ**: 4000文字が両モデルに最適

## 設定

### 環境変数
`.env`ファイルで以下を設定:

```bash
ANTHROPIC_API_KEY=sk-ant-...  # あなたのAnthropic APIキー
```

### アプリ設定
- **ポート**: 8501 (Streamlitのデフォルトポート)
- **チャンクサイズ**: 4000文字
- **モデルコンテキスト**: 200Kトークン（HaikuとSonnetの両方）

## 開発

### 必要な環境
- Docker & Docker Compose
- Python 3.11以上
- StreamlitとLangChainの基礎知識

### ローカル開発セットアップ

```bash
# コンテナを起動
docker compose up -d

# 依存関係をインストール
docker compose exec -it app pip install -r requirements.txt

# アプリを実行
docker compose exec -it app streamlit run src/main.py --server.address=0.0.0.0
```

### 新しい依存関係を追加

```bash
# コンテナ内にインストール
docker compose exec -it app pip install <package-name>

# requirements.txtを更新
docker compose exec -it app pip freeze > requirements.txt

# コンテナを再構築
docker compose build --no-cache
docker compose down && docker compose up -d
```

### コード品質

このプロジェクトはクリーンコード原則に従っています:
- 責務が明確なモジュール設計
- 包括的なエラーハンドリング
- 適切な型ヒント
- 明確性のための日本語コメント
- UI層とロジック層の分離

詳細は [CLAUDE.md](./CLAUDE.md) をご覧ください。

## トラブルシューティング

### 「字幕を取得できませんでした」というエラー
- 動画に字幕が有効になっていることを確認
- 別の動画を試してみる
- インターネット接続を確認

### 「無効なYouTube URL」というエラー
- URLフォーマットを確認: `https://www.youtube.com/watch?v=VIDEO_ID`
- 直接的なYouTubeリンクを使用していることを確認

### APIキーエラー
- `.env`ファイルのAPIキーが正しいことを確認
- https://console.anthropic.com でAPIキーの権限を確認
- `sk-ant-`で始まっていることを確認

### コンテナが起動しない
```bash
# イメージを再構築
docker compose build --no-cache

# コンテナを再起動
docker compose down && docker compose up -d

# ログを確認
docker compose logs -f app
```

## パフォーマンス

- **Haiku モデル**: 一般的な動画（5～15分）で約10～30秒
- **Sonnet モデル**: 一般的な動画（5～15分）で約15～45秒
- 処理時間は動画の長さと字幕サイズに依存

## 制限事項

- 英語または日本語の字幕がある動画のみに対応
- 長い動画（2時間以上）は要約に数分かかる可能性あり
- API呼び出しのためアクティブなインターネット接続が必要

## ライセンス

このプロジェクトはMITライセンスの下で公開されています - 詳細はLICENSEファイルをご覧ください。

## 貢献

貢献を歓迎します！以下の手順で貢献できます:
1. リポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを開く

## サポート

問題、質問、提案については:
- [GitHub Issues](https://github.com/yourusername/youtube-summarizer/issues) を作成
- 既存のIssueで解決策を確認
- [CLAUDE.md](./CLAUDE.md) 開発ガイドを参照

## 謝辞

- [Anthropic](https://www.anthropic.com/) - Claude API提供
- [Streamlit](https://streamlit.io/) - 優れたWebフレームワーク提供
- [LangChain](https://www.langchain.com/) - LLMオーケストレーションツール提供
- [YouTube Transcript API](https://github.com/jdelatorrealba/youtube-transcript-api) - 字幕抽出機能提供

## ロードマップ

- [ ] 複数言語対応（日本語以外）
- [ ] 複数動画のバッチ処理
- [ ] ビデオベースの要約（音声分析）
- [ ] カスタム要約長オプション
- [ ] PDF/DOCXへのエクスポート機能
- [ ] プログラム的アクセス用APIエンドポイント

---

**Claude AIで作成 ❤️**
