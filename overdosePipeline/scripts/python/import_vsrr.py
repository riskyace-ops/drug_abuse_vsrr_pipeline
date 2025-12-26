import requests
import pandas as pd
from datetime import datetime

VSRR_URL = "https://data.cdc.gov/api/views/xkb8-kh2a/rows.csv?accessType=DOWNLOAD"

LOCAL_PATH = r"G:\My Drive\overdosePipeline\national\vsrr_overdose_yearly.csv"
TEMP_PATH = r"C:\Users\kingw\Documents\PYTHON\overdosePipeline\data\vsrr_overdose_temp.csv"
LOG_PATH = r"C:\Users\kingw\Documents\PYTHON\overdosePipeline\logs\logs.txt"

MONTH_MAP = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}


def log(msg):
    with open(LOG_PATH, "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")


def download_latest():
    r = requests.get(VSRR_URL)
    r.raise_for_status()
    with open(TEMP_PATH, "wb") as f:
        f.write(r.content)
    log("Downloaded lastest dataset")


# only keep december rows because of rolling period
def update_dataset():
    df = pd.read_csv(TEMP_PATH)

    df.columns = [c.strip() for c in df.columns]
    df["MonthNum"] = df["Month"].map(MONTH_MAP)

    df_dec = df[df["MonthNum"] == 12].copy()
    df_dec.rename(columns={"Data Value": "Total Deaths"}, inplace=True)

    df_final = df_dec[
        ["Year", "State Name", "Indicator", "Total Deaths"]
    ].sort_values(["State Name", "Year", "Indicator"])

    df_final.to_csv(LOCAL_PATH, index=False)

    log(f"Saved cleaned annual dataset with {len(df_final)} rows")


if __name__ == "__main__":
    download_latest()
    update_dataset()
    log("VSRR import process done")
