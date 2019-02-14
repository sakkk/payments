import json
from flask import Flask, render_template, redirect, request, Markup, escape
from datetime import datetime

application = Flask(__name__)

DATA_FILE = 'payments.json'

def save_data(item, amount, memo, created_at):
    """記録データを保存します
    :param item: 項目
    :type item: str
    :param amount: 金額
    :type amount: str
    :param memo: メモ
    :type memo: str
    :param created_at: 日付
    :type created_at: datetime.datetime
    :return None
    """

    try:
        # jsonモジュールでデータベースファイルを開きます
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []

    database.insert(0, {
        "item": item,
        "amount": amount,
        "memo": memo,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M")
    })

    json.dump(database, open(DATA_FILE, mode="w", encoding="utf-8"), indent=4, ensure_ascii=False)

def load_data():
    """記録データを返します"""
    try:
        # jsonモジュールでデータベースファイルを開きます
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []

    return database

@application.route('/')
def index():
    """トップページテンプレートを使用してページを表示します"""
    # 記録データを読み込みます
    deals = load_data()
    return render_template('index.html', deals=deals)

@application.route('/save', methods=['POST'])
def save():
    """記録用URL"""
    # 記録されたデータを取得します
    item = request.form.get('item') # 項目
    amount = request.form.get('amount') # 金額
    memo = request.form.get('memo') # メモ
    created_at = datetime.now() # 記録日時

    save_data(item, amount, memo, created_at)

    # 保存後はトップページにリダイレクトします
    return redirect('/')

@application.template_filter('nl2br')
def nl2br_filter(s):
    """改行文字をbrタグに置き換えるテンプレートフィルター"""
    return escape(s).replace('\n', Markup('<br>'))

def main():
    application.run('127.0.0.1', 8000)

if __name__ == '__main__':
    # IPアドレス127.0.0.1の8000番ポートでアプリケーションを実行します
    application.run('127.0.0.1', 8000, debug=True)
