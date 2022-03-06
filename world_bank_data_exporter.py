import pandas as pd
import os
import geographic_exporter

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
    nineteen_eighty = cols.index("2000")

    return [int(year) for year in cols[nineteen_eighty: ]]


def orient_dfs(dfs):
    indicators = []
    years = None
    for df in dfs:
        indicators += get_indicators(df)
        years = get_years(df)
        assert (years[0] == 2000 and years[-1] == 2020)

    merged = dfs[0]
    for df in dfs[1:]:
        merged = merged.append(df)
    merged = merged.sort_values(by=["Country Code"])

    df = pd.DataFrame()
    index = 0
    start_country = merged.iloc[0]["Country Code"]
    while index < len(merged.index):
        rows = [{
            "country_name": merged.iloc[index]["Country Name"],
            "country_code": merged.iloc[index]["Country Code"]
        } for _ in range(len(years))]
        year = 2000
        for row in range(len(rows)):
            rows[row]["year"] = year
            year += 1
        while merged.iloc[index]["Country Code"] == start_country:
            indicator = merged.iloc[index]["Indicator Name"]
            year = 2000
            for row in rows:
                row[indicator] = merged.iloc[index][str(year)]
                year += 1

            index += 1
            if index == len(merged.index):
                break
        
        if index == len(merged.index):
            break

        df = df.append(rows)
        start_country = merged.iloc[index]["Country Code"]

    return df


def main():
    cwd = os.getcwd() + '/data'
    print(cwd)
    pandas_list = []
    for file in os.listdir(cwd):
        if file.endswith(".xls"):
            print(file)
            pandas_list.append(pd.read_excel("data/" + file))

    df = orient_dfs(pandas_list)

    df.to_excel("world_bank_stata.xlsx")


if __name__ == "__main__":
    main()