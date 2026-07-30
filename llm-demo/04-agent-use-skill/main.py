"""Agent Skills 示例：扫描 skills/*/SKILL.md，把 name/description 注入 system prompt，
需要时通过 load_skill 按需加载完整指令（progressive disclosure）。"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
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
        skills[name] = Skill(name=name, description=description, body=body, path=skill_md)
    return skills


SKILLS = discover_skills(SKILLS_DIR)


def skills_catalog(skills: dict[str, Skill]) -> str:
    if not skills:
        return "(no skills found)"
    lines = []
    for skill in skills.values():
        lines.append(f"- {skill.name}: {skill.description}")
    return "\n".join(lines)


@tool
def load_skill(skill_name: str) -> str:
    """Load a specialized skill's full instructions by name.

    Call this when the user task matches a skill description in the catalog.
    Available skills are listed in the system prompt.

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
        "Follow the instructions above to complete the user's request."
    )


llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_base="https://api.deepseek.com/v1",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.2,
)

SYSTEM = f"""你是电商助手，具备可按需加载的 Skills。

## 可用 Skills（仅 name + description；完整内容需 load_skill）
{skills_catalog(SKILLS)}

## 工作方式（progressive disclosure）
1. 阅读用户请求，判断是否匹配某个 skill 的 description
2. 匹配时先调用 load_skill 加载完整指令
3. 严格按 skill 指令回答；不要凭空编造政策
4. 若不匹配任何 skill，直接正常回答

回复使用简体中文。"""

print("SYSTEM:")
print(SYSTEM)

agent = create_agent(
    model=llm,
    tools=[load_skill],
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

# 打印工具调用轨迹，便于观察是否识别并加载了 skill
for msg in response["messages"]:
    if getattr(msg, "tool_calls", None):
        for call in msg.tool_calls:
            print(f"tool_call -> {call['name']}({call.get('args', {})})")
