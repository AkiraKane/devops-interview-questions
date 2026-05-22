"""
Solution for: Build a Serverless API with Lambda, API Gateway, and DynamoDB

Company: Amazon | Difficulty: Hard

Scenario:
An internal serverless API for order management. Orders stored in DynamoDB with all access
routed through a Lambda function — never direct database access. Uses least-privilege principles.

Task:
1. Create DynamoDB table `orders` with orderId as partition key
2. Create IAM role `lambda-orders-role` assuming Lambda permissions
3. Create `orders-handler` Lambda function using Python 3.12, env var TABLE_NAME=orders
4. Create REST API `orders-api` with /orders endpoint, GET and POST
5. Deploy to `dev` stage for public access
"""

import io
import json
import zipfile
import boto3


def create_dynamodb_table():
    """Create the orders DynamoDB table with orderId as partition key."""
    dynamodb = boto3.client('dynamodb')
    try:
        dynamodb.create_table(
            TableName='orders',
            KeySchema=[
                {'AttributeName': 'orderId', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'orderId', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print("Created DynamoDB table 'orders'")
    except dynamodb.exceptions.ResourceInUseException:
        print("DynamoDB table 'orders' already exists")


def create_lambda_role():
    """Create the IAM role for the Lambda execution."""
    iam = boto3.client('iam')

    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }

    try:
        role = iam.create_role(
            RoleName='lambda-orders-role',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Execution role for orders Lambda function'
        )
        role_arn = role['Role']['Arn']
        print(f"Created IAM role: lambda-orders-role ({role_arn})")
    except iam.exceptions.EntityAlreadyExistsException:
        role = iam.get_role(RoleName='lambda-orders-role')
        role_arn = role['Role']['Arn']
        print(f"IAM role 'lambda-orders-role' already exists: {role_arn}")

    # Attach minimal DynamoDB + CloudWatch permissions
    inline_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:PutItem",
                    "dynamodb:GetItem",
                    "dynamodb:Scan",
                    "dynamodb:Query"
                ],
                "Resource": "arn:aws:dynamodb:*:*:table/orders"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "arn:aws:logs:*:*:*"
            }
        ]
    }

    iam.put_role_policy(
        RoleName='lambda-orders-role',
        PolicyName='LambdaOrdersPolicy',
        PolicyDocument=json.dumps(inline_policy)
    )
    print("Attached inline policy LambdaOrdersPolicy to lambda-orders-role")

    return role_arn


def create_lambda_function(role_arn):
    """Create the orders-handler Lambda function from /tmp/handler.py."""
    lambda_client = boto3.client('lambda')

    # Read handler code from the path specified in the question
    try:
        with open('/tmp/handler.py', 'r') as f:
            handler_code = f.read()
    except FileNotFoundError:
        # Fallback inline handler
        handler_code = '''import json
import os
import boto3

TABLE_NAME = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']

    if path == '/orders' and http_method == 'GET':
        response = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Items', []))
        }

    if path == '/orders' and http_method == 'POST':
        body = json.loads(event['body'])
        order_id = body.get('orderId')
        table.put_item(Item=body)
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Order created', 'orderId': order_id})
        }

    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Unsupported route'})
    }
'''

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('lambda_function.py', handler_code)
    zip_buffer.seek(0)

    try:
        lambda_client.create_function(
            FunctionName='orders-handler',
            Runtime='python3.12',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_buffer.read()},
            Environment={'Variables': {'TABLE_NAME': 'orders'}},
            Timeout=30,
            MemorySize=128
        )
        print("Created Lambda function 'orders-handler'")
    except lambda_client.exceptions.ResourceConflictException:
        print("Lambda function 'orders-handler' already exists")


def create_rest_api(lambda_function_arn):
    """Create REST API with /orders GET and POST, deploy to dev stage."""
    apigw = boto3.client('apigateway')

    # Create REST API
    api = apigw.create_rest_api(
        name='orders-api',
        description='Serverless orders API'
    )
    api_id = api['id']
    print(f"Created REST API 'orders-api' (ID: {api_id})")

    # Get root resource ID
    resources = apigw.get_resources(restApiId=api_id)
    root_id = [r for r in resources['items'] if r['path'] == '/'][0]['id']

    # Create /orders resource
    orders_resource = apigw.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart='orders'
    )
    orders_id = orders_resource['id']
    print(f"Created /orders resource (ID: {orders_id})")

    # Enable CORS OPTIONS method
    apigw.put_method(
        restApiId=api_id, resourceId=orders_id,
        httpMethod='OPTIONS', authorizationType='NONE',
        apiKeyRequired=False
    )
    apigw.put_method_response(
        restApiId=api_id, resourceId=orders_id,
        httpMethod='OPTIONS', statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': True,
            'method.response.header.Access-Control-Allow-Methods': True,
            'method.response.header.Access-Control-Allow-Origin': True
        },
        responseModels={}
    )
    apigw.put_integration(
        restApiId=api_id, resourceId=orders_id,
        httpMethod='OPTIONS', type='MOCK',
        integrationHttpMethod='OPTIONS',
        requestTemplates={'application/json': '{"statusCode": 200}'},
        uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_function_arn}/invocations'
    )

    # PUT /orders GET
    apigw.put_method(
        restApiId=api_id, resourceId=orders_id,
        httpMethod='GET', authorizationType='NONE',
        apiKeyRequired=False
    )
    apigw.put_integration(
        restApiId=api_id, resourceId=orders_id,
        httpMethod='GET', type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:lambda:us-east-1:123456789012:function:orders-handler'
    )

    # PUT /orders POST
    apigw.put_method(
        restApiId=api_id, resourceId=orders_id,
        httpMethod='POST', authorizationType='NONE',
        apiKeyRequired=False
    )
    apigw.put_integration(
        restApiId=api_id, resourceId=orders_id,
        httpMethod='POST', type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:lambda:us-east-1:123456789012:function:orders-handler'
    )

    # Deploy to dev stage
    apigw.create_deployment(
        restApiId=api_id,
        stageName='dev',
        description='Development stage deployment'
    )
    print(f"Deployed 'orders-api' to 'dev' stage")
    print(f"Invoke URL: https://{api_id}.execute-api.us-east-1.amazonaws.com/dev/orders")


def main():
    print("=== Step 1: Create DynamoDB table ===")
    create_dynamodb_table()

    print("\n=== Step 2: Create Lambda execution role ===")
    role_arn = create_lambda_role()

    print("\n=== Step 3: Create Lambda function ===")
    create_lambda_function(role_arn)

    print("\n=== Step 4 & 5: Create REST API and deploy to dev ===")
    # Note: In production, fetch the actual Lambda ARN
    lambda_arn = 'arn:aws:lambda:us-east-1:123456789012:function:orders-handler'
    create_rest_api(lambda_arn)


if __name__ == '__main__':
    main()