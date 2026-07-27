# 鱼泡论坛 Client

React + Vite 前端，对接 `fastapi-project/server` 论坛 API。

## 功能

- 注册 / 登录（JWT）
- 帖子列表、详情、发帖
- 点赞 / 收藏
- 我的帖子 / 我的收藏

## 开发

```bash
pnpm install
pnpm dev
```

默认通过 Vite 代理将 `/api` 转发到 `http://localhost:8000`（可用环境变量 `VITE_API_URL` 覆盖）。请先启动后端。

## 脚本

| 命令 | 说明 |
|------|------|
| `pnpm dev` | 本地开发 |
| `pnpm build` | 类型检查 + 生产构建 |
| `pnpm preview` | 预览构建产物 |
| `pnpm lint` | ESLint |
