CREATE DATABASE IF NOT EXISTS sentiment_db;

CREATE EXTERNAL TABLE IF NOT EXISTS sentiment_db.sentiment_results (
  post_id          STRING,
  event_name       STRING,
  text             STRING,
  clean_text       STRING,
  language         STRING,
  source           STRING,
  timestamp        STRING,
  sentiment_label  STRING,
  sentiment_score  DOUBLE,
  model_name       STRING,
  processing_time  STRING
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION 's3://sentiment-project-raw-aya-660838763568-eu-north-1-an/results/';