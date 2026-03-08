# Create Route 53 Health Checks

> **Company:** Autodesk | **Difficulty:** Easy

---

#### **Scenario**

Your infrastructure has two application endpoints requiring distinct monitoring strategies through Route 53 health checks, each with different protocols, ports, health check intervals, and failure thresholds.

#### **Task**

Configure two health checks:

1. **web-server** at `10.0.1.10` using HTTP on port 80 with a `/health` path, 3-failure threshold, and 30-second intervals
2. **api-server** at `10.0.2.10` using HTTPS on port 443, 5-failure threshold, 10-second fast intervals, inverted status enabled, and monitoring from three specific AWS regions (US East, EU Ireland, Asia Pacific Singapore)

---
📹 [Video Solution](https://prepare.sh/interview/devops/aws/create-route-53-health-checks)