# ui-refactor

按 **输入的风格 skill** 重构 `app-client` 页面（Less + BEM、`index.css` 令牌）。

## 用法

在指令中附带风格，例如：`/ui-refactor app-ui-design-black`

- **`app-ui-design-black`** → 对照 `@.cursor/skills/app-ui-design-black.md`：暗色令牌、`html.theme-dark`、边框/次级底分层、弱化阴影、单一 `--accent`。
- 其他风格 → 读取用户 `@` 的对应 skill 后执行。

## 通用步骤

1. 阅读指定的 **风格 skill** 与 `@.cursor/skills/app-structure.md`。
2. 颜色只改 **`src/index.css`** 的 `:root` / `html.theme-dark` / `prefers-color-scheme`，组件内 **`var(--*)`**。
3. 收尾：`lint`，不改无关 API 逻辑。
