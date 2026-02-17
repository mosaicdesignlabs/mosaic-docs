"""
Configuration for the document control pipeline.

All secrets and environment-specific values come from environment variables.
Enums and constants are defined here.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

VALID_CATEGORIES = frozenset(
    {"SOP", "POL", "WI", "RPT", "DG", "STR", "GOV", "MKT", "PRO"}
)

VALID_DEPARTMENTS = frozenset({"ENG", "OPS", "FIN", "BD"})

VALID_ORGS = frozenset({"MOS", "POP", "XCC", "ACC"})

VALID_STATUSES = frozenset({"Draft", "Released"})

VALID_DESIRED_STATES = frozenset({"draft", "release", "none"})

# ---------------------------------------------------------------------------
# Paths (relative to repo root)
# ---------------------------------------------------------------------------

DOCS_DIR = "docs"
IMAGES_DIR = "docs/images"
META_DIR = "docs/.meta"

# ---------------------------------------------------------------------------
# Config dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PipelineConfig:
    """Runtime configuration loaded from environment variables."""

    notion_token: str
    notion_database_id: str

    repo_root: Path
    gitea_url: str = ""
    gitea_token: str = ""
    gitea_repo_owner: str = ""
    gitea_repo_name: str = ""

    git_commit_sha: str = ""
    git_branch: str = ""
    git_pr_number: str = ""
    git_pr_url: str = ""
    git_actor: str = ""

    bot_commit_author: str = "mosaic-bot"

    # Constructed at runtime
    docs_dir: Path = field(init=False)
    images_dir: Path = field(init=False)
    meta_dir: Path = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "docs_dir", self.repo_root / DOCS_DIR)
        object.__setattr__(self, "images_dir", self.repo_root / IMAGES_DIR)
        object.__setattr__(self, "meta_dir", self.repo_root / META_DIR)

    @property
    def raw_content_base_url(self) -> str:
        """Base URL for raw file access in Gitea (for image hosting)."""
        if self.gitea_url and self.gitea_repo_owner and self.gitea_repo_name:
            return (
                f"{self.gitea_url}/{self.gitea_repo_owner}"
                f"/{self.gitea_repo_name}/raw/branch/main"
            )
        return ""


def load_config(repo_root: Path | str | None = None) -> PipelineConfig:
    """Load pipeline configuration from environment variables."""
    if repo_root is None:
        repo_root = Path(os.environ.get("GITHUB_WORKSPACE", ".")).resolve()
    else:
        repo_root = Path(repo_root).resolve()

    return PipelineConfig(
        notion_token=os.environ.get("NOTION_TOKEN", ""),
        notion_database_id=os.environ.get("NOTION_DATABASE_ID_DOCUMENTS", ""),
        repo_root=repo_root,
        gitea_url=os.environ.get("GITEA_URL", ""),
        gitea_token=os.environ.get("GITEA_TOKEN", ""),
        gitea_repo_owner=os.environ.get("GITHUB_REPOSITORY_OWNER", ""),
        gitea_repo_name=os.environ.get("GITHUB_REPOSITORY", "").split("/")[-1]
        if os.environ.get("GITHUB_REPOSITORY")
        else "",
        git_commit_sha=os.environ.get("GITHUB_SHA", ""),
        git_branch=os.environ.get("GITHUB_REF_NAME", ""),
        git_pr_number=os.environ.get("PR_NUMBER", ""),
        git_pr_url=os.environ.get("PR_URL", ""),
        git_actor=os.environ.get("GITHUB_ACTOR", ""),
        bot_commit_author=os.environ.get("BOT_COMMIT_AUTHOR", "mosaic-bot"),
    )
