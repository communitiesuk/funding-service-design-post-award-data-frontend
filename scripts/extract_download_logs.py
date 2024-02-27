import csv
import datetime
import json
import time
from optparse import OptionParser
from typing import List

from boto3 import client

parser = OptionParser(
    usage="Output a report of downloads (required AWS authentication)"
)
parser.add_option(
    "-e",
    "--environment",
    dest="environment",
    default="test",
    help="Specify the environment (default: test)",
)
parser.add_option(
    "-d",
    "--days",
    dest="days",
    type=int,
    default=30,
    help="Specify the number of days (default: 30)",
)
parser.add_option(
    "-f",
    "--filename",
    dest="filename",
    default="output.csv",
    help="Specify the output filename",
)

(options, args) = parser.parse_args()

ENVIRONMENT = options.environment
DAYS = options.days

print("Starting script")

FIELD_NAMES = [
    "timestamp",
    "user_id",
    "funds",
    "file_format",
    "organisations",
    "regions",
    "outcome_categories",
    "rp_start",
    "rp_end",
]
OUTPUT_FILENAME = options.filename


def cloudwatch_logs_to_rows_dict(data: List[dict]) -> List[dict]:
    def parse_item(item: dict) -> dict:
        message = json.loads([i for i in item if i["field"] == "@message"][0]["value"])
        user_id = message["user_id"]
        query_params = message["query_params"]
        timestamp = [i for i in item if i["field"] == "@timestamp"][0]["value"]
        return {"timestamp": timestamp, "user_id": user_id, **query_params}

    return [parse_item(item) for item in data]


cloudwatch_logs_client = client("logs", region_name="eu-west-2")

now = datetime.datetime.now()
d = datetime.timedelta(days=DAYS)
start_time = now - d

query_id = cloudwatch_logs_client.start_query(
    logGroupName=f"/copilot/post-award-{ENVIRONMENT}-data-frontend",
    queryString="""fields @timestamp, @message
| sort @timestamp desc
| limit 1000
| filter request_type = 'download'""",
    startTime=int(datetime.datetime.timestamp(start_time)),
    endTime=int(datetime.datetime.timestamp(now)),
)["queryId"]

# Poll until query is complete
response = None

while response is None or response["status"] == "Running":
    print("Waiting for query to complete ...")
    time.sleep(1)
    response = cloudwatch_logs_client.get_query_results(queryId=query_id)

rows_dict = cloudwatch_logs_to_rows_dict(response["results"])

# Open the CSV file
with open(OUTPUT_FILENAME, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
    writer.writeheader()
    writer.writerows(rows_dict)

print(f"File written to {OUTPUT_FILENAME}")
