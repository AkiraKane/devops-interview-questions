"""
Amazon Cloud Solutions — `solutions/__init__.py`

Provides programmatic access to all AWS solution runners via their main() functions.

Usage:
    from cloud.solutions import (
        audit_and_enforce_least_privilege_iam_permissions,
        build_a_serverless_api,
        ...
    )

    # Run any solution
    create_hello_world_lambda_function.main()
"""

# Relative imports so this works when solutions/ is imported as part of the cloud package
from .audit_and_enforce_least_privilege_iam_permissions import (
    main as audit_and_enforce_least_privilege_iam_permissions,
)
from .build_a_serverless_api_with_lambda_api_gateway_and_dynamodb import (
    main as build_a_serverless_api,
)
from .create_a_hello_world_lambda_function import (
    main as create_hello_world_lambda_function,
)
from .create_aws_iam_admin_user_with_group_and_policy import (
    main as create_aws_iam_admin_user,
)
from .create_iam_role_for_ec2_with_full_iam_access import (
    main as create_iam_role_for_ec2,
)
from .create_route_53_health_checks import (
    main as create_route_53_health_checks,
)
from .create_route_53_hosted_zone_and_dns_records import (
    main as create_route_53_hosted_zone,
)
from .deploy_an_internal_web_application_with_vpc_ec2_alb_and_route_53 import (
    main as deploy_internal_web_application,
)
from .design_egress_only_vpc_with_nat import (
    main as design_egress_only_vpc,
)
from .launch_an_ec2_web_server_instance import (
    main as launch_ec2_web_server,
)

__all__ = [
    "audit_and_enforce_least_privilege_iam_permissions",
    "build_a_serverless_api",
    "create_hello_world_lambda_function",
    "create_aws_iam_admin_user",
    "create_iam_role_for_ec2",
    "create_route_53_health_checks",
    "create_route_53_hosted_zone",
    "deploy_internal_web_application",
    "design_egress_only_vpc",
    "launch_ec2_web_server",
]