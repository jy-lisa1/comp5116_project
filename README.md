# COMP 5116 Project

## Data
Access: https://zenodo.org/records/17957582

To process raw data:
- Download `globi-bees-filtered_file.tsv.gz` and place it in the `data/raw` folder. Some data preprocessing is done here, such as selecting relevant columns and dropping rows NaN values in key columns
- Run `trim_df.ipynb`, which will generate `processed/bees.parquet`

To load processed df:
- Write something like `df = pd.read_parquet("data/processed/bee_interactions.parquet")`

### Features
Feature information can be found in `data/features.json`.
  
Trimmed down set of features (can modify as needed):
#### Core interaction information
- `sourceTaxonName` - Most granular taxonomic name of the source (subject) of the interaction
- `targetTaxonName` - Most granular taxonomic name of the target (object) of the interaction
- `interactionTypeName` - Human-readable description of the interaction connecting the source and target (e.g., "eats")
- `interactionTypeId` - Machine-readable URI identifying the interaction type

#### Taxonomic information (optional; can be trimmed as needed)
- `sourceTaxonGenusName` — Genus of the source organism
- `targetTaxonGenusName` — Genus of the target organism
- `sourceTaxonFamilyName` — Family of the source organism
- `targetTaxonFamilyName` — Family of the target organism
- `sourceTaxonOrderName` — Order of the source organism
- `targetTaxonOrderName` — Order of the target organism

#### Temporal and geographical information
- `eventDate` - Date on which the interaction was observed or recorded
- `decimalLatitude` - Geographic latitude where the interaction was recorded
- `decimalLongitude` - Geographic longitude where the interaction was recorded

#### Data provenance
- `sourceNamespace` - Identifier/namespace of the dataset containing the interaction record
- `referenceCitation` - Citation associated with the recorded interaction claim
- `sourceCitation` - Citation associated with the dataset containing the interaction claim
