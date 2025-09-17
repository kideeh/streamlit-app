import pandas as pd
import argparse

# setup argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="Path to metadata.csv")
parser.add_argument("--out", required=True, help="Path to save cleaned sample")
parser.add_argument("--sample_frac", type=float, default=0.05, help="Fraction of data to sample")
args = parser.parse_args()

print("Loading data...")

# load dataset, skip bad lines if found
df = pd.read_csv(args.input, low_memory=False, on_bad_lines="skip")

print(f"Original rows: {len(df)}")

# keep only rows with required info
df = df.dropna(subset=["title", "publish_time"])

# convert publish_time to datetime safely
df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
df = df.dropna(subset=["publish_time"])

# add year column
df["year"] = df["publish_time"].dt.year

# sample data (smaller for easy testing)
if args.sample_frac < 1.0:
    df = df.sample(frac=args.sample_frac, random_state=42)

print(f"Cleaned rows: {len(df)}")

# save cleaned sample
df.to_csv(args.out, index=False)
print(f"Saved cleaned data to {args.out}")
# load dataset, skip bad lines if found
df = pd.read_csv(args.input, low_memory=False, on_bad_lines="skip")

# normalize column names (strip whitespace)
df.columns = df.columns.str.strip()
print("Columns after cleaning:", df.columns.tolist())
