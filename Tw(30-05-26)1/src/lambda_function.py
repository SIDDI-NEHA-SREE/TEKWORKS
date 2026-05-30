import os
import json
import boto3

# Initialize backend AWS SageMaker Runtime Client interface
runtime = boto3.client('runtime.sagemaker')
ENDPOINT_NAME = os.environ.get('ENDPOINT_NAME', 'your-sagemaker-endpoint-name')

def lambda_handler(event, context):
    try:
        # Extract body payload arriving via API Gateway route
        body = json.loads(event['body'])
        features = body['features'] 
        
        # Dispatch structured query matrix to SageMaker Endpoint
        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType='application/json',
            Body=json.dumps({"instances": [features]})
        )
        
        # Decode neural network array response back to API
        result = json.loads(response['Body'].read().decode())
        prediction = result['predictions'][0][0]
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({'churn_probability': prediction})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error_log_trace': str(e)})
        }
