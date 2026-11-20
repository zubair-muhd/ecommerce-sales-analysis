import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
os.makedirs("output", exist_ok=True)


def load_and_clean(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    initial_rows = len(df)

    # 1. Remove duplicate orders
    df = df.drop_duplicates(subset=["order_id"])

    # 2. Fill missing unit prices with the median price of their category
    df["unit_price"] = df["unit_price"].fillna(
        df.groupby("category")["unit_price"].transform("median")
    )

    # 3. Parse dates and engineer revenue features
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["gross_revenue"] = df["unit_price"] * df["quantity"]
    df["net_revenue"] = df["gross_revenue"] * (1 - df["discount"])

    print(f"Cleaned data: {initial_rows} -> {len(df)} rows (removed {initial_rows - len(df)} duplicates).")
    df.to_csv("output/cleaned_sales_data.csv", index=False)
    return df


def print_kpis(df: pd.DataFrame) -> None:
    total_rev = df["net_revenue"].sum()
    total_orders = len(df)
    aov = total_rev / total_orders
    top_category = df.groupby("category")["net_revenue"].sum().idxmax()
    top_region = df.groupby("region")["net_revenue"].sum().idxmax()

    print("\n--- EXECUTIVE SUMMARY ---")
    print(f"Total Net Revenue:   ${total_rev:,.2f}")
    print(f"Total Orders:        {total_orders:,}")
    print(f"Average Order Value: ${aov:,.2f}")
    print(f"Top Category:        {top_category}")
    print(f"Top Region:          {top_region}")
    print("-------------------------\n")


def generate_charts(df: pd.DataFrame) -> None:
    # Chart 1: Monthly Revenue Trend
    monthly = df.groupby("month")["net_revenue"].sum().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly, x="month", y="net_revenue", marker="o", linewidth=2.5, color="#2563eb")
    plt.title("Monthly Net Revenue (2025)", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Net Revenue ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/monthly_revenue.png", dpi=150)
    plt.close()

    # Chart 2: Revenue by Category
    cat_rev = df.groupby("category")["net_revenue"].sum().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=cat_rev, x="net_revenue", y="category", hue="category", palette="viridis", legend=False)
    plt.title("Net Revenue by Product Category", fontsize=14, fontweight="bold")
    plt.xlabel("Net Revenue ($)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("output/category_revenue.png", dpi=150)
    plt.close()

    # Chart 3: Region vs. Customer Segment Heatmap
    pivot = df.pivot_table(values="net_revenue", index="region", columns="customer_segment", aggfunc="sum")
    plt.figure(figsize=(8, 5))
    sns.heatmap(pivot, annot=True, fmt=",.0f", cmap="Blues", linewidths=0.5)
    plt.title("Net Revenue ($) by Region & Segment", fontsize=14, fontweight="bold")
    plt.xlabel("Customer Segment")
    plt.ylabel("Region")
    plt.tight_layout()
    plt.savefig("output/region_segment_heatmap.png", dpi=150)
    plt.close()

    print("Saved 3 charts to the 'output/' directory.")


if __name__ == "__main__":
    data = load_and_clean("sales_data.csv")
    print_kpis(data)
    generate_charts(data)