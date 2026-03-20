# Graphiti 知识图谱前端系统

## 项目概述
基于FastAPI + Jinja2模板 + Tailwind CSS构建的现代化知识图谱管理界面，采用金融机构风格的简洁设计。

## 技术栈
- **后端**: FastAPI + Jinja2模板引擎
- **样式**: Tailwind CSS
- **JavaScript**: 原生JS + Fetch API
- **图标**: Heroicons
- **字体**: Inter

## 项目结构
```
src/frontend/
├── static/                    # 静态资源
│   ├── css/                  # 样式文件
│   │   ├── tailwind.css      # Tailwind基础样式
│   │   ├── components.css    # 自定义组件样式
│   │   └── themes.css        # 主题切换样式
│   ├── js/                   # JavaScript文件
│   │   ├── app.js           # 主应用逻辑
│   │   ├── i18n.js          # 国际化支持
│   │   ├── theme.js         # 主题切换
│   │   └── api.js           # API客户端
│   └── images/              # 图片资源
│       ├── logo-company.png # 企业Logo
│       └── logo-project.png # 项目Logo
├── templates/               # Jinja2模板
│   ├── base.html           # 基础布局模板
│   ├── components/         # 可复用组件
│   │   ├── header.html     # 顶部导航
│   │   ├── sidebar.html    # 侧边栏
│   │   ├── footer.html     # 底部
│   │   └── loading.html    # 加载状态
│   ├── pages/              # 页面模板
│   │   ├── dashboard.html  # 首页面板
│   │   ├── add-knowledge.html # 新增知识
│   │   └── search.html     # 知识查询
│   └── errors/             # 错误页面
│       ├── 404.html        # 404错误
│       └── 500.html        # 500错误
├── locales/                # 国际化文件
│   ├── zh-CN.json         # 简体中文
│   └── en-US.json         # 英文（预留）
└── config/                # 配置文件
    └── settings.py        # 前端配置
```

## 功能特性

### 1. 国际化支持
- 默认简体中文
- 支持语言切换
- 所有界面文本集中管理

### 2. 主题切换
- 亮色/暗色主题
- 跟随系统自动切换
- 用户手动切换选项

### 3. 响应式设计
- 桌面端优化布局
- 移动端适配
- 平板端兼容

### 4. 金融机构风格
- 简洁专业的界面
- 清晰的信息层级
- 稳重的色彩搭配

## 快速开始

### 1. 安装依赖
```bash
# 安装Tailwind CSS
npm install -D tailwindcss
npx tailwindcss init

# 安装其他依赖
npm install heroicons
```

### 2. 配置环境
复制 `.env.example` 为 `.env`，配置相关参数：
```env
FRONTEND_LANGUAGE=zh-CN
FRONTEND_THEME=light
FRONTEND_AUTO_THEME=true
```

### 3. 构建样式
```bash
npm run build:css
```

### 4. 启动服务
前端服务集成在FastAPI中，启动后端服务即可：
```bash
uvicorn api.main:app --reload
```

## 开发规范

### 1. 代码规范
- 使用语义化HTML标签
- CSS采用BEM命名规范
- JavaScript使用ES6+语法

### 2. 国际化规范
- 所有用户可见文本使用i18n键名
- 在代码注释中标注原始中文文本
- 语言文件按模块分类

### 3. 组件规范
- 组件文件名单词小写，连字符分隔
- 模板文件使用.html扩展名
- 样式文件按功能模块组织

## API接口

### 新增知识
- **端点**: `POST /api/episodes/text`
- **功能**: 提交文本内容到知识图谱
- **参数**: content, description, name, reference_time

### 知识查询
- **端点**: `GET /api/episodes/search`
- **功能**: 搜索知识图谱中的实体
- **参数**: query, limit

## 部署说明

### 生产环境
1. 构建优化后的CSS文件
2. 配置CDN加速静态资源
3. 设置适当的缓存策略
4. 配置HTTPS安全连接

### 性能优化
- 启用CSS和JS压缩
- 使用图片懒加载
- 实现资源预加载
- 优化字体加载策略