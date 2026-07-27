---
name: app-structure
description: 描述仓库内 app-client（React + Vite）的目录职责、路由、API 与鉴权约定；改前端或对接后端时优先遵循本文。
---

# app-client 应用结构（Skill）

在修改 `app-client/`、新增页面或 API、或排查前后端联调问题时，先对照本 skill，保持与现有约定一致。

## 技术栈

| 类别 | 选型 |
|------|------|
| 运行时 | React 19、`react-dom` |
| 构建 | Vite 8、`@vitejs/plugin-react` |
| 路由 | `react-router-dom` v6（入口使用 `BrowserRouter`） |
| HTTP | Axios；统一封装在 `src/apis/request.ts` |
| 样式 | 全局 CSS（`index.css`、`App.css`）；页面可用 Less（如 `pages/login/index.less`） |

根目录脚本：`pnpm/npm run dev|build|lint|preview`。生产构建会先 `tsc -b` 再 `vite build`。

## 目录一览（职责）

```
app-client/
├── index.html                 # HTML 入口（Vite）
├── vite.config.ts             # 开发代理 /api → 后端
├── tsconfig*.json             # TS 工程引用配置
├── package.json
└── src/
    ├── main.tsx               # ReactDOM createRoot；包裹 StrictMode + BrowserRouter
    ├── App.tsx                # 顶层 Routes：/、/login、/register、/profile
    ├── index.css              # 全局样式
    ├── App.css                # 首页 / 模板样式
    ├── assets/                # 静态资源（图片、SVG 等）
    ├── layout/
    │   ├── BasicLayout.tsx    # 通用壳（ children 容器 + BasicLayout.css）
    │   └── AuthLayout.tsx     # 登录注册等认证页壳（ + AuthLayout.css）
    ├── components/            # 可复用的公共组件
    ├── pages/
    │   ├── login/index.tsx    # 页面组件 + 同目录样式（如 index.less）
    │   ├── register/
    │   └── profile/
    ├── apis/
    │   ├── request.ts         # Axios 实例、IBaseRes、拦截器、export request()
    │   └── auth.ts            # 认证相关接口（login、fetchProfile 等）
    └── utils/
        └── auth.ts            # localStorage token 读写（键名 token）
```

**约定简述：**

- **页面**：按路由拆在 `src/pages/<name>/`，入口一般为 `index.tsx`；组件可具名导出（如 `Login`）供 `App.tsx` 引用。
- **布局**：需要统一侧栏/顶栏等时用 `BasicLayout`；登录注册类用 `AuthLayout`。
- **接口**：所有后端调用经 `apis/`；底层 HTTP 只用 `request.ts` 暴露的实例与 `request()`，不要在页面里新建 axios 实例（除非有充分理由并文档化）。

## 路由

路由集中在 `src/App.tsx` 的 `<Routes>`：

- `/`：`Home`（当前含 Vite/React 演示内容）
- `/login`：`Login`
- `/register`：`Register`
- `/profile`：`Profile`

新增路由：在 `App.tsx` 增加 `<Route>`，并实现对应 `pages/` 下页面；若需布局，用现有 Layout 包裹页面内容。

## HTTP 与后端约定

- src/apis 目录存放接口
- src/types/apis.ts 存放接口的出入参

### 开发代理

`vite.config.ts` 将 **`/api`** 代理到环境变量 **`VITE_API_URL`**；未设置时默认为 `http://localhost:3000`。前端 Axios `baseURL` 为 **`/api`**，因此浏览器请求形如 `/api/auth/login`，由 Vite 转发到后端根路径下的 `/api`（按你后端实际挂载调整）。

### 响应壳 `IBaseRes<T>`

`request.ts` 约定后端 JSON 形如：

```ts
{ code: string; msg: string; data: T }
```

- HTTP 2xx 且 **`code`** 属于成功集合（当前含 `'0'`、`'200'`、`'00000'`，可按后端在 `BIZ_SUCCESS_CODES` 扩充）视为业务成功。
- 业务失败会抛出 **`BizApiError`**（可与 Axios 错误区分）。
- 页面或 `apis/*.ts` 中取业务数据应使用返回值的 **`data` 字段**（即 envelope 里的 `data`，类型参数 `T`）。

鉴权：`request` 拦截器从 `getAuthToken()` 读取 token，设置 **`Authorization: Bearer <token>`**。

### 新增 API

1. 在 `apis/<domain>.ts` 中编写函数，内部调用 `request<T>(path, options)`。
2. `method` 默认 POST；GET 需显式 `method: 'GET'`。
3. 路径为 **`/api` 之后的相对路径**（例如 `/auth/login`），不要重复写 `/api` 前缀（已由 `baseURL` 承担）。

## 本地鉴权辅助

`src/utils/auth.ts`：`getAuthToken` / `setAuthToken` / `removeAuthToken`，存储键 **`token`**。登录成功后应写入 token；需要登出时清除。

## 样式与静态资源

- 全局：`index.css`、`App.css`。
- 页面级：`pages/<page>/index.less` 或 `.css`，在页面文件中 import。
- 公共图标等：`src/assets/` 或 `public/`（按 Vite 惯例，`public/` 下文件按根路径引用）。

## 修改时的检查清单

1. **路由**：`App.tsx` 是否注册；链接/跳转是否使用 `react-router-dom` 的 `Link` / `useNavigate`。
2. **API**：是否走 `apis/request.ts`；业务错误是否区分 `BizApiError` 与网络错误。
3. **类型**：新业务字段在对应 `apis/*.ts` 的类型里补充，避免在组件里散落 `any`。
4. **环境**：联调后端时确认 `VITE_API_URL` 与后端端口、路径一致。

## 样式规范
1) 使用 less
2) 遵循 BEM 风格
3) 颜色尽量统一抽离为主题色

---

*若后端契约变更（字段名、成功码集合、路径前缀），应同步更新 `request.ts` 中的成功码或 `apis/` 类型，并视情况更新本 skill。*
