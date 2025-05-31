import pandas as pd
import numpy as np

# CSVファイルの読み込み
df = pd.read_csv('EURUSD_H1.csv', parse_dates=['Date'], index_col='Date')

# EMAの計算
df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
df['EMA100'] = df['Close'].ewm(span=100, adjust=False).mean()

# エントリーシグナルの生成
df['Signal'] = 0
df['Signal'][df['EMA50'] > df['EMA100']] = 1
df['Signal'][df['EMA50'] < df['EMA100']] = -1

# ポジションの変化を検出
df['Position'] = df['Signal'].diff()

# バックテストの初期設定
initial_balance = 10000
balance = initial_balance
pips = 0
wins = 0
losses = 0
trades = 0

for i in range(1, len(df)):
    if df['Position'].iloc[i] == 2:  # ゴールデンクロス
        entry_price = df['Close'].iloc[i]
        for j in range(i+1, len(df)):
            price_change = df['Close'].iloc[j] - entry_price
            if price_change >= 0.0050:
                balance += 50
                pips += 50
                wins += 1
                trades += 1
                break
            elif price_change <= -0.0050:
                balance -= 50
                pips -= 50
                losses += 1
                trades += 1
                break
    elif df['Position'].iloc[i] == -2:  # デッドクロス
        entry_price = df['Close'].iloc[i]
        for j in range(i+1, len(df)):
            price_change = entry_price - df['Close'].iloc[j]
            if price_change >= 0.0050:
                balance += 50
                pips += 50
                wins += 1
                trades += 1
                break
            elif price_change <= -0.0050:
                balance -= 50
                pips -= 50
                losses += 1
                trades += 1
                break

# 結果の表示
print(f"初期残高: {initial_balance}")
print(f"最終残高: {balance}")
print(f"総取引回数: {trades}")
print(f"勝率: {wins / trades * 100:.2f}%")
print(f"平均獲得pips: {pips / trades:.2f}")