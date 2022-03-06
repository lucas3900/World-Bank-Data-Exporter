import pandas as pd

YEARS = [2004, 2009, 2014, 2019]

def get_geographic_data():
    root = "data/gravity_data_"
    dfs = [pd.read_csv(f"{root}{year}.csv") for year in YEARS]

def get_bilateral_trade_data():
    df = pd.read_csv("data/bilateral_trade.csv")
    print(len(df["Country Name"].unique()))
    df.drop(df[(df["Time Period"] != 2004) & (df["Time Period"] != 2009) & (df["Time Period"] != 2014) & (df["Time Period"] != 2019)].index, inplace=True)


def main():
    # get_geographic_data()
    get_bilateral_trade_data()


if __name__ == "__main__":
    main()