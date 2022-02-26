import pandas as pd
import os

def get_indicators(df):
    first_indicator = df.iloc[0]["Indicator Name"]
    index = 1
    curr_indicator = df.iloc[1]["Indicator Name"]
    indicators = [first_indicator]
    while curr_indicator != first_indicator:
        indicator = df.iloc[index]["Indicator Name"]
        indicators.append(indicator)
        index += 1
        curr_indicator = indicator

    return indicators


def get_years(df):
    cols = list(df.columns)
    nineteen_eighty = cols.index("1980")

    return [int(year) for year in cols[nineteen_eighty: ]]


def orient_dfs(dfs):
    indicators = []
    for df in dfs:
        indicators += get_indicators(df)
        years = get_years(df)
        assert (years[0] == 1980 and years[-1] == 2020)

    merged = dfs[0]
    for df in dfs[1:]:
        merged = merged.append(df)
    merged = merged.sort_values(by=["Country Code"])
    
    
def main():
    cwd = os.getcwd()
    pandas_list = []
    for file in os.listdir(cwd):
        if file.endswith(".xls"):
            print(file)
            pandas_list.append(pd.read_excel(file))

    pandas_list = orient_dfs(pandas_list)


if __name__ == "__main__":
    main()