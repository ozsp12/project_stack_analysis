from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd


class Stage01DescriptiveAnalysis:
    """Stage 01: basic descriptive inspection of the project datasets."""

    REFINED_DATASET = "cumulative-answers-questions-stackexchange.csv"

    EXACT_DESCRIPTIONS = {
        "MonthStart": "First calendar day of the reference month.",
        "Month Year": "Reference month used as the time axis in the original Excel chart.",
        "Cumulative Unanswered Questions": (
            "Running number of questions that have neither an accepted answer nor a "
            "currently positive-scored answer."
        ),
        "Cumulative No Answers At All": (
            "Running number of questions that have never received any answer."
        ),
        "New Questions": "Questions created during the reference month.",
        "Newly Answered Questions": (
            "Questions that leave the unanswered state during the reference month."
        ),
        "NewlyGotFirstAnswer": (
            "Questions receiving their first answer during the reference month."
        ),
        "NetChangeInUnanswered": (
            "Monthly change in the unanswered-question stock: new questions minus "
            "newly answered questions."
        ),
        "NetChangeInNoAnswersAtAll": (
            "Monthly change in the no-answer stock: new questions minus questions "
            "receiving a first answer."
        ),
    }

    def __init__(
        self,
        data_dir: str | Path | None = None,
        assets_dir: str | Path | None = None,
    ) -> None:
        root = Path(__file__).resolve().parents[2]
        self.data_dir = Path(data_dir) if data_dir else root / "data"
        self.raw_dir = self.data_dir / "raw"
        self.refined_dir = self.data_dir / "refined"
        self.assets_dir = Path(assets_dir) if assets_dir else root / "assets"
        self.figures_dir = self.assets_dir / "figures"
        self.tables_dir = self.assets_dir / "tables"
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        self.tables_dir.mkdir(parents=True, exist_ok=True)

    def _save_table(self, dataframe: pd.DataFrame, filename: str) -> pd.DataFrame:
        path = self.tables_dir / filename
        dataframe.to_csv(path, index=False)
        return dataframe

    def _save_figure(self, figure: Any, filename: str) -> Any:
        path = self.figures_dir / filename
        figure.savefig(path, dpi=180, bbox_inches="tight")
        return figure

    def _dataset_names(self, layer: str) -> list[str]:
        directory = self.raw_dir if layer == "raw" else self.refined_dir
        return [path.name for path in sorted(directory.glob("*.csv"))]

    def _resolve(self, dataset: str | Path) -> Path:
        path = Path(dataset)
        if path.exists():
            return path
        for directory in (self.raw_dir, self.refined_dir):
            candidate = directory / path
            if candidate.exists():
                return candidate
        raise FileNotFoundError(f"Dataset not found: {dataset}")

    def _load(self, dataset: str | Path) -> pd.DataFrame:
        path = self._resolve(dataset)
        if path.suffix.lower() == ".xlsx":
            return pd.read_excel(path)
        try:
            return pd.read_csv(path, low_memory=False)
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="latin-1", low_memory=False)

    @staticmethod
    def _date_candidates(dataframe: pd.DataFrame) -> dict[str, pd.Series]:
        parsed_columns: dict[str, pd.Series] = {}
        date_tokens = ("date", "day", "month", "year", "time")
        for column in dataframe.columns:
            name = str(column)
            if any(token in name.lower() for token in date_tokens):
                parsed = pd.to_datetime(dataframe[column], errors="coerce")
                if len(parsed) and parsed.notna().mean() >= 0.60:
                    parsed_columns[name] = parsed
        return parsed_columns

    def _explain_column(self, column: str) -> str:
        if column in self.EXACT_DESCRIPTIONS:
            return self.EXACT_DESCRIPTIONS[column]

        name = column.lower()
        rules = (
            ("tag", "Tag or tag-related attribute from Stack Exchange."),
            ("vote", "Vote count or vote-related attribute."),
            ("score", "Stack Exchange score or score-derived metric."),
            ("answer", "Answer count, answer status, or answer-related metric."),
            ("question", "Question count, question status, or question-related metric."),
            ("user", "User identifier, count, cohort, or user-related metric."),
            ("site", "Stack Exchange site or site-level identifier."),
            ("database", "SEDE database or database-level identifier."),
            ("count", "Number of records satisfying the corresponding condition."),
            ("total", "Aggregate total for the corresponding measure."),
            ("cumulative", "Running cumulative value over the ordered time dimension."),
            ("netchange", "Net change over the reference period."),
            ("month", "Monthly time field or month-level aggregation."),
            ("year", "Calendar year or year-level aggregation."),
            ("day", "Daily time field or day-level aggregation."),
            ("date", "Date or datetime field."),
            ("id", "Identifier used by the underlying Stack Exchange data model."),
        )
        for token, description in rules:
            if token in name:
                return description
        return (
            "Dataset-specific field; inspect the paired query in "
            "data/metadata/queries."
        )

    def _overview(self, dataset: str | Path) -> pd.DataFrame:
        path = self._resolve(dataset)
        dataframe = self._load(path)
        dates = self._date_candidates(dataframe)
        date_column = next(iter(dates), None)
        date_min = dates[date_column].min() if date_column else pd.NaT
        date_max = dates[date_column].max() if date_column else pd.NaT

        return pd.DataFrame(
            [
                {
                    "dataset": path.name,
                    "rows": len(dataframe),
                    "columns": dataframe.shape[1],
                    "missing_cells": int(dataframe.isna().sum().sum()),
                    "duplicated_rows": int(dataframe.duplicated().sum()),
                    "memory_mb": round(
                        dataframe.memory_usage(deep=True).sum() / 1024**2, 3
                    ),
                    "date_column": date_column,
                    "date_min": date_min,
                    "date_max": date_max,
                }
            ]
        )

    def _columns(self, dataset: str | Path) -> pd.DataFrame:
        dataframe = self._load(dataset)
        rows: list[dict[str, Any]] = []
        for column in dataframe.columns:
            series = dataframe[column]
            rows.append(
                {
                    "column": column,
                    "dtype": str(series.dtype),
                    "non_null": int(series.notna().sum()),
                    "missing": int(series.isna().sum()),
                    "unique": int(series.nunique(dropna=True)),
                    "description": self._explain_column(str(column)),
                }
            )
        return pd.DataFrame(rows)

    def dataset_inventory(self) -> pd.DataFrame:
        """List every analytical dataset and save the inventory asset."""
        rows: list[dict[str, Any]] = []
        for layer, directory in (("raw", self.raw_dir), ("refined", self.refined_dir)):
            for pattern in ("*.csv", "*.xlsx"):
                for path in sorted(directory.glob(pattern)):
                    rows.append(
                        {
                            "dataset": path.name,
                            "layer": layer,
                            "format": path.suffix.lower().lstrip("."),
                            "size_mb": round(path.stat().st_size / 1024**2, 3),
                        }
                    )
        dataframe = pd.DataFrame(rows)
        return self._save_table(dataframe, "stage_01_dataset_inventory.csv")

    def raw_overview(self) -> pd.DataFrame:
        """Summarize the structure and quality of every raw dataframe."""
        names = self._dataset_names("raw")
        dataframe = (
            pd.concat([self._overview(name) for name in names], ignore_index=True)
            if names
            else pd.DataFrame()
        )
        return self._save_table(dataframe, "stage_01_raw_overview.csv")

    def raw_columns(self) -> pd.DataFrame:
        """Catalog every column from every raw dataframe."""
        frames: list[pd.DataFrame] = []
        for name in self._dataset_names("raw"):
            frame = self._columns(name).copy()
            frame.insert(0, "dataset", name)
            frames.append(frame)
        dataframe = (
            pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
        )
        return self._save_table(dataframe, "stage_01_raw_columns.csv")

    def refined_overview(self) -> pd.DataFrame:
        """Inspect the refined cumulative answers/questions dataset."""
        dataframe = self._overview(self.REFINED_DATASET)
        return self._save_table(dataframe, "stage_01_refined_overview.csv")

    def refined_columns(self) -> pd.DataFrame:
        """Describe the nine fields in the refined cumulative dataset."""
        dataframe = self._columns(self.REFINED_DATASET)
        return self._save_table(dataframe, "stage_01_refined_columns.csv")

    def refined_numeric_summary(self) -> pd.DataFrame:
        """Compute standard descriptive statistics for refined numeric fields."""
        dataframe = self._load(self.REFINED_DATASET)
        numeric = dataframe.select_dtypes(include="number")
        if numeric.empty:
            summary = pd.DataFrame()
        else:
            summary = numeric.describe().T.reset_index().rename(
                columns={"index": "column"}
            )
        return self._save_table(
            summary,
            "stage_01_refined_numeric_summary.csv",
        )

    def cumulative_unanswered_figure(self) -> Any:
        """Reproduce and persist the cumulative unanswered-question figure."""
        dataframe = self._load(self.REFINED_DATASET).copy()
        dataframe["Month Year"] = pd.to_datetime(
            dataframe["Month Year"], errors="coerce"
        )

        figure, axis = plt.subplots(figsize=(11, 5))
        axis.plot(
            dataframe["Month Year"],
            dataframe["Cumulative Unanswered Questions"],
            label="Cumulative Unanswered Questions",
        )
        axis.plot(
            dataframe["Month Year"],
            dataframe["Cumulative No Answers At All"],
            label="Cumulative No Answers At All",
        )
        axis.set(
            title="Cumulative unanswered questions",
            xlabel="Month",
            ylabel="Questions",
        )
        axis.legend()
        axis.grid(alpha=0.2)
        figure.tight_layout()
        return self._save_figure(
            figure,
            "stage_01_cumulative_unanswered.png",
        )
