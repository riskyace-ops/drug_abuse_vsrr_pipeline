import os
import pandas as pd
from sqlalchemy import create_engine
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

MASTER_SQL = r"C:\Users\kingw\Documents\PYTHON\overdosePipeline\scripts\python\master_sql.sql"
EXPORT_CSV = r"G:\My Drive\overdosePipeline\national\master_overdose_full.csv"

# load and run


def run_master_sql():
    if not os.path.exists(MASTER_SQL):
        return

    with open(MASTER_SQL, "r", encoding="utf-8") as f:
        query = f.read()

    df = pd.read_sql(query, engine)
    df.to_csv(EXPORT_CSV, index=False)


if __name__ == "__main__":
    run_master_sql()
