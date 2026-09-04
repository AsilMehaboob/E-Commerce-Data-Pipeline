# E-Commerce Data Engineering Platform

An end-to-end e-commerce data engineering pipeline built with Databricks, PySpark, and Delta Lake using the Brazilian E-Commerce Public Dataset by Olist.

## Architecture

Raw CSV → Bronze → Silver → Gold → Databricks SQL → AI/BI Dashboard

## Pipeline

- **Bronze:** Ingest raw CSV data into Delta tables.
- **Silver:** Clean, standardize, validate, and enrich the data.
- **Gold:** Create business-ready datasets and metrics.
- **Data Quality:** Automated checks for nulls, duplicates, schema, validity, and referential integrity.
- **Incremental Processing:** Demonstrated Delta Lake `MERGE` for upserts.
- **Orchestration:** Databricks Job runs the Bronze → Silver → DQ → Gold pipeline.
- **Analytics:** AI/BI dashboard for sales, products, and delivery performance.

## Dashboard

The dashboard includes:

- Total Revenue
- Total Orders
- Items Sold
- Average Order Value
- Monthly Revenue Trend
- Top Product Categories
- Top Products
- Delivery Performance

## Project Structure

```text
E-Commerce-Data-Pipeline/
├── 01_data_exploration
├── 02_bronze_ingestion
├── 03_silver_transformation
├── 04_silver_data_quality
├── 05_gold_transformation
├── 06_data_quality_pipeline
├── 07_incremental_processing
└── README.md
```

## Dataset

Brazilian E-Commerce Public Dataset by Olist

Approx. 100K orders from 2016–2018.
