import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from boto3.dynamodb.conditions import Key

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
dynamodb_table = dynamodb.Table('Medicaments')
items_check_path = '/items'

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='AKIA57LEVK6QRETBTEJY',
    aws_secret_access_key='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',
    region_name='us-east-1'  # Northern Virginia
)

items_check_path = '/items'
def handler(event, context):
    print('Request event: ', event)
    response = None
    try:
        http_method = event.get('httpMethod')
        path = event.get('path')

        if http_method == 'GET' :
            response = get_medications()
        elif http_method == 'POST' :
            response = save(json.loads(event['body'])) 
        elif http_method == 'PATCH' :
            body = json.loads(event['body'])
            response = modify_medication(body['Med'],body['SortKey'],body['updateKey'], body['updateValue']) 
        elif http_method == 'DELETE' :
            body = json.loads(event['body'])
            response = delete_medication(body['Med'],body['SortKey'])      
        else:
            response = build_response(404, '404 Not Found')    
    except Exception as e:
        print('Error:', e)
        response = build_response(400, 'Error processing request')
   
    return response
def get_medications():
    try:
        scan_params = {
            'TableName': 'Medicaments'
        }
        return build_response(200, scan_dynamo_records(scan_params, []))
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])

def modify_medication(Med,Q, update_key, update_value):
    try:
        response = dynamodb_table.update_item(
            Key={'Med': Med,'SortKey':Q},
            UpdateExpression=f'SET {update_key} = :value',
            ExpressionAttributeValues={':value': update_value},
            ReturnValues='UPDATED_NEW'
        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttributes': response
        }
        return build_response(200, body)
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])


def scan_dynamo_records(scan_params, item_array):
    response = dynamodb_table.scan(**scan_params)
    item_array.extend(response.get('Items', []))
   
    if 'LastEvaluatedKey' in response:
        scan_params['ExclusiveStartKey'] = response['LastEvaluatedKey']
        return scan_dynamo_records(scan_params, item_array)
    else:
        return {'Medications': item_array}        
 
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Check if it's an int or a float
            if obj % 1 == 0:
                return int(obj)
            else:
                return float(obj)
        # Let the base class default method raise the TypeError
        return super(DecimalEncoder, self).default(obj) 
def save(request_body):
    try:
        dynamodb_table.put_item(Item=request_body)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': request_body
        }
        return build_response(200, body)
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])        

def delete_medication(Med,Q):
    try:
        response = dynamodb_table.delete_item(
            Key={'Med': Med,'SortKey':Q},
            ReturnValues='ALL_OLD'
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'Item': response
        }
        return build_response(200, body)
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])

def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }    
            
































