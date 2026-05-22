"""
Programming Solutions for DevOps Interview Questions

Each module implements solutions for GitHub Actions workflow questions.
"""

from .docker_image_tagging import generate_build_workflow as docker_image_tagging
from .rollback_deployment import generate_deploy_workflow as rollback_deployment
from .environment_gated_deployment import generate_deploy_workflow as environment_gated
from .github_actions_retry import generate_retry_workflow
from .github_actions_matrix import generate_pr_tests_workflow as github_actions_matrix
from .github_actions_timeout import generate_timeout_workflow
from .job_dependency import generate_pipeline_workflow
from .artifact_handoff import generate_artifact_handoff_workflow
from .path_based_execution import generate_infra_check_workflow
from .pr_test_gate import generate_pr_tests_workflow as pr_test_gate
from .reusable_workflow import generate_shared_build_workflow, generate_deploy_workflow as generate_caller_workflow
from .gitops_promotion import generate_promote_workflow

__all__ = [
    "docker_image_tagging",
    "rollback_deployment",
    "environment_gated",
    "generate_retry_workflow",
    "github_actions_matrix",
    "generate_timeout_workflow",
    "generate_pipeline_workflow",
    "generate_artifact_handoff_workflow",
    "generate_infra_check_workflow",
    "pr_test_gate",
    "generate_shared_build_workflow",
    "generate_caller_workflow",
    "generate_promote_workflow",
]