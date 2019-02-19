# peing clone
- [Peing-質問箱](https://peing.net/ja/)
- 勉強用

## 環境作成
```
git clone git@github.com:yamap55/peing_clone.git
cd peing_clone
python -m venv .venv
source .venv/bin/activate # .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## memo
- Flask
- Flask-Login
    - login
- Flask-SQLAlchemy
    - orm
- Flask-WTF
    - form

## 目標
- 2月中
    - できてなくても2月で終わり
- サクッと作る

## やること
- サクッと作る
- ログイン
    - passwordハッシュ化
- ログアウト
- ユーザ登録
- 一覧
- 質問登録
- 回答登録
- どこかサーバで動かす

## やらないこと（やりたいけど）
- firebase
- vue.js
- 画面デザイン
    - bootstrap位はやる？
- spa
- Twitter認証
    - Twitter連携
