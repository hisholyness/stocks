from pprint import pprint

import pandas as pd
import yfinance as yf

df: pd.DataFrame = pd.read_csv('data/nasdaq_screener_1712527070153.csv')
df: pd.DataFrame = df[~df["Symbol"].isna()]
all_stocks = pd.DataFrame()

min_value = 50.0  # stocks that fall below $1.0 are at risk of being delisted from Nasdaq
for item in df['Symbol'].tolist():
    if isinstance(item, str):
        if "^" not in item:
            # try:
            information: yf.Ticker = yf.Ticker(item)
            new_row: pd.DataFrame = information.history(period="6mo")

            # don't buy stocks that are too low valued
            if (new_row["Low"] < min_value).any():
                continue

            recommendations: pd.DataFrame = information.get_recommendations()
            if not recommendations.empty:
                recommendations.drop(labels=["period"], axis=1, inplace=True)
                mean_df = recommendations.mean() + recommendations.std()
                if "buy" in mean_df.keys()[mean_df.argmax()].lower():
                    print(item)
            # information.fast_info['yearLow'], information.fast_info['fiftyDayAverage'], \
            # information.fast_info['twoHundredDayAverage'], information.fast_info['yearHigh']
                    new_row['Symbol'] = item

            # except:
            #     pass

pprint(all_stocks.head())

all_stocks.to_csv('all_stocks.csv', index=True)
