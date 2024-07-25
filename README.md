# manga-stock-prices

This is a simple pipeline project to extract data from a realtime system (finnhub websocket API), ingest in a kafka topic to consume and aggregate in a pyspark streaming process, and ingest in an OTF table (delta lake) inside a blob storage (minio). After that, consume the data through a query engine (trino) and show some charts in a BI tool (superset).

To this project we'll be use stock price data from MANGA companies.

<img src="assets/manga_logo.png" >

## Pipeline

<img src="assets/pipeline.png" /> 

## Folder Structure

```markdown
├── README.md
├── assets           <- For resources like images and documents
├── docker           <- Docker images and volume configurations
|   └── config       <- Config files to mirror in volumes
|       ├── minio
│       └── trino              
├── source           <- Source code
|    ├── modules     <- Python modules with some pieces of code
│    └── scripts     <- General purpose scripts in python and sql   
```

---

## Launch the Project

```bash
sh build.sh
```

## Services

- `Minio` - available on [http://localhost:9001](http://localhost:9001)
- `Superset` - available on [http://localhost:8088/](http://localhost:8088/)
- `Kafka UI` - available on [http://localhost:8080/](http://localhost:8080/)
- `Trino UI` - available on [http://localhost:8080/](http://localhost:8080/)


### Connections

- trino URI on superset connection: `trino://trino@trino:8080/hive`