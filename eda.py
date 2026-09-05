from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


project_root = Path(__file__).resolve().parent
org_data = project_root / "data" / "oasis_longitudinal.csv"
clean_data = project_root / "data" / "oasis_cleaned.csv"
result_plot_dir = project_root / "result_plot"

def load_and_clean_data(input_path: Path) -> pd.DataFrame:
    """Load the raw data and remove visits without an MMSE score."""
    data = pd.read_csv(input_path)
    return data.dropna(subset=["MMSE"]).copy()

def save_group_summary(data: pd.DataFrame):
    """Prints a summary of the dataset by diagnostic group."""
    subject_count = data["Subject ID"].nunique()
    group_counts = data["Group"].value_counts()
    group_statistics = data.groupby("Group")[["Age", "MR Delay"]].describe()

    print(f"Loaded {len(data):,} records for {subject_count:,} subjects.")
    print("\nRecords by group:")
    print(group_counts)

    print("\nAge and MRI delay by group:")
    print(group_statistics)

def save_figure(figure, file_path: Path):
    figure.savefig(file_path, bbox_inches="tight")
    plt.close(figure)

def create_age_plot(data: pd.DataFrame, plot_dir: Path):
    plot = sns.lmplot(data=data, x="Age", y="nWBV", hue="Group")
    plot.set_axis_labels("Age", "Normalized whole-brain volume")
    save_figure(plot.figure, plot_dir / "age_vs_brain_volume_by_group.png")

def create_converted_trend_plot(converted: pd.DataFrame, plot_dir: Path):
    plot = sns.lineplot(data=converted, x="MR Delay", y="nWBV", hue="Subject ID", legend=False)
    plot.set(title="Brain volume trend for converted subjects", xlabel="MRI delay (days)", ylabel="Normalized whole-brain volume")
    save_figure(plot.figure, plot_dir / "brain_volume_trend_converted_subjects.png")

def create_stage_distribution_plot(converted: pd.DataFrame, plot_dir: Path):
    plot = sns.displot(data=converted, x="nWBV", hue="stage", kde=True)
    plot.set_axis_labels("Normalized whole-brain volume","Count")
    save_figure(plot.figure, plot_dir / "brain_volume_distribution_by_stage.png")

def create_decline_comparison_plot(converted: pd.DataFrame, plot_dir: Path):
    stage_comparison = (converted.groupby(["Subject ID", "stage"])["nWBV"].mean().unstack())
    stage_comparison["difference"] = (stage_comparison["early"] - stage_comparison["later"])
    stage_comparison = (stage_comparison.sort_values("difference").reset_index())

    plot = sns.barplot(data=stage_comparison, x="difference", y="Subject ID")
    plot.set(title="Early-to-later brain volume difference", xlabel="Difference in normalized whole-brain volume", ylabel="Subject ID")
    save_figure(plot.figure, plot_dir / "decline_pace_difference_by_subject.png")

def create_stage_trend_plot(converted: pd.DataFrame, plot_dir: Path):
    stage_means = (converted.groupby(["Subject ID", "stage"])["nWBV"].mean().reset_index())
    plot = sns.lineplot(data=stage_means,x="nWBV", y="stage", units="Subject ID", estimator=None)
    plot.set(title="Average brain volume by progression stage", xlabel="Normalized whole-brain volume", ylabel="Stage")
    save_figure(plot.figure, plot_dir / "brain_volume_trend_by_stage.png")

def create_mmse_plot(data: pd.DataFrame, plot_dir: Path):
    plot = sns.boxplot(data=data, x="CDR", y="MMSE")
    plot.set(title="MMSE scores by clinical dementia rating", xlabel="Clinical dementia rating (CDR)", ylabel="MMSE")
    save_figure(plot.figure, plot_dir / "mmse_by_cdr_boxplot.png")

def create_plots(data: pd.DataFrame, plot_dir: Path):
    """Create and save all exploratory analysis plots."""
    plot_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    converted = data[data["Group"] == "Converted"].copy() 
    converted["stage"] = np.where(converted["CDR"] < 0.5, "early", "later")

    create_age_plot(data, plot_dir)
    create_converted_trend_plot(converted, plot_dir)
    create_stage_distribution_plot(converted, plot_dir)
    create_decline_comparison_plot(converted, plot_dir)
    create_stage_trend_plot(converted, plot_dir)
    create_mmse_plot(data, plot_dir)

def main() -> None:
    data = load_and_clean_data(org_data)
    clean_data.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(clean_data, index=False)

    save_group_summary(data)
    create_plots(data, result_plot_dir)
    print(f"\nCleaned data saved to {clean_data}")
    print(f"Plots saved to {result_plot_dir}")

if __name__ == "__main__":
    main()
