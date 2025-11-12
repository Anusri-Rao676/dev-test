import json
import boto3
from botocore.exceptions import ClientError
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = "Emp_Master"
table = dynamodb.Table(table_name)

logger.info("Lambda triggered")

def lambda_handler(event, context):
    try:
        logger.info(f"Received event: {json.dumps(event)}")

        http_method = (
            event.get("httpMethod")
            or event.get("requestContext", {}).get("http", {}).get("method", "")
        ).upper()

        if http_method == "POST":
            return handle_post(event)
        elif http_method == "GET":
            return handle_get(event)
        else:
            return response(405, {"error": "Method Not Allowed"})

    except Exception as e:
        logger.exception("Unhandled exception in lambda_handler")
        return response(500, {"error": str(e)})


def handle_post(event):
    try:
        payload = json.loads(event.get("body", "{}"))
        if "Emp_Id" not in payload:
            return response(400, {"message": "Missing Emp_Id in request body"})

        logger.info(f"Inserting item: {payload}")
        table.put_item(Item=payload)
        return response(201, {"message": "Item inserted successfully", "item": payload})

    except json.JSONDecodeError:
        return response(400, {"message": "Invalid JSON in request body"})
    except ClientError as e:
        logger.exception("DynamoDB client error in handle_post")
        return response(500, {"error": str(e)})


def handle_get(event):
    params = event.get("queryStringParameters") or {}
    Emp_id = params.get("Emp_Id")

    if not Emp_id:
        return response(400, {"error": "Missing Emp_Id in query parameters"})

    try:
        logger.info(f"Fetching item with Emp_Id: {Emp_id}")
        result = table.get_item(Key={"Emp_Id": Emp_id})

        if "Item" in result:
            logger.info(f"Item found: {result['Item']}")
            return response(200, result["Item"])
        else:
            return response(404, {"error": "Item not found"})

    except ClientError as e:
        logger.exception("DynamoDB client error in handle_get")
        return response(500, {"error": str(e)})


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
