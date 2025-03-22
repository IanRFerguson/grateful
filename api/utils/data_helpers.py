import os

from klondike.gcp.bigquery import BigQueryConnector
from utils.logger import logger

##########


def get_all_gratitudes(bq: BigQueryConnector) -> list:
    logger.info("Getting all gratitudes...")

    DATASET, TABLE = os.environ["DESTINATION_SCHEMA"], os.environ["DESTINATION_TABLE"]

    sql = f"""
    SELECT
        Body,
        _load_timestamp
    FROM {DATASET}.{TABLE}
    WHERE `From` = '{os.environ['KANES_PHONE_NUMBER']}'
    ORDER BY _load_timestamp DESC
    """

    responses = bq.read_dataframe(sql=sql).to_dicts()

    clean_array = []
    for resp in responses:
        gratitudes = resp["Body"].split("\n")
        timestamp = (
            resp["_load_timestamp"].strftime("%D") if resp["_load_timestamp"] else None
        )

        for g in gratitudes:
            clean_array.append({"value": g.title().strip(), "sent_at": timestamp})

    logger.debug(f"Returning {len(clean_array)} gratitudes...")

    return clean_array
