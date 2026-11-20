import numpy as np
import pandas as pd

def create_dataset(n_rows=1000, seed=42):
    np.random.seed(seed)

    dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    categories = {
        "Electronics": (150, 800),
        "Home & Kitchen": (30, 200),
        "Apparel": (20, 120),
        "Books": (10, 45),
        "Sports": (25, 250),
    }
    regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
    segments = ["Consumer", "Corporate", "Small Business"]

    cat_choices = np.random.choice(list(categories.keys()), size=n_rows, p=[0.25, 0.22, 0.23, 0.15, 0.15])
    prices = [round(np.random.uniform(*categories[c]), 2) for c in cat_choices]

    df = pd.DataFrame({
        "order_id": [f"ORD-{10000 + i}" for i in range(n_rows)],
        "order_date": np.random.choice(dates, size=n_rows),
        "category": cat_choices,
        "region": np.random.choice(regions, size=n_rows, p=[0.40, 0.30, 0.20, 0.10]),
        "customer_segment": np.random.choice(segments, size=n_rows, p=[0.60, 0.25, 0.15]),
        "unit_price": prices,
        "quantity": np.random.randint(1, 6, size=n_rows),
        "discount": np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20], size=n_rows, p=[0.50, 0.20, 0.15, 0.10, 0.05]),
    })

    # Inject realistic data issues: 15 missing prices and 10 duplicate rows
    missing_idx = np.random.choice(df.index, size=15, replace=False)
    df.loc[missing_idx, "unit_price"] = np.nan
    df = pd.concat([df, df.sample(10, random_state=seed)], ignore_index=True)

    df.to_csv("sales_data.csv", index=False)
    print(f"Generated sales_data.csv with {len(df)} rows.")

if __name__ == "__main__":
    create_dataset()