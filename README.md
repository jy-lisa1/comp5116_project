# COMP 5116 Project

## Data
Access: https://zenodo.org/records/17957582
- Feature information can be found in `data/features.json`

To process raw data:
- Download `globi-bees-filtered_file.tsv.gz` and place it in the `data/raw` folder. Some data preprocessing is done here, such as selecting relevant columns and dropping rows NaN values in key columns
- Run `trim_df.ipynb`, which will generate `processed/bees.parquet`

To load processed df:
- Write something like `df = pd.read_parquet("data/processed/bee_interactions.parquet")`
