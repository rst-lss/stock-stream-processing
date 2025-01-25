# `spark-submit-stock-analyzer.sh`

The script uses the `spark-submit` command to launch the `stock-analyzer.py` application as spark driver with the following configurations:

- **Master URL**: The Spark master is specified as `spark://spark-master-service:7077`, which is the address of the Spark master service.
- **Deploy Mode**: The application runs in `client` mode, meaning the driver program runs on the machine where the script is executed.
- **Application Name**: The application is named "StockAnalyzer".
- **Packages**: The `spark-sql-kafka` package is included to enable Kafka integration for Spark SQL.
- **Resource Allocation**:
  - Driver memory is set to `1g`.
  - Executor memory is set to `1g`.
  - Executor cores are set to `1`.
  - Total executor cores are set to `1`.
  - Only `1` executor instance is created.
- **Network Configuration**:
  - The driver's bind address is set to `0.0.0.0` to allow connections from any IP.
  - The driver's host is set to `stock-analyzer-service`.
  - The driver's port is set to `7072`.
  - The block manager's port is set to `35635`.
- **Python Files**: Additional dependencies are included via `dependencies.zip`.
- **Application File**: The main application file is `/app/stock-analyzer.py`.