import pandas as pd
import numpy as np

#----------------------------------------------------------------------------
spot_snapshot = pd.Series(
    {'nikkei': 34831.15,    # Nikkei 225 on 2024-08-08
     'JPYZAR': 0.124632},  # 1 JPY = 0.124632 ZAR
    name='2024-08-08'
)

config = {
    'initial_JPY': 1_000_000,
    'barrier': 0.70,
    'coupons': {1:1.17, 2:1.34, 3:1.51, 4:1.68, 5:1.85},
}

#----------------------------------------------------------------------------

maturities = pd.date_range(start="2025-08-22", periods=5, freq="12MS")

# ランダムな金利（ダミー）
np.random.seed(42)
jpy_rates = np.round(0.2 + np.random.rand(5) * 0.8, 3)  # 0.2〜1.0%
zar_rates = np.round(6.0 + np.random.rand(5) * 4.0, 3)  # 6.0〜10.0%

# DataFrameにまとめて maturity_date をインデックスに
df_yield_curve = pd.DataFrame({
    "JPY": jpy_rates,
    "ZAR": zar_rates
}, index=maturities)


# インデックスの名前を付ける
df_yield_curve.index.name = "maturity_date"

#----------------------------------------------------------------------------

# 1. Nikkeiの基準日
nikkei_dates = pd.to_datetime([
    "2024-08-15", "2025-08-15", "2026-08-17",
    "2027-08-16", "2028-08-16", "2029-08-15"
])

# 2. ZARJPYの基準日 = Nikkeiのうち先5つ + 7営業日
zarjpy_dates = nikkei_dates[1:] + BDay(7)

# 3. 資産名と日付を作成
dates = list(nikkei_dates) + list(zarjpy_dates)
assets = ["Nikkei"] * len(nikkei_dates) + ["ZARJPY"] * len(zarjpy_dates)

# 4. 乱数シミュレーション（標準正規乱数）
n_simulations = 10
np.random.seed(42)  # 再現性のため
random_values = np.random.normal(loc=0, scale=1, size=(len(dates), n_simulations))

# 5. DataFrameの作成
df_random = pd.DataFrame(random_values, columns=[f"sim_{i+1}" for i in range(n_simulations)])
df_random.insert(0, "Asset", assets)
df_random.insert(0, "Date", dates)