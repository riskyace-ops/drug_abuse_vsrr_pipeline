# DRUG_ABUSE_PIPELINE_VSRR


Hi! Very sweet of you to check my profile out and investigate my freelance projects >:) As of this day I've finalized my automated data pipeline that ingests monthly CDC overdose mortality data, which performs SQL queries, exports dataset, and powers a Tableau Public dashboard. Due to expenditure & resource limitations, execution is fully automated via Windows Task Scheduler.

Data Source (CDC VSRR)
This pipeline uses drug overdose mortality data from the CDC’s Vital Statistics Rapid Release (VSRR) system. VSRR provides provisional 12-month ending overdose death estimates derived from recent death certificate data. These counts are updated monthly and differ from actual overdose mortality rates. I redacted the 2025 years data from the project because of the CDC's awcknowledgement on how limited & incomplete the data was for that annual year.

PIPELINE FLOW

1. Ingest raw monthly VSRR data
2. Transform and aggregate via SQL
3. Export a single output file
4. Tableau Public displays the final dataset


Automation: Execution is triggered on system startup by Windows Task Scheduler, which runs run_pipeline.bat. this file runs all the python/sql scripts seqentially from top-bottom below!

Dashboard Structure

- Latest YoY change, most recent annual total, cumulative deaths
- YoY Trend Analysis — percent change by drug category
- Annual Totals with YoY Overlay — absolute counts with growth context
- Geographic Distribution — state-level overdose impact
- Filters — year and drug category



Limitations
 - direct database connectivity with tablaue was not available. My workaround for this was producing a singular output file which connected to my free version of tablaue via my google drive. 
 - tableau refreshes by reconnecting to this file after each successful pipeline run.
 - the downloaded raw vsrr database doesn't include actual annualized data, just 12-month rolling period data. My workaround for this was assigning a numeric value from 1-12 to each month and only extracting the December values to produce a table for my analysis.
- execution happens locally, not on a server/cloud


My Future Improvements

- Cloud-based orchestration
- Tablaue Desktop integration so I can automate my pipeline more effectively




Automated batch ETL pipeline that ingests monthly overdose data, performs SQL queries, exports dataset, and powers a Tableau Public dashboard.
