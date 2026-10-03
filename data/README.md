# Data

<p align="justify">
The <code>data/</code> directory contains the source datasets, reproducibility metadata, and the intermediate and validated data layers used by the project. The primary public source is the <a href="https://data.stackexchange.com/">Stack Exchange Data Explorer (SEDE)</a>. Original query outputs are kept in <code>raw/</code>; deterministic transformations may be written to <code>refined/</code>; datasets that have passed explicit provenance, schema, grain, coverage, and quality checks may be promoted to <code>trusted/</code>; and the SQL definitions and machine-readable data catalog are stored in <code>metadata/</code>. Raw files should remain unchanged after extraction so that every downstream result can be traced to its source.
</p>

## Directory structure

```text
data/
├── raw/                   # Original CSV exports from SEDE
├── refined/               # Deterministically transformed datasets
├── trusted/               # Validated canonical analytical datasets
├── metadata/
│   ├── datasets.csv       # Column-level data catalog
│   └── queries/           # SQL/query definitions used to generate raw CSVs
└── README.md
```

## Raw datasets

<p align="justify">
The <code>raw/</code> directory is the source layer of the project. Each CSV is paired with the SQL or query definition stored in <code>metadata/queries/</code>. The table below provides the direct repository link to each raw dataset and the corresponding query file used to produce it. Detailed column names, logical data types, column descriptions, table descriptions, query filenames, and CSV URLs are maintained in <a href="metadata/datasets.csv"><code>metadata/datasets.csv</code></a>.
</p>

| Raw CSV | Description | SEDE SQL / query |
|---|---|---|
| [`History-Sum-By-Month-Per-Year-of-Votes-by-Tag.csv`](raw/History-Sum-By-Month-Per-Year-of-Votes-by-Tag.csv) | Monthly vote metrics by tag. | [`History-Sum-By-Month-Per-Year-of-Votes-by-Tag.txt`](metadata/queries/History-Sum-By-Month-Per-Year-of-Votes-by-Tag.txt) |
| [`all-db-names-from-db-system.csv`](raw/all-db-names-from-db-system.csv) | Stack Overflow and Stack Exchange database names exposed by SEDE. | [`all-db-names-from-db-system.txt`](metadata/queries/all-db-names-from-db-system.txt) |
| [`cumulative-answers-questions-stackexchange.csv`](raw/cumulative-answers-questions-stackexchange.csv) | Monthly question-lifecycle series matching the legacy workbook schema. | [`cumulative-answers-questions-stackexchange.sql`](metadata/queries/cumulative-answers-questions-stackexchange.sql) |
| [`cumulative-unanswered-questions-per-month-since-2008.csv`](raw/cumulative-unanswered-questions-per-month-since-2008.csv) | Monthly unanswered/no-answer question stocks and flows. | [`cumulative-unanswered-questions-per-month.txt`](metadata/queries/cumulative-unanswered-questions-per-month.txt) |
| [`new-answers-per-day-since-2008.csv`](raw/new-answers-per-day-since-2008.csv) | Daily new-answer counts split by deletion status. | [`new-answers-per-day-since-2008.txt`](metadata/queries/new-answers-per-day-since-2008.txt) |
| [`new-answers-per-month-since-2008.csv`](raw/new-answers-per-month-since-2008.csv) | Monthly new-answer counts split by deletion status. | [`new-answers-per-month-since-2008.txt`](metadata/queries/new-answers-per-month-since-2008.txt) |
| [`new-question-activity-per-day-since-2008.csv`](raw/new-question-activity-per-day-since-2008.csv) | Daily new-question counts. | [`new-question-activity-per-day-since-2008.txt`](metadata/queries/new-question-activity-per-day-since-2008.txt) |
| [`new-question-activity-per-month-since-2008.csv`](raw/new-question-activity-per-month-since-2008.csv) | Monthly new-question counts. | [`new-question-activity-per-month-since-2008.txt`](metadata/queries/new-question-activity-per-month-since-2008.txt) |
| [`new-questions-per-day-by-sites-since-2008.csv`](raw/new-questions-per-day-by-sites-since-2008.csv) | Daily new-question counts across selected Stack Exchange communities and Stack Overflow. | [`new-questions-per-day-by-sites-since-2008.txt`](metadata/queries/new-questions-per-day-by-sites-since-2008.txt) |
| [`tags-db.csv`](raw/tags-db.csv) | Snapshot of the SEDE <code>Tags</code> table. | [`tags-db.txt`](metadata/queries/tags-db.txt) |
| [`user-metrics-by-site-by-month-all-time.csv`](raw/user-metrics-by-site-by-month-all-time.csv) | User metrics by site and account-creation month. | [`user-metrics-by-site-by-month-all-time.txt`](metadata/queries/user-metrics-by-site-by-month-all-time.txt) |
| [`user-static-metrics-by-several-site-all-time.csv`](raw/user-static-metrics-by-several-site-all-time.csv) | Cross-site snapshot of aggregate user metrics. | [`user-static-metrics-by-several-site-all-time.txt`](metadata/queries/user-static-metrics-by-several-site-all-time.txt) |

## Refined data

<p align="justify">
The <code>refined/</code> layer is reserved for datasets produced by explicit, deterministic transformations of raw data, such as type normalization, reshaping, joins, derived variables, aggregation, or reproducible cleaning. A refined dataset must remain traceable to its raw inputs and transformation code. The layer is currently empty; the former cumulative CSV was moved to <code>raw/</code> because it is itself a direct SEDE query result rather than a Python-generated transformation.
</p>

## Trusted data

<p align="justify">
The <code>trusted/</code> layer is reserved for datasets that have passed documented checks of provenance, schema, grain, temporal coverage, missingness, duplicates, and semantic consistency. These datasets are intended to become stable analytical inputs for later stages of the project. The layer is currently empty and promotion into it should be deliberate and reproducible.
</p>

## Metadata

<p align="justify">
The <code>metadata/</code> directory contains the information required to reproduce and interpret the data. The <code>queries/</code> subdirectory stores the SQL or query text associated with each raw CSV. The machine-readable catalog <a href="metadata/datasets.csv"><code>datasets.csv</code></a> contains one row per dataset column and records the table name, column name, logical column type, column description, query filename, table description, and direct GitHub URL of the CSV. Dataset-specific caveats, including snapshot semantics, current-score dependence, query limits, or incomplete historical coverage, should be documented here rather than hidden inside analysis notebooks.
</p>

## Legacy analysis workbook

<p align="justify">
The Excel workbook formerly stored beside the cumulative CSV is an analysis artifact rather than a source dataset. It is preserved at <a href="../assets/analysis/cumulative-answers-questions-stackexchange.xlsx"><code>assets/analysis/cumulative-answers-questions-stackexchange.xlsx</code></a>. Its tabular content is represented separately by the raw CSV generated from the documented SEDE query.
</p>
