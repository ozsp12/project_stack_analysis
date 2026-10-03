# Data metadata

<p align="justify">
The project data are divided into three layers. <code>raw/</code> contains the original Stack Exchange Data Explorer (SEDE) exports and is kept unchanged; <code>refined/</code> contains datasets prepared for direct analytical use; and <code>metadata/queries/</code> contains the SQL or query definitions associated with those exports. The primary source is the <a href="https://data.stackexchange.com/">Stack Exchange Data Explorer</a>, and the underlying public schema is documented in the <a href="https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede">SEDE/public data dump schema documentation</a>.
</p>

## `cumulative-answers-questions-stackexchange`

<p align="justify">
The legacy workbook <code>cumulative-answers-questions-stackexchange.xlsx</code> contains one worksheet, <code>QueryResults</code>, with 118 monthly observations from August 2016 through May 2026 and nine fields. The workbook is retained in <code>data/refined/</code> together with a CSV representation. Its corresponding reproducible SEDE query is stored at <code>data/metadata/queries/cumulative-answers-questions-stackexchange.sql</code>.
</p>

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
The Excel workbook contains one line chart using <code>Month Year</code> as its time axis and plotting <code>Cumulative Unanswered Questions</code> together with <code>Cumulative No Answers At All</code>. Stage 01 reproduces that chart with <code>Stage01DescriptiveAnalysis.cumulative_unanswered_figure()</code> and persists it as <code>assets/figures/stage_01_cumulative_unanswered.png</code>.
</p>
