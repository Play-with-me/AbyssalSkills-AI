"""
AbyssalSkillsD - Data Models
Defines structured dataclasses and JSON serializable models for Skills,
References, Rules, and Installation Targets.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
import time

@dataclass
class ReferenceDoc:
    id: str
    title: str
    filename: str
    content: str
    category: str = "general"

@dataclass
class RuleDoc:
    id: str
    name: str
    filename: str
    content: str
    rule_type: str = "always_on"  # always_on, system, tool_guard

@dataclass
class SkillItem:
    id: str
    name: str
    display_title: str
    version: str
    description: str
    category: str  # Architecture, UI/UX, Debugging, Content, Database, DevOps, etc.
    tags: List[str] = field(default_factory=list)
    author: str = "Community"
    repo_url: Optional[str] = None
    skill_content: str = ""  # Main SKILL.md body
    yaml_frontmatter: Dict[str, Any] = field(default_factory=dict)
    references: List[ReferenceDoc] = field(default_factory=list)
    rules: List[RuleDoc] = field(default_factory=list)
    has_graphify: bool = False
    graphify_summary: Optional[Dict[str, Any]] = None
    installed_targets: List[str] = field(default_factory=list) # ['antigravity', 'claude', 'copilot', 'workspace']
    installed_path: Optional[str] = None  # Actual path on disk where SKILL.md is located
    has_update: bool = False  # True if disk version differs from registry version
    always_on_enabled: bool = False
    icon: str = "Sparkles"
    is_favorite: bool = False
    when_to_use: str = ""
    use_case_group: str = "all"  # plan_debug, ui_ux, web_db, testing_qa, design_assets
    starter_prompts: List[Dict[str, str]] = field(default_factory=list)
    source_group: str = "skill_ai"  # "skill_ai", "addy_osmani", "community"
    is_persona: bool = False
    license: str = "MIT"
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillItem":
        refs = [ReferenceDoc(**r) if isinstance(r, dict) else r for r in data.get("references", [])]
        rules = [RuleDoc(**r) if isinstance(r, dict) else r for r in data.get("rules", [])]
        field_names = {f.name for f in cls.__dataclass_fields__.values()}
        clean_data = {k: v for k, v in data.items() if k in field_names and k not in ["references", "rules"]}
        return cls(references=refs, rules=rules, **clean_data)

@dataclass
class InstallRequest:
    skill_id: str
    targets: List[str]  # ['antigravity', 'claude', 'copilot', 'workspace']
    workspace_path: Optional[str] = None
    enable_always_on: bool = True
    with_graphify: bool = True

@dataclass
class InstallResult:
    success: bool
    skill_id: str
    installed_paths: List[str] = field(default_factory=list)
    rules_paths: List[str] = field(default_factory=list)
    graphify_status: str = "skipped" # success, skipped, error
    message: str = ""
    errors: List[str] = field(default_factory=list)
