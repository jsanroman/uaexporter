# 📊 UaExporter

> ⚠️ Important Notice: Universal Analytics (UA) properties stopped processing new hits on 1 July 2023, and the **UA API is scheduled to stop working on 1 July 2024**. To preserve your metrics, it is crucial to export your data. For more detailed information, please visit the Google support page at https://support.google.com/analytics/answer/11583528?hl=en.

**UaExporter** helps you export your Universal Analytics data to your own datasources, including **CSV** and **Clickhouse**.


## Configuration
### 1. Environment Variables
Update the `.env` file with your specific configurations for **Clickhouse**/**CSV** connectors and Google Analytics settings.

### 2. Define Your Reports
Customize reports.yml to define the specifics of the data you want to export:

- **name**: The name of your report, which also serves as the csv file name or database table name.
- **connector**: Choose between **csv** and **clickhouse**.
- **start_date**: The starting date for the data export.
- **end_date**: The ending date for the data export.
- **metrics**: Specify the metrics from Universal Analytics, e.g., `ga:pageviews`.
- **dimensions**: Define the dimensions to include, e.g., `ga:pagePath,ga:date`.

Use the Google Analytics Query Explorer (https://ga-dev-tools.appspot.com/query-explorer/) to prototype and test your queries with customm metrics and dimensions.

## Usage
To execute UaExporter, simply run:
```
./uaexporter
```
