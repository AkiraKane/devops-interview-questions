"""
Solution for: Create a Hello World Lambda Function

Company: Adobe | Difficulty: Easy

Scenario:
Your team needs a simple Lambda function for a greeting microservice.

Task:
1. Create Lambda function `hello-function` accepting `name` field, returns `Hello <name>`
2. Use pre-created IAM role `lambda-execution-role`
3. Invoke the function with {"name": "World"} and verify output is "Hello World"
"""

import io
import json
import zipfile
import boto3


LAMBDA_HANDLER_CODE = '''import json


def lambda_handler(event, context):
    name = event.get('name', 'World')
    return f"Hello {name}"
'''


def create_zip_payload():
    """Create a zip file containing lambda_function.py."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('lambda_function.py', LAMBDA_HANDLER_CODE)
    buffer.seek(0)
    return buffer.read()


def create_hello_function(lambda_client, iam_client):
    """Create the hello-function Lambda using the pre-created lambda-execution-role."""
    # Verify the execution role exists
    try:
        role = iam_client.get_role(RoleName='lambda-execution-role')
        role_arn = role['Role']['Arn']
        print(f"Using existing role: lambda-execution-role ({role_arn})")
    except iam_client.exceptions.NoSuchEntityException:
        raise RuntimeError(
            "IAM role 'lambda-execution-role' does not exist. "
            "Please create it first via AWS Console or CLI."
        )

    zip_bytes = create_zip_payload()

    try:
        lambda_client.create_function(
            FunctionName='hello-function',
            Runtime='python3.12',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_bytes},
            Description='Simple Hello World Lambda function for Adobe',
            Timeout=10,
            MemorySize=128
        )
        print("Created Lambda function 'hello-function'")
    except lambda_client.exceptions.ResourceConflictException:
        print("Lambda function 'hello-function' already exists — skipping creation")


def invoke_and_verify(lambda_client):
    """Invoke hello-function with {"name": "World"} and verify output."""
    payload = json.dumps({"name": "World"})

    response = lambda_client.invoke(
        FunctionName='hello-function',
        InvocationType='RequestResponse',
        Payload=payload
    )

    result = json.loads(response['Payload'].read().decode('utf-8'))
    expected = "Hello World"

    print(f"Payload: {payload}")
    print(f"Response: {result}")

    if result == expected:
        print(f"VERIFIED: Output '{result}' matches expected '{expected}'")
    else:
        print(f"MISMATCH: Got '{result}', expected '{expected}'")

    return result


def main():
    iam_client = boto3.client('iam')
    lambda_client = boto3.client('lambda')

    print("=== Step 1: Create hello-function using lambda-execution-role ===")
    create_hello_function(lambda_client, iam_client)

    print("\n=== Step 2 & 3: Invoke and verify ===")
    invoke_and_verify(lambda_client)


if __name__ == '__main__':
    main()