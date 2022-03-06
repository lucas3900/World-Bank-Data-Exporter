import pandas as pd
from math import log

def get_geographic_data():
    df = pd.read_csv("gravity_data.csv")
    print(df)


def main():
    get_geographic_data()


if __name__ == "__main__":
    main()