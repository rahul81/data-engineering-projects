import logging
import sys

import apache_beam as beam
from apache_beam.io.kafka import ReadFromKafka
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import PipelineOptions


def run(
    bootstrap_servers,
    topic,
    with_metadata,
    bq_dataset,
    bq_table_name,
    project,
    pipeline_options,
):

    def convert_kafka_record_to_dictionary(record):
        # the records have 'value' attribute when --with_metadata is given
        if hasattr(record, "value"):
            data_bytes = record.value
        elif isinstance(record, tuple):
            data_bytes = record[1]
        else:
            raise RuntimeError("unknown record type: %s" % type(record))
        # Converting bytes record from Kafka to a dictionary.
        import ast

        data = ast.literal_eval(data_bytes.decode("UTF-8"))
        output = {
            key: data[key] for key in ["latitude", "longitude", "id"]
        }
        if hasattr(record, "timestamp"):
            # timestamp is read from Kafka metadata
            output["timestamp"] = record.timestamp
        return output

    with beam.Pipeline(options=pipeline_options) as pipeline:
        get_col = (
            pipeline
            | ReadFromKafka(
                consumer_config={"bootstrap.servers": bootstrap_servers},
                topics=[topic],
                with_metadata=with_metadata,
            )
            | beam.Map(lambda record: convert_kafka_record_to_dictionary(record))
        )

        if bq_dataset:
            schema = "latitude:STRING,longitude:STRING,id:INTEGER"
            if with_metadata:
                schema += ",timestamp:STRING"
            _ = get_col | beam.io.WriteToBigQuery(
                bq_table_name, bq_dataset, project, schema
            )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bootstrap_servers",
        dest="bootstrap_servers",
        required=True,
        help="Bootstrap servers for the Kafka cluster. Should be accessible by "
        "the runner",
    )
    parser.add_argument(
        "--topic",
        dest="topic",
        default="messages",
        help="Kafka topic to write to and read from",
    )
    parser.add_argument(
        "--with_metadata",
        default=False,
        action="store_true",
        help="If set, also reads metadata from the Kafka broker.",
    )
    parser.add_argument(
        "--bq_dataset",
        type=str,
        default="",
        help="BigQuery Dataset to write tables to. ",
    )
    parser.add_argument(
        "--bq_table_name",
        default="kafka_geo_data",
        help="The BigQuery table name. Should not already exist.",
    )
    
    known_args, pipeline_args = parser.parse_known_args()

    pipeline_options = PipelineOptions(
        pipeline_args, save_main_session=True, streaming=True
    )

    # We also require the --project option to access --bq_dataset
    project = pipeline_options.view_as(GoogleCloudOptions).project

    if project is None:
        parser.print_usage()
        print(sys.argv[0] + ": error: argument --project is required")
        sys.exit(1)

    run(
        known_args.bootstrap_servers,
        known_args.topic,
        known_args.with_metadata,
        known_args.bq_dataset,
        known_args.bq_table_name,
        project,
        pipeline_options,
    )
