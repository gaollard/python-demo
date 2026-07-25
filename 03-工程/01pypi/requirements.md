requirements.txt 一般放在哪里

`requirements.txt` **一般放在项目根目录**（和 `README.md`、`pyproject.toml` 同级）。

例如：

```text
my-project/
├── requirements.txt      ← 这里
├── README.md
├── pyproject.toml        ← 若是库项目
├── src/
│   └── my_pkg/
└── tests/
```

这样别人（或 CI）在仓库根目录执行：

```bash
pip install -r requirements.txt
```

就能找到文件，不必再指定子路径。

补充两点：

| 场景 | 常见做法 |
|---|---|
| 应用 / 脚本项目 | 根目录放 `requirements.txt`（或 `requirements-dev.txt`） |
| 要发布的库 | 依赖写在 `pyproject.toml` 的 `[project.dependencies]`；`requirements.txt` 可选，多用于文档/示例/部署 |

你这份 `doc.md` 里也是这个约定：小项目用根目录的 `requirements.txt`，库项目优先 `pyproject.toml`。