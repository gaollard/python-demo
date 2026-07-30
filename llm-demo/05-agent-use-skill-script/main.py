"""Agent Skills + Scripts 示例：每个 skill 自带 scripts/，
load_skill 按需加载指令，run_skill_script 执行 skill 目录下的确定性脚本。"""

from __future__ import annotations

import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

SKILLS_DIR = Path(__file__).resolve().parent / "skills"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    body: str
    path: Path
    scripts: tuple[Path, ...] = field(default_factory=tuple)

    @property
    def root(self) -> Path:
        return self.path.parent


def _parse_frontmatter(raw: str) -> tuple[dict[str, str], str]:
    """Parse YAML-ish frontmatter without requiring a full YAML dependency."""
    match = FRONTMATTER_RE.match(raw.strip())
    if not match:
        return {}, raw

    meta: dict[str, str] = {}
    key: str | None = None
    chunks: list[str] = []
    for line in match.group(1).splitlines():
        if re.match(r"^[a-zA-Z0-9_-]+:\s*", line):
            if key is not None:
                meta[key] = " ".join(chunks).strip().strip("\"'")
            key, _, rest = line.partition(":")
            key = key.strip()
            chunks = [rest.strip().lstrip(">").strip()]
        elif key is not None:
            chunks.append(line.strip())
    if key is not None:
        meta[key] = " ".join(chunks).strip().strip("\"'")
    return meta, match.group(2).strip()


def _discover_scripts(skill_dir: Path) -> tuple[Path, ...]:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.is_dir():
        return ()
    return tuple(sorted(p for p in scripts_dir.glob("*.py") if p.is_file()))


def discover_skills(skills_dir: Path) -> dict[str, Skill]:
    """Scan skills/*/SKILL.md and return skills keyed by name."""
    skills: dict[str, Skill] = {}
    if not skills_dir.is_dir():
        return skills

    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        meta, body = _parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = (meta.get("name") or skill_md.parent.name).strip()
        description = (meta.get("description") or "").strip()
        if not description:
            description = f"Skill defined in {skill_md.parent.name}"
        scripts = _discover_scripts(skill_md.parent)
        skills[name] = Skill(
            name=name,
            description=description,
            body=body,
            path=skill_md,
            scripts=scripts,
        )
    return skills


SKILLS = discover_skills(SKILLS_DIR)


def skills_catalog(skills: dict[str, Skill]) -> str:
    if not skills:
        return "(no skills found)"
    lines = []
    for skill in skills.values():
        script_names = ", ".join(s.name for s in skill.scripts) or "(none)"
        lines.append(
            f"- {skill.name}: {skill.description} [scripts: {script_names}]"
        )
    return "\n".join(lines)


def _scripts_help(skill: Skill) -> str:
    if not skill.scripts:
        return "(no scripts)"
    lines = []
    for script in skill.scripts:
        rel = script.relative_to(skill.root).as_posix()
        lines.append(f"- {rel}")
    return "\n".join(lines)


@tool
def load_skill(skill_name: str) -> str:
    """Load a specialized skill's full instructions and list its scripts.

    Call this when the user task matches a skill description in the catalog.
    After loading, use run_skill_script to execute any bundled scripts.

    Args:
        skill_name: Skill name, e.g. refund-policy or support-reply
    """
    print(f"[tool] load_skill(skill_name={skill_name!r})")
    skill = SKILLS.get(skill_name.strip())
    if not skill:
        available = ", ".join(SKILLS) or "(none)"
        return f"Unknown skill '{skill_name}'. Available: {available}"
    return (
        f"# Skill: {skill.name}\n"
        f"Source: {skill.path}\n\n"
        f"{skill.body}\n\n"
        f"## Bundled scripts (run via run_skill_script)\n"
        f"{_scripts_help(skill)}\n\n"
        "Follow the instructions above. Prefer running scripts over reinventing logic."
    )


@tool
def run_skill_script(skill_name: str, script_name: str, cli_args: str = "") -> str:
    """Run a Python script bundled under skills/<skill>/scripts/.

    Only scripts discovered for that skill are allowed (sandbox by path).
    Working directory is the skill root so relative paths like scripts/foo.py work.

    Args:
        skill_name: Skill name, e.g. refund-policy
        script_name: Script file name, e.g. calculate_refund.py
        cli_args: CLI arguments string, e.g. '--unit-price 89 --qty 2 --reason defect --membership gold'
    """
    print(
        f"[tool] run_skill_script(skill_name={skill_name!r}, "
        f"script_name={script_name!r}, cli_args={cli_args!r})"
    )
    skill = SKILLS.get(skill_name.strip())
    if not skill:
        available = ", ".join(SKILLS) or "(none)"
        return f"Unknown skill '{skill_name}'. Available: {available}"

    name = Path(script_name.strip()).name
    script = next((s for s in skill.scripts if s.name == name), None)
    if script is None:
        available = ", ".join(s.name for s in skill.scripts) or "(none)"
        return f"Unknown script '{script_name}' for skill '{skill.name}'. Available: {available}"

    try:
        argv = shlex.split(cli_args) if cli_args.strip() else []
    except ValueError as exc:
        return f"Failed to parse cli_args: {exc}"

    cmd = [sys.executable, str(script), *argv]
    try:
        completed = subprocess.run(
            cmd,
            cwd=skill.root,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "Script timed out after 30s"

    parts = [
        f"exit_code={completed.returncode}",
        f"cmd={' '.join(shlex.quote(c) for c in cmd)}",
    ]
    if completed.stdout.strip():
        parts.append("--- stdout ---\n" + completed.stdout.rstrip())
    if completed.stderr.strip():
        parts.append("--- stderr ---\n" + completed.stderr.rstrip())
    return "\n".join(parts)


llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_base="https://api.deepseek.com/v1",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.2,
)

SYSTEM = f"""你是电商助手，具备可按需加载的 Skills；每个 skill 可自带可执行 scripts。

## 可用 Skills（仅 name + description + scripts 列表；完整内容需 load_skill）
{skills_catalog(SKILLS)}

## 工作方式（progressive disclosure + scripts）
1. 阅读用户请求，判断是否匹配某个 skill 的 description
2. 匹配时先调用 load_skill 加载完整指令与脚本列表
3. 若 skill 要求运行脚本：调用 run_skill_script(skill_name, script_name, cli_args)
4. 严格按 skill 指令 + 脚本输出回答；不要自己重算或编造政策数字
5. 若不匹配任何 skill，直接正常回答

回复使用简体中文。"""

print("SYSTEM:")
print(SYSTEM)

agent = create_agent(
    model=llm,
    tools=[load_skill, run_skill_script],
    system_prompt=SYSTEM,
)

USER_QUERY = (
    "金牌会员 Alice 买的耳机单价 89 美元、数量 2，因为质量问题（defect）要退货。"
    "请按退款政策算出应退多少，并起草一封中文客服确认回复邮件。"
)

print("已发现 Skills:")
print(skills_catalog(SKILLS))
print("=" * 60)

response = agent.invoke({"messages": [{"role": "user", "content": USER_QUERY}]})

print("最终回复:")
print(response["messages"][-1].content)
print("=" * 60)

for msg in response["messages"]:
    if getattr(msg, "tool_calls", None):
        for call in msg.tool_calls:
            print(f"tool_call -> {call['name']}({call.get('args', {})})")
