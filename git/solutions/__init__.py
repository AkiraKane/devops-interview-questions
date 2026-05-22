"""
Git Solutions Package

This package contains Python solutions for all 22 Git interview questions.
Each module provides a main() function that demonstrates the Git solution.
"""

# Import all solution modules
from .apply_specific_stash_from_multiple_stashes import (
    main as apply_specific_stash_main,
    apply_specific_stash
)
from .checkout_single_file_from_another_branch import (
    main as checkout_single_file_main,
    checkout_single_file
)
from .cherry_pick_specific_commit import (
    main as find_and_cherry_pick_commit_main,
    find_and_cherry_pick_commit
)
from .convert_remote_from_https_to_ssh import (
    main as convert_remote_url_main,
    convert_remote_url
)
from .create_an_annotated_tag import (
    main as create_annotated_tag_main,
    create_annotated_tag
)
from .fix_repository_with_unrelated_histories import (
    main as fix_unrelated_histories_main,
    fix_unrelated_histories
)
from .merge_feature_branch_and_delete import (
    main as merge_and_delete_branch_main,
    merge_and_delete_branch
)
from .merge_repositories_preserving_both_histories import (
    main as merge_repositories_into_monorepo_main,
    merge_repositories_into_monorepo
)
from .rebase_branch_with_reversed_commit_order import (
    main as rebase_with_reversed_order_main,
    rebase_with_reversed_order
)
from .rebase_feature_branch import (
    main as rebase_feature_onto_main_main,
    rebase_feature_onto_main
)
from .rebase_feature_branch_onto_correct_base import (
    main as rebase_onto_correct_base_main,
    rebase_onto_correct_base
)
from .recover_lost_commits_from_detached_head import (
    main as recover_lost_commits_main,
    recover_lost_commits
)
from .remove_file_from_entire_git_history import (
    main as remove_file_from_history_main,
    remove_file_from_history
)
from .remove_last_commit_and_discard_changes import (
    main as remove_last_commit_discard_changes_main,
    remove_last_commit_discard_changes
)
from .restore_file_to_previous_version import (
    main as restore_file_to_previous_version_main,
    restore_file_to_previous_version
)
from .shallow_clone_limited_to_latest_commit import (
    main as shallow_clone_main,
    shallow_clone
)
from .stage_only_specific_files import (
    main as stage_only_specific_files_main,
    stage_only_specific_files
)
from .stash_work_fix_bug_restore_and_update import (
    main as stash_work_fix_bug_restore_update_main,
    stash_work_fix_bug_restore_update
)
from .stash_work_fix_bug_resume import (
    main as stash_work_fix_bug_resume_main,
    stash_work_fix_bug_resume
)
from .undo_commits_but_keep_changes import (
    main as undo_commits_keep_changes_main,
    undo_commits_keep_changes
)
from .update_submodule_to_latest_commit import (
    main as update_submodule_to_latest_main,
    update_submodule_to_latest
)
from .view_unique_commits_between_branch_and_origin import (
    main as find_unique_commits_main,
    find_unique_commits
)

# All solution functions mapped by question name
SOLUTIONS = {
    "apply_specific_stash_from_multiple_stashes": apply_specific_stash,
    "checkout_single_file_from_another_branch": checkout_single_file,
    "cherry_pick_specific_commit": find_and_cherry_pick_commit,
    "convert_remote_from_https_to_ssh": convert_remote_url,
    "create_an_annotated_tag": create_annotated_tag,
    "fix_repository_with_unrelated_histories": fix_unrelated_histories,
    "merge_feature_branch_and_delete": merge_and_delete_branch,
    "merge_repositories_preserving_both_histories": merge_repositories_into_monorepo,
    "rebase_branch_with_reversed_commit_order": rebase_with_reversed_order,
    "rebase_feature_branch": rebase_feature_onto_main,
    "rebase_feature_branch_onto_correct_base": rebase_onto_correct_base,
    "recover_lost_commits_from_detached_head": recover_lost_commits,
    "remove_file_from_entire_git_history": remove_file_from_history,
    "remove_last_commit_and_discard_changes": remove_last_commit_discard_changes,
    "restore_file_to_previous_version": restore_file_to_previous_version,
    "shallow_clone_limited_to_latest_commit": shallow_clone,
    "stage_only_specific_files": stage_only_specific_files,
    "stash_work_fix_bug_restore_and_update": stash_work_fix_bug_restore_update,
    "stash_work_fix_bug_resume": stash_work_fix_bug_resume,
    "undo_commits_but_keep_changes": undo_commits_keep_changes,
    "update_submodule_to_latest_commit": update_submodule_to_latest,
    "view_unique_commits_between_branch_and_origin": find_unique_commits,
}

__all__ = [
    "SOLUTIONS",
    "apply_specific_stash",
    "checkout_single_file",
    "find_and_cherry_pick_commit",
    "convert_remote_url",
    "create_annotated_tag",
    "fix_unrelated_histories",
    "merge_and_delete_branch",
    "merge_repositories_into_monorepo",
    "rebase_with_reversed_order",
    "rebase_feature_onto_main",
    "rebase_onto_correct_base",
    "recover_lost_commits",
    "remove_file_from_history",
    "remove_last_commit_discard_changes",
    "restore_file_to_previous_version",
    "shallow_clone",
    "stage_only_specific_files",
    "stash_work_fix_bug_restore_update",
    "stash_work_fix_bug_resume",
    "undo_commits_keep_changes",
    "update_submodule_to_latest",
    "find_unique_commits",
]