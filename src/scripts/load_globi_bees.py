from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "globi-bees-filtered_file.tsv.gz"

KEEP_COLUMNS = [
    # core interaction info
    "sourceTaxonName",
    "targetTaxonName",
    "interactionTypeName",
    "interactionTypeId",

    # taxonomic info (optional, could be useful depending on what we wanna do)
    "sourceTaxonGenusName",
    "targetTaxonGenusName",
    "sourceTaxonFamilyName",
    "targetTaxonFamilyName",
    "sourceTaxonOrderName",
    "targetTaxonOrderName",

    # temporal and geographical info
    "eventDate",
    "decimalLatitude",
    "decimalLongitude",

    # data provenance (not sure if we need these)
    "sourceNamespace",
    "referenceCitation",
    "sourceCitation",
]

# columns whose values must be present in the df, otherwise drop the row
REQUIRED_COLUMNS = ["eventDate", "sourceTaxonName", "targetTaxonName"]

def load_data():
    """Load the compressed GloBI TSV into a pandas DataFrame."""
    available_columns = [
        col for col in KEEP_COLUMNS
        if col in pd.read_csv(
            DATA_FILE,
            sep="\t",
            compression="gzip",
            nrows=0
        ).columns
    ]

    df = pd.read_csv(
        DATA_FILE,
        sep="\t",
        compression="gzip",
        usecols=available_columns,
        low_memory=False
    )

    df["eventDate"] = pd.to_datetime(
            df["eventDate"],
            format="ISO8601",
            utc=True,
            errors="coerce"
    )

    df = df.dropna(subset=REQUIRED_COLUMNS)
    
    return df


if __name__ == "__main__":
    df = load_data()
    print(f"Loaded {len(df):,} rows and {len(df.columns):,} columns.")
    print(f"Columns: {', '.join(df.columns)}")
