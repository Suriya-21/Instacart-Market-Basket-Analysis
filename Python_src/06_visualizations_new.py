import os
import pandas as pd
import matplotlib.pyplot as plt

from config import IMAGE_OUTPUT_DIR, CSV_OUTPUT_DIR

# ==========================================================
# Visualization Settings
# ==========================================================

FIGSIZE = (12, 7)
TITLE_SIZE = 16
LABEL_SIZE = 12
TICK_SIZE = 10

# ==========================================================
# Helper Functions
# ==========================================================

def load_csv(filename):
    """
    Load a CSV file from the output directory
    and remove the unwanted index column if present.
    """
    df = pd.read_csv(
        os.path.join(
            CSV_OUTPUT_DIR,
            filename
        )
    )

    return df.drop(
        columns=["Unnamed: 0"],
        errors="ignore"
    )


def get_top_n(data, column, n=20):
    """
    Return the top n rows sorted by a column.
    """
    return (
        data
        .sort_values(column, ascending=False)
        .head(n)
        .copy()
    )


def clean_itemset_labels(series):
    """
    Convert frozenset labels into readable text.
    """
    return (
        series.astype(str)
        .str.replace("frozenset", "", regex=False)
        .str.replace("{", "", regex=False)
        .str.replace("}", "", regex=False)
        .str.replace("'", "", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
    )


def save_plot(filename):
    """
    Save the current figure.
    """
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            IMAGE_OUTPUT_DIR,
            filename
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def setup_figure(title, xlabel, ylabel):
    """
    Apply common styling to all charts.
    """

    plt.figure(figsize=FIGSIZE)

    plt.title(
        title,
        fontsize=TITLE_SIZE,
        fontweight="bold"
    )

    plt.xlabel(
        xlabel,
        fontsize=LABEL_SIZE
    )

    plt.ylabel(
        ylabel,
        fontsize=LABEL_SIZE
    )

    plt.xticks(fontsize=TICK_SIZE)
    plt.yticks(fontsize=TICK_SIZE)

    plt.grid(
        axis="x",
        linestyle="--",
        alpha=0.4
    )


def plot_top_horizontal_bar(
    data,
    x_col,
    y_col,
    title,
    xlabel,
    ylabel,
    filename,
    decimal_places=2,
    offset=0.02
):
    """
    Generic function for Top-N horizontal bar charts.
    """

    setup_figure(
        title,
        xlabel,
        ylabel
    )

    plt.barh(
        data[y_col],
        data[x_col]
    )

    plt.gca().invert_yaxis()

    for index, value in enumerate(data[x_col]):
        plt.text(
            value + offset,
            index,
            f"{value:.{decimal_places}f}",
            va="center",
            fontsize=9
        )

    save_plot(filename)


# ==========================================================
# Market Basket Analysis
# ==========================================================

def top_frequent_itemsets():
    """
    Top 20 Frequent Itemsets by Support.
    """

    frequent_itemsets = load_csv(
        "frequent_itemsets.csv"
    )

    top20 = get_top_n(
        frequent_itemsets,
        "support"
    )

    top20["itemsets"] = clean_itemset_labels(
        top20["itemsets"]
    )

    plot_top_horizontal_bar(
        data=top20,
        x_col="support",
        y_col="itemsets",
        title="Top 20 Frequent Itemsets by Support",
        xlabel="Support",
        ylabel="Product Combination",
        filename="01_top_frequent_itemsets.png",
        decimal_places=3,
        offset=0.001
    )


def top_association_rules():
    """
    Top 20 Association Rules by Lift.
    """

    association_rules = load_csv(
        "association_rules.csv"
    )

    top20 = get_top_n(
        association_rules,
        "lift"
    )

    top20["rule"] = (
        clean_itemset_labels(
            top20["antecedents"]
        )
        + " → " +
        clean_itemset_labels(
            top20["consequents"]
        )
    )

    plot_top_horizontal_bar(
        data=top20,
        x_col="lift",
        y_col="rule",
        title="Top 20 Association Rules by Lift",
        xlabel="Lift",
        ylabel="Association Rule",
        filename="02_top_association_rules.png",
        decimal_places=2,
        offset=0.02
    )

# ==========================================================
# Lift Distribution
# ==========================================================

def lift_distribution():
    """
    Distribution of Lift values across association rules.
    """

    association_rules = load_csv(
        "association_rules.csv"
    )

    setup_figure(
        title="Distribution of Lift Values",
        xlabel="Lift",
        ylabel="Number of Rules"
    )

    plt.hist(
        association_rules["lift"],
        bins=20,
        edgecolor="black"
    )

    save_plot(
        "03_lift_distribution.png"
    )

# ==========================================================
# Confidence Distribution
# ==========================================================

def confidence_distribution():
    """
    Distribution of Confidence values across association rules.
    """

    association_rules = load_csv(
        "association_rules.csv"
    )

    setup_figure(
        title="Distribution of Confidence Values",
        xlabel="Confidence",
        ylabel="Number of Rules"
    )

    plt.hist(
        association_rules["confidence"],
        bins=20,
        edgecolor="black"
    )

    save_plot(
        "04_confidence_distribution.png"
    )

# ==========================================================
# Top Products by Product Affinity Index
# ==========================================================

def top_product_affinity_index():
    """
    Top 20 Products ranked by Product Affinity Index.
    """

    affinity = load_csv(
        "product_affinity_index.csv"
    )

    top20 = get_top_n(
        affinity,
        "Product_Affinity_Index"
    )

    plot_top_horizontal_bar(
        data=top20,
        x_col="Product_Affinity_Index",
        y_col="Product",
        title="Top 20 Products by Product Affinity Index",
        xlabel="Product Affinity Index",
        ylabel="Product",
        filename="05_top_product_affinity_index.png",
        decimal_places=2,
        offset=0.05
    )

# ==========================================================
# Top Products by Total Associations
# ==========================================================

def top_total_associations():
    """
    Top 20 Products by Total Associations.
    """

    affinity = load_csv(
        "product_affinity_index.csv"
    )

    top20 = get_top_n(
        affinity,
        "Total_Associations"
    )

    plot_top_horizontal_bar(
        data=top20,
        x_col="Total_Associations",
        y_col="Product",
        title="Top 20 Products by Total Associations",
        xlabel="Total Associations",
        ylabel="Product",
        filename="06_top_total_associations.png",
        decimal_places=0,
        offset=1
    )

# ==========================================================
# Product Business Role Distribution
# ==========================================================

def business_role_distribution():
    """
    Distribution of products across Business Roles.
    """

    affinity = load_csv(
        "product_affinity_index.csv"
    )

    role_counts = (
        affinity["Business_Role"]
        .value_counts()
        .reset_index()
    )

    role_counts.columns = [
        "Business_Role",
        "Count"
    ]

    plot_top_horizontal_bar(
        data=role_counts,
        x_col="Count",
        y_col="Business_Role",
        title="Product Distribution by Business Role",
        xlabel="Number of Products",
        ylabel="Business Role",
        filename="07_business_role_distribution.png",
        decimal_places=0,
        offset=0.5
    )

# ==========================================================
# Top Cross-Sell Recommendations
# ==========================================================

def top_cross_sell_recommendations():
    """
    Top 20 Cross-Sell Recommendations by Recommendation Strength.
    """

    recommendations = load_csv(
        "cross_sell_recommendations.csv"
    )

    top20 = get_top_n(
        recommendations,
        "Lift"
    )


    top20["Recommendation"] = (
            top20["Purchased_Product"].fillna("").astype(str)
            + " → "
            + top20["Recommended_Product"].fillna("").astype(str)
            + top20["Recommendation_Strength"].astype(str)
            + ")"
    )

    plot_top_horizontal_bar(
        data=top20,
        x_col="Lift",
        y_col="Recommendation",
        title="Top 20 Cross-Sell Recommendations",
        xlabel="Lift",
        ylabel="Recommendation",
        filename="08_top_cross_sell_recommendations.png",
        decimal_places=2,
        offset=0.05
    )

# ==========================================================
# Top Product Bundles by Bundle Quality
# ==========================================================

def top_bundle_recommendations():
    """
    Top 20 Product Bundles ranked by Bundle Quality.
    """

    bundles = load_csv(
        "bundle_recommendations.csv"
    )

    top20 = get_top_n(
        bundles,
        "Lift"
    )


    top20["Bundle"] = (
            top20["Bundle_Product_1"].fillna("").astype(str)
            + " + "
            + top20["Bundle_Product_2"].fillna("").astype(str)
    )

    plot_top_horizontal_bar(
        data=top20,
        x_col="Lift",
        y_col="Bundle",
        title="Top 20 Product Bundles by Bundle Quality",
        xlabel="Lift",
        ylabel="Bundle",
        filename="09_top_bundle_recommendations.png",
        decimal_places=2,
        offset=0.05
    )

# ==========================================================
# Top Store Layout Recommendations
# ==========================================================

def top_store_layout_recommendations():
    """
    Top 20 Store Layout Recommendations.
    """

    layout = load_csv(
        "store_layout_recommendations.csv"
    )

    top20 = get_top_n(
        layout,
        "Lift"
    )


    top20["Placement"] = (
            top20["Primary_Product"].fillna("").astype(str)
            + " ↔ "
            + top20["Nearby_Product"].fillna("").astype(str)
    )

    plot_top_horizontal_bar(
        data=top20,
        x_col="Lift",
        y_col="Placement",
        title="Top 20 Store Layout Recommendations",
        xlabel="Lift",
        ylabel="Product Placement",
        filename="10_store_layout_recommendations.png",
        decimal_places=2,
        offset=0.05
    )

# ==========================================================
# Top Product Pairs by Affinity Score
# ==========================================================

def top_product_pair_affinity():
    """
    Top 20 Product Pairs ranked by Product Pair Affinity Score.
    """

    pair_affinity = load_csv(
        "product_pair_affinity_scores.csv"
    )

    top20 = get_top_n(
        pair_affinity,
        "Product_Pair_Affinity_Score"
    )

    top20["Product Pair"] = (
        top20["Product_1"]
        + " ↔ "
        + top20["Product_2"]
    )

    plot_top_horizontal_bar(
        data=top20,
        x_col="Product_Pair_Affinity_Score",
        y_col="Product Pair",
        title="Top 20 Product Pairs by Affinity Score",
        xlabel="Product Pair Affinity Score",
        ylabel="Product Pair",
        filename="11_top_product_pair_affinity.png",
        decimal_places=2,
        offset=0.05
    )

# ==========================================================
# Lift vs Confidence Scatter Plot
# ==========================================================

def lift_vs_confidence():
    """
    Scatter plot showing the relationship between
    Confidence and Lift for all association rules.
    """

    association_rules = load_csv(
        "association_rules.csv"
    )

    setup_figure(
        title="Lift vs Confidence",
        xlabel="Confidence",
        ylabel="Lift"
    )

    plt.scatter(
        association_rules["confidence"],
        association_rules["lift"],
        alpha=0.6,
        s=40
    )

    plt.grid(
        linestyle="--",
        alpha=0.4
    )

    save_plot(
        "12_lift_vs_confidence.png"
    )
# ==========================================================
# Main Function
# ==========================================================

def main():

    print("=" * 60)
    print("Generating Visualizations...")
    print("=" * 60)

    visualizations = [
        ("Top Frequent Itemsets", top_frequent_itemsets),
        ("Top Association Rules", top_association_rules),
        ("Lift Distribution", lift_distribution),
        ("Confidence Distribution", confidence_distribution),
        ("Top Product Affinity Index", top_product_affinity_index),
        ("Top Total Associations", top_total_associations),
        ("Business Role Distribution", business_role_distribution),
        ("Top Cross-Sell Recommendations", top_cross_sell_recommendations),
        ("Top Bundle Recommendations", top_bundle_recommendations),
        ("Store Layout Recommendations", top_store_layout_recommendations),
        ("Top Product Pair Affinity", top_product_pair_affinity),
        ("Lift vs Confidence", lift_vs_confidence)
    ]

    for title, func in visualizations:
        try:
            func()
            print(f"✓ {title}")
        except Exception as e:
            print(f"✗ {title}: {e}")


    print("=" * 60)
    print("All visualizations generated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()