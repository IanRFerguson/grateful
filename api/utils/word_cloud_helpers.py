import itertools
import os

import wordcloud
from klondike import BigQueryConnector

##########


def generate_word_cloud(bq: BigQueryConnector, outpath: str, phrases: bool = False):
    sql = f"""
    SELECT
        Body
    FROM {os.environ['DESTINATION_SCHEMA']}.{os.environ['DESTINATION_TABLE']}
    WHERE `From` = '{os.environ['KANES_PHONE_NUMBER']}'
    """

    tbl = bq.read_dataframe(sql=sql)

    # Break body responses into individual arrays
    cloud_gratitudes = [x.split("\n") for x in tbl["Body"]]

    # Combine arrays into a long string
    word_bank = [
        x.title().strip() for x in list(itertools.chain.from_iterable(cloud_gratitudes))
    ]

    if phrases:
        word_bank = [x.replace(" ", "_") for x in word_bank]

    content = " ".join(word_bank)

    # Create word cloud and save it
    wc = wordcloud.WordCloud(background_color="white", width=800, height=500).generate(
        content
    )

    wc.to_file(outpath)
