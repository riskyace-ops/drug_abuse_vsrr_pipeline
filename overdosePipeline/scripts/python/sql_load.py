import pandas as pd
from sqlalchemy import create_engine, text
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

CSV_PATH = r"C:\Users\kingw\Documents\PYTHON\overdosePipeline\updated_data\vsrr_overdose_yearly.csv"

# load cleaned VSRR data into the database


def load_clean_data():
    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

    df = pd.read_csv(CSV_PATH)

    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS cleaned_vsrr_data;"))

    df.to_sql("cleaned_vsrr_data", engine, if_exists="replace", index=False)


if __name__ == "__main__":
    load_clean_data()
