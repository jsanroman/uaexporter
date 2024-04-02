# 📊 UaExporter
Export your Universal Analytics data to your own datasources (**CSV**, **Clickhouse**).

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
