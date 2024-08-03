import os

from klondike.bigquery.bigquery import BigQueryConnector
from polars import DataFrame

##########


def handle_incoming_traffic(bq: BigQueryConnector, traffic: object) -> None:
    """
    Logs incoming message from Twilio SMS to Google BigQuery
    """

    # Reshape to standard dict object
    traffic_meta = {k: v for k, v in traffic.items()}

    # Reshape to Polars DataFrame object
    traffic_meta_df = DataFrame(data=traffic_meta)

    # Get destination table name from env
    destination_table_name = (
        f"{os.environ['DESTINATION_SCHEMA']}.{os.environ['DESTINATION_TABLE']}"
    )

    # Write Polars DF to BigQuery
    bq.write_dataframe(
        df=traffic_meta_df, table_name=destination_table_name, if_exists="append"
    )
