import numpy as np
import pandas as pd

def generate_dummy_yield_curve():
    """
    ダミーのイールドカーブ（JPYおよびZAR）を生成する関数。

    - 満期日は以下の5日間を手動で設定：
        - 2025年8月26日
        - 2026年8月26日
        - 2027年8月25日
        - 2028年8月25日
        - 2029年8月24日

    - JPY金利は0.2%〜1.0%、ZAR金利は6.0%〜10.0%の範囲でランダムに生成される。
    - 出力は maturity_date をインデックスとする pandas.DataFrame 形式。

    Returns:
        pd.DataFrame: JPY および ZAR の金利を持つイールドカーブのダミーデータ
    """

    # 満期日を手動で指定
    maturities = pd.to_datetime([
        "2025-08-26", "2026-08-26", "2027-08-25",
        "2028-08-25", "2029-08-24"
    ])
    
    # 金利のダミーデータをランダムに生成（再現性のためにシード固定）
    np.random.seed(42)
    jpy_rates = np.round(0.2 + np.random.rand(len(maturities)) * 0.8, 3)
    zar_rates = np.round(6.0 + np.random.rand(len(maturities)) * 4.0, 3)

    # DataFrame の構築
    df = pd.DataFrame({
        "maturity_date": maturities,
        "JPY": jpy_rates,
        "ZAR": zar_rates
    })

    # maturity_date をインデックスに設定
    df.set_index("maturity_date", inplace=True)

    return df


def generate_random_variables(n_simulations=10, seed=42):
    """
    Nikkei225とZARJPYの将来日付に対応した乱数シミュレーション用DataFrameを生成する関数。

    Parameters:
        n_simulations (int): シミュレーション本数
        seed (int): 乱数シード（再現性確保）

    Returns:
        pd.DataFrame: 2列（Date, Asset）+ n_simulations列から成る乱数シミュレーション用DataFrame
    """

    np.random.seed(seed)

    # 1. Nikkei日付（6点）
    nikkei_dates = pd.to_datetime([
        "2024-08-15", "2025-08-15", "2026-08-17",
        "2027-08-16", "2028-08-16", "2029-08-15"
    ])

    # 2. ZARJPY日付（5点）
    zarjpy_dates = pd.to_datetime([
        "2025-08-26", "2026-08-26", "2027-08-25",
        "2028-08-25", "2029-08-24"
    ])

    # 3. 日付・資産名結合
    dates = list(nikkei_dates) + list(zarjpy_dates)
    assets = ["Nikkei"] * len(nikkei_dates) + ["JPYZAR"] * len(zarjpy_dates)

    # 4. 平均・標準偏差設定
    means = np.array([35000 if asset == "Nikkei" else 0.125 for asset in assets])
    stddevs = np.array([1000 if asset == "Nikkei" else 0.01 for asset in assets])

    # 5. 正規乱数を生成し、負値を避ける（例：clipで0.001以上に）
    random_matrix = np.random.normal(loc=means[:, None], scale=stddevs[:, None], size=(len(dates), n_simulations))
    random_matrix = np.clip(random_matrix, a_min=0.001, a_max=None)

    # 6. DataFrame構築
    df = pd.DataFrame(random_matrix, columns=[f"sim_{i+1}" for i in range(n_simulations)])
    df.insert(0, "Asset", assets)
    df.insert(0, "Date", dates)

    return df
