from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import json


# Functions to parse raw data from columns
get_symbol = udf(lambda x: json.loads(x)['symbol'], StringType())
get_last_price = udf(lambda x: json.loads(x)['last_price'], StringType())
get_timestamp = udf(lambda x: json.loads(x)['timestamp'], StringType())
get_volume = udf(lambda x: json.loads(x)['volume'], StringType())
get_trade_conditions = udf(lambda x: json.loads(x)['trade_conditions'], StringType())
