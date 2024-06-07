-- Need to manually run each query now.

CREATE SCHEMA IF NOT EXISTS hive.delta
WITH (location = 's3a://warehouse/');

-- Path s3a://iris/iris_data is the holding directory. We dont give full file path. Only parent directory
CREATE TABLE IF NOT EXISTS hive.delta.manga (
  symbol            VARCHAR,
  last_price        VARCHAR,
  timestamp         VARCHAR,
  volume            VARCHAR,
  trade_conditions  VARCHAR
)
WITH (
  external_location = 's3a://warehouse/test',
  format = 'PARQUET'
);

-- Testing
SELECT 
  *
FROM hive.delta.manga
LIMIT 10;

SHOW TABLES IN hive.delta;