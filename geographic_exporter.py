import pandas as pd

YEARS = [2004, 2009, 2014, 2019]

def get_geographic_data():
    root = "data/gravity_data_"
    dfs = [pd.read_csv(f"{root}{year}.csv") for year in YEARS]

    return dfs

def get_bilateral_trade_data():
    df = pd.read_csv("data/bilateral_trade.csv")
    return df


def main():
    geographic_data = get_geographic_data()
    trade_data = get_bilateral_trade_data()
    good_countries = []
    for country in trade_data["Country Name"].unique():
        if all([country in df["country_o"].unique() for df in geographic_data]):
            good_countries.append(country)
    print(good_countries)
    for df in geographic_data:
        df = df[df["country_o"].isin(good_countries)]
        df = df[df["country_d"].isin(good_countries)]
    trade_data = trade_data[trade_data["Country Name"].isin(good_countries)]
    trade_data = trade_data[trade_data["Counterpart Country Name"].isin(good_countries)]

    for country in good_countries:
        for i in range(len(geographic_data)):
            df = geographic_data[i]
            for year in range(2000 + (i * 5) , 2000 + ((i + 1) * 5)):
                country_geo_data = df.loc[(df["country_o"] == country) & (df["year"] == year)]
                country_trade_data = trade_data.loc[(trade_data["Country Name"] == country) & (trade_data["Time Period"] == year)]
                print(country_geo_data)
                print(country_trade_data)
                exit()


if __name__ == "__main__":
    main()