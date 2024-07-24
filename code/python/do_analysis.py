import pickle
import pandas as pd


def main():
    penman_table, wscp_panel, wscp_static = load_data()
    merged_data = merge_data(wscp_panel, wscp_static)
    df = add_pb_and_ri(merged_data)
    sorted_medians = group_and_summarize(df)
    results = {
        "penman_table": penman_table,
        "replication_results": sorted_medians,
    }
    with open("output/results.pickle", "wb") as f:
        pickle.dump(results, f)


def load_data():
    """
    Load original_penman table, static and panel data from specified paths.nn

    Returns:
        tuple: Contains three dataframes, the original penman table, the panel data and static data.
    """
    penman_table = pd.read_csv("data/external/penman_2013_results.csv")
    penman_table.set_index("pb_group", inplace=True)
    wscp_static = pd.read_csv("data/external/wscp_static.txt", sep="\t")
    wscp_panel = pd.read_excel("data/external/wscp_panel.xlsx", engine="openpyxl")
    wscp_panel = wscp_panel.rename(columns={"year_": "year"})
    return penman_table, wscp_panel, wscp_static


def merge_data(wscp_panel, wscp_static):
    """
    Merge panel and static data, filtering for firms from the United States only.

    Args:
        wscp_panel (DataFrame): Panel data of firms.
        wscp_static (DataFrame): Static data of firms.

    Returns:
        DataFrame: Merged data with firms from the United States.
    """
    wscp_static_us = wscp_static[wscp_static["country"] == "UNITED STATES"]
    df = wscp_panel.merge(
        wscp_static_us[["isin"]], on="isin", how="inner", indicator=True
    )
    df = df[df["_merge"] == "both"]
    df.drop(columns="_merge", inplace=True)
    return df


def add_pb_and_ri(df):
    """
    Add P/B ratios and calculate Residual Income (RI) after encoding 'isin' into 'firmid'.

    Args:
        df (DataFrame): Data containing market and book values.

    Returns:
        DataFrame: Data enriched with P/B ratios and RI values.
    """
    df = df[(df["mve"] > 0) & (df["bve"] > 0)].copy()
    df.loc[:, "firmid"] = pd.factorize(df["isin"])[0]
    all_years = range(df["year"].min(), df["year"].max() + 1)
    all_firmids = df["firmid"].unique()
    grid = pd.MultiIndex.from_product(
        [all_firmids, all_years], names=["firmid", "year"]
    )
    df = df.set_index(["firmid", "year"]).reindex(grid).reset_index()
    df["pb"] = df["mve"] / df["bve"]
    df["l_bve"] = df.groupby("firmid")["bve"].shift(1)
    df["ri"] = df["ninc"] - 0.10 * df["l_bve"]
    df.drop(columns="l_bve", inplace=True)
    for i in range(0, 7):
        df[f"ri_{i}"] = df.groupby("firmid")["ri"].shift(-i) / df["bve"]
    df.dropna(subset=[f"ri_{i}" for i in range(0, 7)], inplace=True)
    return df


def group_and_summarize(df):
    """
    Group data by P/B ratio bins and summarize the median values of RI for sorting.

    Args:
        df (DataFrame): Data with calculated P/B ratios and RI.

    Returns:
        DataFrame: Median values of P/B and RI sorted by P/B ratios.
    """
    df.loc[:, "pb_group"] = pd.qcut(df["pb"], 20, labels=False, duplicates="drop")
    df.loc[:, "pb_group"] = df["pb_group"].max() - df["pb_group"] + 1
    ri_columns = [col for col in df if col.startswith("ri_")]
    return df.groupby("pb_group")[["pb"] + ri_columns].median()


if __name__ == "__main__":
    main()
