CREATE SCHEMA IF NOT EXISTS hive.delta
WITH (location = 's3a://warehouse/');

CREATE TABLE IF NOT EXISTS hive.delta.manga_prices (
  symbol            VARCHAR,
  last_price        VARCHAR,
  timestamp         VARCHAR,
  volume            VARCHAR,
  trade_conditions  VARCHAR
)
WITH (
  external_location = 's3a://warehouse/manga_prices',
  format = 'PARQUET'
);

-- Testing
SELECT 
  *
FROM hive.delta.manga_prices
LIMIT 10;

SHOW TABLES IN hive.delta;