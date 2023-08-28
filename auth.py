import boto3
import json

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodbTableName = 'customers'
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
customerTable = dynamodb.Table(dynamodbTableName)
bucketName = 'befit-visitor-images'


def lambda_handler(event, context):
    print(event)
    objectKey = event['queryStringParameters']['objectKey']
    image_bytes = s3.get_object[Bucket = bucketName, Key = objectKey]['Body'].read()
    response = rekognition.search_faces_by_image(
        CollectionId='customers',
        Image={'Bytes': image_bytes}
    )

    for match in response['FaceMatches']:
        print(match['Face']['FaceId'], match['Face']['Confidence'])

        face = customerTable.get_item(
            Key={
                'rekognitionId': match['Face']['FaceId']
            }
        )
        if 'Item' in face:
            print('Person found', face['Item'])
            return buildResponse(200, {
                'Message': 'Success',
                'firstName': face['Item']['firstName']
                'lastName': face['Item']['lastName']
            })
    print('Person could not be recognized.')

    return buildResponse(403, {'Message': 'Person Not Found'})


def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            "Access-Control-Allow-Credentials": true,
        }

    }
    if body is not None:
        reponse['body'] = json.dumps(body)
    return response
