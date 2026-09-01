"""
=============================================================
  F1 Multi-Year Driver Data — Merge & Validate Script
=============================================================

PIPELINE:
  Yearly CSV files
       ↓
  Load each CSV
       ↓
  Extract & add `year` column (from filename)
       ↓
  Merge with pd.concat()
       ↓
  Validate merged dataset
       ↓
  Save to Data/combined/f1_drivers_2020_2026.csv

WHY each step matters is explained in comments throughout.
=============================================================
"""

import pandas as pd
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# SECTION 1 — Configure paths
# ─────────────────────────────────────────────────────────────
#
# We use pathlib.Path instead of raw strings like "data/2020.csv"
# because Path objects work correctly on Windows, Mac, and Linux
# (they handle the slash direction automatically).
#
# YEARS list makes this script scalable — to add 2027, just
# append 2027 to the list. No other code needs to change.

PROCESSED_DIR = Path("Data/Processed")   # where the yearly CSVs live
COMBINED_DIR  = Path("Data/combined")    # where we will save the master file
YEARS         = list(range(2020, 2027))  # [2020, 2021, 2022, 2023, 2024, 2025, 2026]


# ─────────────────────────────────────────────────────────────
# SECTION 2 — Load each yearly CSV and add a `year` column
# ─────────────────────────────────────────────────────────────
#
# WHY add a `year` column?
#   Without it, once we merge all datasets into one table we
#   lose track of which row came from which season.  The year
#   column lets us later filter, group, or plot by season —
#   essential for EDA, time-series analysis, and ML features.
#
# WHY extract the year from the filename instead of typing it?
#   Hard-coding "year = 2020" inside a loop is error-prone and
#   not scalable.  Parsing it from the filename means the script
#   always uses the correct year for whatever file it reads.

print("=" * 55)
print("  Step 1 — Loading yearly CSV files")
print("=" * 55)

yearly_frames = []   # we will collect one DataFrame per year here

for year in YEARS:
    filename  = f"{year}_F1_Drivers_Championship.csv"
    file_path = PROCESSED_DIR / filename

    if not file_path.exists():
        print(f"  [WARNING] File not found, skipping: {file_path}")
        continue

    # Read the CSV into a DataFrame
    df = pd.read_csv(file_path)

    # Extract year from filename (the first 4 characters) and add as a column
    # e.g. "2020_F1_Drivers_Championship.csv" → stem = "2020_F1..." → int("2020")
    df["year"] = int(file_path.stem[:4])

    print(f"  ✓ {year}: {len(df)} rows  |  columns: {list(df.columns)}")
    yearly_frames.append(df)

print()


# ─────────────────────────────────────────────────────────────
# SECTION 3 — Combine all yearly DataFrames with pd.concat()
# ─────────────────────────────────────────────────────────────
#
# WHY pd.concat() and not pd.merge()?
#   pd.merge() is for joining tables that share a key column
#   (like a SQL JOIN — e.g. matching drivers across seasons).
#   pd.concat() simply stacks DataFrames one on top of the other
#   (like pasting rows together), which is exactly what we want
#   when combining season data that has the same columns.
#
# WHY ignore_index=True?
#   Each yearly CSV has its own index starting at 0.
#   Without ignore_index=True the merged DataFrame would have
#   duplicate index values (0-19 repeated 7 times), which causes
#   confusing bugs.  ignore_index=True resets the index to a
#   single clean sequence: 0, 1, 2, … N.

print("=" * 55)
print("  Step 2 — Merging all yearly DataFrames")
print("=" * 55)

merged_df = pd.concat(yearly_frames, ignore_index=True)
print(f"  ✓ Merge complete. Total rows: {len(merged_df)}")
print()


# ─────────────────────────────────────────────────────────────
# SECTION 4 — Validate the merged dataset
# ─────────────────────────────────────────────────────────────
#
# WHY validate BEFORE cleaning?
#   Data problems discovered at the validation stage tell you
#   WHAT needs fixing and WHY.  If you clean blindly first you
#   may silently remove real F1 records (e.g. a driver who
#   scored 0 points is still a valid finisher).  Validate first,
#   investigate what you find, then make deliberate decisions.

print("=" * 55)
print("  Step 3 — Validating merged dataset")
print("=" * 55)

# ── 3a. Basic shape ──────────────────────────────────────────
print("\n Shape")
print(f"   Rows    : {merged_df.shape[0]}")
print(f"   Columns : {merged_df.shape[1]}")

# ── 3b. Column names ─────────────────────────────────────────
print("\n Column names")
for col in merged_df.columns:
    print(f"   • {col}")

# ── 3c. Data types ───────────────────────────────────────────
print("\n Data types (dtypes)")
print(merged_df.dtypes.to_string())

# ── 3d. Years present ────────────────────────────────────────
print("\n Years present in the merged dataset")
years_found = sorted(merged_df["year"].unique())
for y in years_found:
    count = len(merged_df[merged_df["year"] == y])
    print(f"   {y}  →  {count} drivers")

# Check for unexpected years
expected_years = set(YEARS)
found_years    = set(years_found)
unexpected     = found_years - expected_years
if unexpected:
    print(f"\n  ⚠️  Unexpected years found: {unexpected}")
else:
    print("   ✓ All years match expectations")

# ── 3e. Missing values ───────────────────────────────────────
print("\n Missing values per column")
missing = merged_df.isnull().sum()
if missing.sum() == 0:
    print("   ✓ No missing values found")
