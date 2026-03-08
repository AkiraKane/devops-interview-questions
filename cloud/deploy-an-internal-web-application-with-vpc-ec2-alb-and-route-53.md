# Deploy an Internal Web Application with VPC, EC2, ALB, and Route 53

> **Company:** Lyft | **Difficulty:** Hard

---

#### **Scenario**

You need to deploy a web application accessible only within a VPC. EC2 instances run in private subnets behind an Application Load Balancer in public subnets. A startup script at `/tmp/userdata.sh` runs a simple HTTP server with a `/health` endpoint on port 80.

#### **Task**

1. Create a VPC named `app-vpc` using CIDR `10.0.0.0/16` with public and private subnets across two availability zones
2. Establish two security groups: `alb-sg` allowing HTTP from internal networks, and `ec2-sg` allowing HTTP only from the load balancer
3. Launch two EC2 instances in private subnets using Amazon Linux 2 AMI with the provided startup script
4. Configure an ALB named `app-alb` with target group `app-tg`, health checks at `/health`, and HTTP listener on port 80
5. Create a private Route 53 hosted zone for `internal.example.com` and add a CNAME record `app.internal.example.com` pointing to the ALB

---
[Solution](https://prepare.sh/interview/devops/aws/deploy-an-internal-web-application-with-vpc-ec2-alb-and-route-53)
