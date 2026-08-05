# Code Wiki

代码分析 Agent：输入工作空间路径 + 问题后，自主检索相关代码并回答。

## 关注维度

- 准确率（优先）
- 成本与上下文
- 检索质量
- 体验与可观测
- 工程稳健性

## 安装

```bash
cd code-wiki
pip install -e ".[dev]"
```

需要：Python 3.11+、[DeepSeek API Key](https://platform.deepseek.com/)；推荐安装 `ripgrep`（`rg`）。

默认使用 DeepSeek OpenAI 兼容接口（`https://api.deepseek.com` + `deepseek-v4-flash`）。

## 配置

| 变量 | 说明 |
|------|------|
| `CODE_WIKI_API_KEY` 或 `DEEPSEEK_API_KEY` | DeepSeek API Key（必填） |
| `CODE_WIKI_BASE_URL` | 默认 `https://api.deepseek.com` |
| `CODE_WIKI_MODEL` | 默认 `deepseek-v4-flash` |
| `CODE_WIKI_MAX_STEPS` | 最大工具轮次，默认 `20` |
| `CODE_WIKI_GIT_ENABLED` | 是否启用只读 git 工具，默认 `true` |

## 使用

```bash
export DEEPSEEK_API_KEY=sk-...

code-wiki /path/to/repo "登录鉴权是怎么做的？"
code-wiki . "Who implements payment?" -v --max-steps 30
```

## 能力（P0）

- 工具：`list_dir` / `glob` / `grep` / `read_file`（outline/body/symbol）
- 符号：启发式 `find_definition` / `find_references`
- Git：只读白名单 `git_status` / `git_log` / `git_blame` / `git_show` / `git_diff`
- 同轮多个 tool_calls 并行执行

设计细节见 [tech-design.md](./tech-design.md)。

## 开发

```bash
pytest
```