else:
    print(missing[missing > 0].to_string())

# ── 3f. Fully duplicate rows ─────────────────────────────────
print("\n Duplicate rows (completely identical rows)")
dup_count = merged_df.duplicated().sum()
if dup_count == 0:
    print("   ✓ No fully duplicate rows")
else:
    print(f"    {dup_count} duplicate rows found")
    print("   Preview of duplicates:")
    print(merged_df[merged_df.duplicated(keep=False)].head(10).to_string(index=False))

# ── 3g. Duplicate Driver+Year combinations ───────────────────
print("\n Duplicate Driver + Year combinations")
dup_driver_year = merged_df.duplicated(subset=["Driver", "year"]).sum()
if dup_driver_year == 0:
    print("   ✓ Each driver appears once per year")
else:
    print(f"   ⚠️  {dup_driver_year} duplicate Driver+Year pairs")
    print("   Preview:")
    mask = merged_df.duplicated(subset=["Driver", "year"], keep=False)
    print(merged_df[mask].sort_values(["Driver", "year"]).head(12).to_string(index=False))

# ── 3h. Null or blank driver names ───────────────────────────
print("\n Driver name checks")
blank_drivers = merged_df["Driver"].isna() | (merged_df["Driver"].str.strip() == "")
if blank_drivers.sum() == 0:
    print("   ✓ No null or blank driver names")
else:
    print(f"     {blank_drivers.sum()} null/blank driver names")

# ── 3i. Numeric column check ─────────────────────────────────
print("\n Numeric column check (Points & Pos)")
for col in ["Points", "Pos"]:
    if col in merged_df.columns:
        numeric_test = pd.to_numeric(merged_df[col], errors="coerce")
        non_numeric  = numeric_test.isna().sum()
        actual_dtype = merged_df[col].dtype
        if non_numeric == 0:
            print(f"   ✓ '{col}' is fully numeric  (dtype: {actual_dtype})")
        else:
            print(f"     '{col}' has {non_numeric} non-numeric values  (dtype: {actual_dtype})")
            bad_mask = numeric_test.isna()
            print(f"       Non-numeric samples: {merged_df.loc[bad_mask, col].unique()[:10]}")

# ── 3j. Points range sanity check ────────────────────────────
print("\n Points summary (do NOT remove zero-point drivers yet)")
print("   Zero-point drivers may represent real midfield/backmarker finishers")
print(merged_df["Points"].describe().to_string())

# ── 3k. Quick preview ────────────────────────────────────────
print("\n First 5 rows of merged dataset")
print(merged_df.head().to_string(index=False))
print()


# ─────────────────────────────────────────────────────────────
# SECTION 5 — Save the master dataset
# ─────────────────────────────────────────────────────────────
#
# WHY separate raw/processed and combined directories?
#   • Raw      → original scrape output, never modified
#   • Processed → per-year cleaned CSVs (our current source)
#   • Combined  → the single master file for EDA and ML
#   Keeping them separate means you can always regenerate the
#   combined file from the processed files without re-scraping.
#
# WHY create the directory before saving?
#   pandas .to_csv() will raise a FileNotFoundError if the
#   target directory does not exist.  mkdir(parents=True,
#   exist_ok=True) creates any missing parent folders and
#   silently succeeds if the folder already exists.

print("=" * 55)
print("  Step 4 — Saving master dataset")
print("=" * 55)

COMBINED_DIR.mkdir(parents=True, exist_ok=True)
output_path = COMBINED_DIR / "f1_drivers_2020_2026.csv"

merged_df.to_csv(output_path, index=False)
print(f"  ✓ Master dataset saved to: {output_path}")
print(f"    ({len(merged_df)} rows × {merged_df.shape[1]} columns)")
print()


# ─────────────────────────────────────────────────────────────
# SECTION 6 — What to investigate & do NEXT
# ─────────────────────────────────────────────────────────────
print("=" * 55)
print("  NEXT STEPS — reminder")
print("=" * 55)
print("""
  🔍 Data quality issues to investigate BEFORE cleaning:
     1. Drivers with 0 points  — real finishers or DNFs?
     2. Non-numeric Pos values — "NC", "DQ", "DNS", "DSQ"
     3. Duplicate Driver+Year  — split seasons or data error?
     4. Short driver names     — parsing artifact?
     5. Team name consistency  — e.g. "Red Bull" vs "Red Bull Racing"

  📊 After cleaning → EDA steps:
     1. Points distribution per year (histogram / boxplot)
     2. Top-N drivers across seasons (bar chart)
     3. Constructor dominance per year (grouped bar)
     4. Nationality breakdown (pie / treemap)
     5. Season parity (Gini index of points)

  🛠️  Feature engineering ideas (before ML):
     1. career_points       — cumulative points per driver across seasons
     2. avg_points_per_year
     3. seasons_active
     4. nationality_encoded — label / one-hot encode Nationality
     5. team_encoded
     6. champion            — binary flag (Pos == 1)
     7. podium_finisher     — binary flag (Pos <= 3)

  🤖 ML (ONLY after EDA + feature engineering):
     Start simple:
     • Logistic Regression  → predict champion (classification)
     • Linear Regression    → predict season points (regression)
     Then compare with tree-based models (Random Forest, XGBoost).
""")
print("=" * 55)
print("  Script complete!")
print("=" * 55)
