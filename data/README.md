# Data

<p align="justify">
The <code>data/</code> directory contains the datasets, source definitions, and provenance material used by the project. Its organization separates source preservation from analytical preparation and from datasets that have been explicitly validated for downstream use. The primary public source is the <a href="https://data.stackexchange.com/">Stack Exchange Data Explorer (SEDE)</a>, which provides SQL access to public Stack Exchange data. The corresponding public schema is documented in the <a href="https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede">Stack Exchange database schema documentation</a>. Files should move between data layers only through reproducible transformations, while source files in <code>raw/</code> remain unchanged.
</p>

## Directory structure

```text
data/
├── raw/          # Original source exports, preserved without analytical modification
├── refined/      # Cleaned or prepared datasets produced from source data
├── trusted/      # Validated datasets approved as canonical analytical inputs
└── metadata/
    └── queries/  # SQL queries and source definitions associated with the datasets
```

## Raw data

<p align="justify">
The <code>raw/</code> layer preserves the original exports used by the project. These files should be treated as immutable evidence of the source extraction and should not be manually corrected, reformatted, filtered, or overwritten. Most files are CSV exports produced from SEDE queries and retain the schema and granularity returned by the original query. Any issue discovered in a raw dataset should be documented in metadata and corrected in a downstream layer rather than by editing the original file.
</p>

## Refined data

<p align="justify">
The <code>refined/</code> layer contains datasets that have been prepared for direct analytical use but have not necessarily been promoted to the project's canonical trusted layer. Typical operations at this stage include explicit type conversion, date normalization, column naming, reshaping, aggregation, extraction from legacy workbooks, and other deterministic transformations that make source data easier to inspect and analyze. Every refined dataset should remain traceable to its raw source or reproducible query and should avoid undocumented manual corrections.
</p>

<p align="justify">
The principal refined dataset currently stored here is <code>cumulative-answers-questions-stackexchange</code>, available as both the legacy Excel workbook and a CSV representation. The workbook contains one worksheet, <code>QueryResults</code>, with 118 monthly observations from August 2016 through May 2026 and nine variables. Its fields describe the monthly evolution of cumulative unanswered questions, questions with no answers at all, new questions, questions leaving the unanswered state, questions receiving their first answer, and the corresponding monthly net changes. The Excel workbook also contains the line chart reproduced by Stage 01 of the analysis. The SQL definition used to reconstruct this dataset is stored in <code>metadata/queries/cumulative-answers-questions-stackexchange.sql</code>.
</p>

## Trusted data

<p align="justify">
The <code>trusted/</code> layer is the final curated data layer. A dataset should be placed here only after its provenance, schema, grain, date coverage, missingness, duplicate behavior, variable semantics, and relevant consistency checks have been reviewed. Trusted datasets are intended to become the stable analytical inputs for later stages of the project, so scripts in <code>src/stage_02/</code> and subsequent stages should preferentially consume this layer when an equivalent validated dataset exists. Promotion from <code>refined/</code> to <code>trusted/</code> should therefore be deliberate and reproducible rather than automatic.
</p>

<p align="justify">
The trusted layer is initially empty. This is intentional: the current Stage 01 work is descriptive and diagnostic, and its purpose is partly to establish which datasets are sufficiently well understood to be promoted. Future promotion should be accompanied by explicit validation rules or documented checks so that the meaning of "trusted" remains operational rather than merely organizational.
</p>

## Metadata

<p align="justify">
The <code>metadata/</code> directory contains information required to interpret, reproduce, and audit the datasets. Its <code>queries/</code> subdirectory stores the SQL or query text associated with SEDE exports, including the query that reconstructs the cumulative answers/questions dataset. Metadata should capture where a dataset came from, what entity and time grain it represents, how its fields should be interpreted, and any known limitations such as survivorship effects, snapshot semantics, query truncation, incomplete historical coverage, or site-specific scope. Dataset-specific caveats belong here rather than being hidden inside notebooks.
</p>

## Refined cumulative dataset — variable definitions

| Column | Meaning |
|---|---|
| `MonthStart` | First calendar day of the reference month. |
| `Month Year` | Reference month used on the x-axis of the original Excel chart. |
| `Cumulative Unanswered Questions` | Running number of questions with neither an accepted answer nor a currently positive-scored answer. |
| `Cumulative No Answers At All` | Running number of questions that have never received an answer. |
| `New Questions` | Questions created in the reference month. |
| `Newly Answered Questions` | Questions leaving the unanswered state in the reference month. |
| `NewlyGotFirstAnswer` | Questions receiving their first answer in the reference month. |
| `NetChangeInUnanswered` | New questions minus questions leaving the unanswered state. |
| `NetChangeInNoAnswersAtAll` | New questions minus questions receiving their first answer. |

<p align="justify">
The original workbook chart uses <code>Month Year</code> as its time axis and plots <code>Cumulative Unanswered Questions</code> together with <code>Cumulative No Answers At All</code>. The same chart is reproduced by the Stage 01 analysis and persisted under <code>assets/figures/</code>.
</p>
