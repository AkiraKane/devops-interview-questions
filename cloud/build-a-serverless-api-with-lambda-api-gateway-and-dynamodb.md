# Build a Serverless API with Lambda, API Gateway, and DynamoDB

> **Company:** Amazon | **Difficulty:** Hard

---

#### **Scenario**

An internal serverless API is needed for order management. Orders must be stored in a DynamoDB table with all access routed through a Lambda function — never direct database access. The Lambda execution role should follow least-privilege principles, limiting permissions to only what's necessary.

#### **Task**

1. Create a DynamoDB table named `orders` with `orderId` as the partition key
2. Create an IAM role called `lambda-orders-role` that assumes Lambda permissions
3. Create a `orders-handler` Lambda function using Python 3.12 with environment variable `TABLE_NAME=orders` (code provided at `/tmp/handler.py`)
4. Create a REST API named `orders-api` with an `/orders` endpoint supporting GET and POST methods
5. Deploy to a `dev` stage for public access

---
📹 [Video Solution](https://prepare.sh/interview/devops/aws/build-a-serverless-api-with-lambda-api-gateway-and-dynamodb)
