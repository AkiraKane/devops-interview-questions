# Launch an EC2 Web Server Instance

> **Company:** EPAM | **Difficulty:** Easy

---

#### **Scenario**

A basic landing page needs to be delivered via an EC2 instance accessible over HTTP with its own security group.

#### **Task**

1. Create a security group named `web-sg` permitting TCP port 80 from any IPv4
2. Launch a `t2.micro` instance tagged as `web-1` using the `web-sg` security group
3. Automatically provision `/var/www/html/index.html` containing "Hello from web-1" during startup using user data

---
📹 [Video Solution](https://prepare.sh/interview/devops/aws/launch-an-ec2-web-server-instance)