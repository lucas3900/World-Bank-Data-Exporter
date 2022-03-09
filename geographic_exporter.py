from itertools import count
import pandas as pd

YEARS = [2004, 2009, 2014, 2019]

def get_geographic_data():
    root = "data/gravity_data_"

    return [pd.read_csv(f"{root}{year}.csv") for year in YEARS]

def get_bilateral_trade_data():
    df = pd.read_csv("data/bilateral_trade.csv", low_memory=False)

    return df


def main():
    geographic_data = get_geographic_data()
    trade_data = get_bilateral_trade_data()
    world_bank_data = pd.read_excel("output/world_bank_stata.xlsx")
    good_countries = []
    for country in trade_data["Country Name"].unique():
        if all([country in df["country_o"].unique() for df in geographic_data]):
            if country in world_bank_data["country_name"].unique():
                good_countries.append(country)
    china_trade = "China, P.R.: Mainland"
    good_countries.append("China")
    print(len(good_countries), "Countries Available")
    """
    geographic data -> Gravity Data Set
    trade data -> DOTS
    world bank -> world bank
    """
    for df in geographic_data:
        df = df[df["country_o"].isin(good_countries)]
        df = df[df["country_d"].isin(good_countries)]
    trade_data = trade_data[trade_data["Country Name"].isin(good_countries + [china_trade])]
    trade_data = trade_data[trade_data["Counterpart Country Name"].isin(good_countries + [china_trade])]
    trade_data.fillna(0, inplace=True)
    world_bank_data = world_bank_data[world_bank_data["country_name"].isin(good_countries)]

    """
    GDP -> world_bank_data["GDP (current US$)"] *
    Trade_ij -> bilateral_trade["Goods, Value of Exports, Free on board (FOB), US Dollars (TXG_FOB_USD)"]
                + bilateral_trade["Goods, Value of Imports, Cost, Insurance, Freight (CIF), US Dollars (TMG_CIF_USD)"] 
    Distance -> geographic_data["distance"] *
    Population -> geographic_data["pop"] or world_bank_data["Population, total"] *
    Area -> world_bank_data["Land area (sq. km)"] *
    Landlocked -> geographic_data["landlocked_"] *
    Common Borders -> geographic_data["contiguity"] *
    """
    exports_index = "Goods, Value of Exports, Free on board (FOB), US Dollars (TXG_FOB_USD)"
    imports_index = "Goods, Value of Imports, Cost, Insurance, Freight (CIF), US Dollars (TMG_CIF_USD)"
    bilateral_trade_df = pd.DataFrame(
        columns=["trade_over_gdp", "pop_i", "pop_j", "area_i", "area_j", 
                 "distance", "landlocked_i", "landlocked_j", "common_border"])
    obs = 0
    for country_i in good_countries:
        print("Inserting for", country_i)
        for country_j in good_countries:
            if country_i != country_j:
                for i in range(len(geographic_data)):
                    geo_df = geographic_data[i]
                    for year in range(2000 + (i * 5) , 2000 + ((i + 1) * 5)):
                        # country_geo_data = df.loc[(df["country_o"] == country_a) & (df["year"] == year)]
                        # if country_a == "China":
                        #     country_trade_data = trade_data.loc[(trade_data["Country Name"] == china_trade) & (trade_data["Time Period"] == year)]
                        gdp_i = world_bank_data.loc[(world_bank_data["country_name"] == country_i)
                                                  & (world_bank_data["year"] == year), "GDP (current US$)"].iloc[0]
                        gdp_j = world_bank_data.loc[(world_bank_data["country_name"] == country_j)
                                                  & (world_bank_data["year"] == year), "GDP (current US$)"].iloc[0]
                        pop_i = world_bank_data.loc[(world_bank_data["country_name"] == country_i)
                                                  & (world_bank_data["year"] == year), "Population, total"].iloc[0]
                        pop_j = world_bank_data.loc[(world_bank_data["country_name"] == country_j)
                                                  & (world_bank_data["year"] == year), "Population, total"].iloc[0]
                        area_i = world_bank_data.loc[(world_bank_data["country_name"] == country_i)
                                                  & (world_bank_data["year"] == year), "Land area (sq. km)"].iloc[0]
                        area_j = world_bank_data.loc[(world_bank_data["country_name"] == country_j)
                                                  & (world_bank_data["year"] == year), "Land area (sq. km)"].iloc[0]
                        distance_ij = geo_df.loc[(geo_df["country_o"] == country_i) & (geo_df["country_d"] == country_j)
                                                & (geo_df["year"] == year), "distance"].iloc[0]
                        landlocked_i = geo_df.loc[(geo_df["country_o"] == country_i) & (geo_df["country_d"] == country_j)
                                                & (geo_df["year"] == year), "landlocked_o"].iloc[0]
                        landlocked_j = geo_df.loc[(geo_df["country_o"] == country_i) & (geo_df["country_d"] == country_j)
                                                & (geo_df["year"] == year), "landlocked_d"].iloc[0]
                        common_border_ij = geo_df.loc[(geo_df["country_o"] == country_i) & (geo_df["country_d"] == country_j)
                                                & (geo_df["year"] == year), "contiguity"].iloc[0]
                        
                        country_i_trade = china_trade if country_i == "China" else country_i
                        country_j_trade = china_trade if country_j == "China" else country_j

                        try:
                            imports_ij = trade_data.loc[(trade_data["Country Name"] == country_i_trade)
                                                    & (trade_data["Counterpart Country Name"] == country_j_trade)
                                                    & (trade_data["Time Period"] == year), imports_index].iloc[0]
                            imports_ji = trade_data.loc[(trade_data["Country Name"] == country_j_trade)
                                                    & (trade_data["Counterpart Country Name"] == country_i_trade)
                                                    & (trade_data["Time Period"] == year), imports_index].iloc[0]
                            exports_ij = trade_data.loc[(trade_data["Country Name"] == country_i_trade)
                                                    & (trade_data["Counterpart Country Name"] == country_j_trade)
                                                    & (trade_data["Time Period"] == year), exports_index].iloc[0]
                            exports_ji = trade_data.loc[(trade_data["Country Name"] == country_j_trade)
                                                    & (trade_data["Counterpart Country Name"] == country_i_trade)
                                                    & (trade_data["Time Period"] == year), exports_index].iloc[0]
                            trade_ij = imports_ij + imports_ji + exports_ij + exports_ji
                        except:
                            trade_ij = 0
                        # print(gdp_i, gdp_j, pop_i, pop_j, area_i, area_j, distance_ij, landlocked_i, landlocked_j, common_border_ij, imports_ij, imports_ji, exports_ij, exports_ji, trade_ij)
                        bilateral_trade_df.loc[obs] = [trade_ij / gdp_i, pop_i, pop_j, area_i, area_j, distance_ij, landlocked_i, landlocked_j, common_border_ij]
                        obs += 1
    print(bilateral_trade_df)
    bilateral_trade_df.to_excel("output/bilateral_trade.xlsx")
                        

if __name__ == "__main__":
    main()