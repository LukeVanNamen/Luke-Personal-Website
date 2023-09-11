import json
import boto3
import os

# Initialize dynamodb boto3 object
dynamodb = boto3.resource('dynamodb')
# Set dynamodb table name variable from env
ddbTableName = os.environ['databaseName']
table = dynamodb.Table(ddbTableName)

def lambda_handler(event, context):
    # Update item in table or add if doesn't exist
    ddbResponse = table.update_item(
        Key={
            'Visitors': 'visitorCount', 
        },
        UpdateExpression='SET visitorCount = visitorCount + :value',
        ExpressionAttributeValues={
            ':value': 1
        },
        ReturnValues="UPDATED_NEW"
    )

    # Format dynamodb response into variable
    responseBody = json.dumps({"Visitors": ddbResponse["Attributes"]["visitorCount"]}, default=str)

    # Create api response object
    apiResponse = {
        "isBase64Encoded": False,
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": responseBody
    }

    # Return api response object
    return apiResponse

#import json
#import boto3

# Initialize dynamodb boto3 object
#dynamodb = boto3.resource('dynamodb')
#table = dynamodb.Table('myCounterTable')

#def lambda_handler(event, context):
    # Update item in table or add if doesn't exist
#    response = table.get_item(
#        Key={
#            'Visitors': 'visitorCount', 
#        })
#    views = response["Attributes"]["visitorCount"]
#    views = views + 1
#    print(views)
#    reponse = table.put_item(Item={
#        'Visitors':'0',
#        'visitorCount':str(views)
#    })
#    return views
