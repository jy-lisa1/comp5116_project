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

BEE_ORDER = "Hymenoptera"
PLANT_ORDERS = [
    "Rosales",
    "Asterales",
    "Ericales",
    "Ranunculales",
    "Apiales",
    "Myrtales",
    "Lamiales",
    "Brassicales",
    "Malvales",
    "Malpighiales",
    "Solanales",
    "Fabales",
    "Dipsacales",
    "Gentianales",
    "Caryophyllales",
    "Liliales",
    "Boraginales",
    "Poales",
    "Cornales",
    "Sapindales",
    "Asparagales",
    "Saxifragales",
    "Oxalidales",
    "Piperales",
    "Geraniales",
    "Cupressales",
    "Fagales",
    "Magnoliales",
    "Vitales",
    "Pinales",
    "Proteales",
    "Arecales",
    "Zingiberales",
    "Laurales",
    "Buxales",
    "Dilleniales",
    "Santalales",
    "Nymphaeales",
    "Aquifoliales",
    "Alismatales",
    "Pandanales",
    "Cycadales",
    "Austrobaileyales",
    "Canellales",
    "Gnetales",
]

BEE_FAMILIES = [
    "Apidae",
    "Andrenidae",
    "Colletidae",
    "Halictidae",
    "Megachilidae",
    "Melittidae",
]

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

    # filter for only bees and plants interactions
    df = df[
    (
        df["sourceTaxonFamilyName"].isin(BEE_FAMILIES)
        & df["targetTaxonOrderName"].isin(PLANT_ORDERS)
    )
    |
    (
        df["targetTaxonFamilyName"].isin(BEE_FAMILIES)
        & df["sourceTaxonOrderName"].isin(PLANT_ORDERS)
    )
]

    return df

def save_data(df: pd.DataFrame, output_file: Path):
    project_root = next(
        (path for path in (Path.cwd(), *Path.cwd().parents)
        if (path / "data" / "raw").is_dir()),
        None,
    )
    if project_root is None:
        raise RuntimeError("Could not locate the project root containing data/raw")

    processed_dir = project_root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    output_file = processed_dir / "bees.parquet"
    df.to_parquet(output_file, index=False)
    print(f"Saved {len(df):,} rows to {output_file}")


if __name__ == "__main__":
    df = load_data()
    save_data(df, Path("data/processed/bees.parquet"))
