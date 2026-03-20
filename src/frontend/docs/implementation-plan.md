# Graphiti 前端系统实现计划

## 项目概述
基于FastAPI + Jinja2模板 + Tailwind CSS构建现代化知识图谱管理界面，采用金融机构风格的简洁设计，支持国际化和主题切换。

## 实施阶段规划

### 第一阶段：基础架构搭建 (优先级：高)

#### 1.1 项目结构创建
```bash
# 创建基础目录结构
mkdir -p src/frontend/{static/{css,js,images},templates/{components,pages,errors},locales,config}

# 创建具体文件结构
touch src/frontend/static/css/{tailwind.css,components.css,themes.css}
touch src/frontend/static/js/{app.js,i18n.js,theme.js,api.js}
touch src/frontend/templates/{base.html,components/{header.html,sidebar.html,footer.html,loading.html}}
touch src/frontend/templates/pages/{dashboard.html,add-knowledge.html,search.html}
touch src/frontend/templates/errors/{404.html,500.html}
touch src/frontend/locales/{zh-CN.json,en-US.json}
```

#### 1.2 FastAPI Jinja2集成
**任务清单：**
- [ ] 安装Jinja2模板引擎依赖
- [ ] 配置模板目录路径
- [ ] 创建模板渲染工具函数
- [ ] 配置静态文件服务
- [ ] 创建基础路由处理器

**实现代码：**
```python
# api/frontend.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

# 配置模板和静态文件
templates = Jinja2Templates(directory="src/frontend/templates")
app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# 基础路由
@app.get("/")
async def dashboard(request: Request):
    return templates.TemplateResponse("pages/dashboard.html", {
        "request": request,
        "page_title": "首页面板 - Graphiti 知识图谱",
        "active_page": "dashboard"
    })
```

#### 1.3 Tailwind CSS配置
**任务清单：**
- [ ] 安装Tailwind CSS依赖
- [ ] 创建tailwind.config.js配置文件
- [ ] 配置金融机构风格色彩系统
- [ ] 创建基础样式文件
- [ ] 设置构建流程

**配置文件：**
```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./src/frontend/templates/**/*.html",
    "./src/frontend/static/js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8'
        },
        secondary: {
          50: '#f8fafc',
          500: '#64748b',
          600: '#475569',
          700: '#334155'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif']
      }
    }
  },
  plugins: []
}
```

### 第二阶段：核心功能开发 (优先级：高)

#### 2.1 国际化系统实现
**任务清单：**
- [ ] 创建i18n.js核心类
- [ ] 实现语言文件加载机制
- [ ] 创建翻译函数和参数替换
- [ ] 实现语言切换功能
- [ ] 创建完整的zh-CN语言文件

**核心代码：**
```javascript
// static/js/i18n.js
class I18n {
    constructor() {
        this.currentLanguage = this.getDefaultLanguage();
        this.translations = {};
        this.loadTranslations();
    }
    
    t(key, params = {}, fallback = null) {
        const keys = key.split('.');
        let value = this.translations;
        
        for (const k of keys) {
            value = value[k];
            if (!value) return fallback || key;
        }
        
        return this.replaceParams(value, params);
    }
    
    replaceParams(text, params) {
        return text.replace(/\{(\w+)\}/g, (match, paramName) => {
            return params.hasOwnProperty(paramName) ? params[paramName] : match;
        });
    }
}
```

#### 2.2 主题系统实现
**任务清单：**
- [ ] 创建theme.js主题管理器
- [ ] 实现亮色/暗色主题CSS变量
- [ ] 创建主题切换UI组件
- [ ] 实现自动主题检测
- [ ] 主题偏好本地存储

**核心代码：**
```javascript
// static/js/theme.js
class ThemeManager {
    constructor() {
        this.currentTheme = this.getInitialTheme();
        this.autoTheme = this.getAutoThemeSetting();
        this.init();
    }
    
    init() {
        this.applyTheme(this.currentTheme);
        this.setupAutoTheme();
    }
    
    applyTheme(theme) {
        const root = document.documentElement;
        if (theme === 'dark') {
            root.setAttribute('data-theme', 'dark');
        } else {
            root.removeAttribute('data-theme');
        }
    }
}
```

#### 2.3 API客户端实现
**任务清单：**
- [ ] 创建api.js API客户端类
- [ ] 实现请求/响应拦截器
- [ ] 错误处理和超时机制
- [ ] 封装具体API方法
- [ ] 加载状态管理

**核心代码：**
```javascript
// static/js/api.js
class ApiClient {
    constructor() {
        this.baseURL = window.FRONTEND_CONFIG?.apiBaseUrl || 'http://localhost:8000';
        this.timeout = window.FRONTEND_CONFIG?.apiTimeout || 30000;
    }
    
    async request(endpoint, options = {}) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                ...options,
                signal: controller.signal,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }
    
    // 具体API方法
    async addTextEpisode(data) {
        return this.request('/api/episodes/text', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    async searchEntities(query, limit = 10) {
        const params = new URLSearchParams({ query, limit: limit.toString() });
        return this.request(`/api/episodes/search?${params}`);
    }
}
```

### 第三阶段：页面组件开发 (优先级：中)

#### 3.1 基础布局组件
**任务清单：**
- [ ] 创建base.html基础模板
- [ ] 实现header.html顶部导航
- [ ] 创建sidebar.html侧边栏
- [ ] 实现footer.html底部信息
- [ ] 创建loading.html加载组件

**base.html模板结构：**
```html
<!DOCTYPE html>
<html lang="{{ language }}" data-theme="{{ theme }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ page_title }}{% endblock %}</title>
    
    <!-- CSS文件 -->
    <link href="{{ url_for('static', path='css/tailwind.css') }}" rel="stylesheet">
    <link href="{{ url_for('static', path='css/components.css') }}" rel="stylesheet">
    <link href="{{ url_for('static', path='css/themes.css') }}" rel="stylesheet">
    
    <!-- 配置注入 -->
    <script>
        window.FRONTEND_CONFIG = {{ frontend_config | tojson }};
    </script>
</head>
<body class="bg-background text-text font-sans">
    {% include 'components/header.html' %}
    
    <div class="flex min-h-screen">
        {% include 'components/sidebar.html' %}
        <main class="flex-1 p-6">
            {% block content %}{% endblock %}
        </main>
    </div>
    
    {% include 'components/footer.html' %}
    {% include 'components/loading.html' %}
    
    <!-- JavaScript文件 -->
    <script src="{{ url_for('static', path='js/i18n.js') }}"></script>
    <script src="{{ url_for('static', path='js/theme.js') }}"></script>
    <script src="{{ url_for('static', path='js/api.js') }}"></script>
    <script src="{{ url_for('static', path='js/app.js') }}"></script>
    
    {% block scripts %}{% endblock %}
</body>
</html>
```

#### 3.2 首页面板实现
**任务清单：**
- [ ] 创建dashboard.html页面模板
- [ ] 实现欢迎信息和系统状态展示
- [ ] 预留知识图谱预览区域
- [ ] 添加最近活动组件
- [ ] 实现响应式布局

**页面功能：**
- 系统欢迎信息
- 知识统计概览
- 图谱预览占位区
- 最近活动列表
- 系统健康状态

#### 3.3 新增知识页面
**任务清单：**
- [ ] 创建add-knowledge.html模板
- [ ] 实现文本输入区域
- [ ] 创建文件上传组件
- [ ] 实现二选一输入逻辑
- [ ] 添加参考时间输入
- [ ] 表单验证和错误提示

**核心功能：**
```javascript
// 二选一输入逻辑
function handleInputMethod(method) {
    const textInput = document.getElementById('text-input-section');
    const fileUpload = document.getElementById('file-upload-section');
    
    if (method === 'text') {
        textInput.classList.remove('hidden');
        fileUpload.classList.add('hidden');
        // 清空文件选择
        document.getElementById('file-input').value = '';
    } else {
        textInput.classList.add('hidden');
        fileUpload.classList.remove('hidden');
        // 清空文本输入
        document.getElementById('text-content').value = '';
    }
}

// 文件读取和处理
function handleFileUpload(file) {
    if (!file) return;
    
    // 验证文件类型和大小
    if (!validateFile(file)) {
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        // 将文件内容设置为表单数据
        document.getElementById('file-content').value = content;
    };
    reader.readAsText(file);
}
```

#### 3.4 知识查询页面
**任务清单：**
- [ ] 创建search.html模板
- [ ] 实现搜索输入框
- [ ] 创建搜索结果展示区域
- [ ] 实现结果分页和排序
- [ ] 添加高级搜索选项

**搜索功能实现：**
```javascript
// 搜索功能
async function performSearch() {
    const query = document.getElementById('search-input').value.trim();
    if (!query) {
        showError(t('search.validation.query_required'));
        return;
    }
    
    showLoading(true);
    
    try {
        const results = await apiClient.searchEntities(query, currentLimit);
        displaySearchResults(results);
    } catch (error) {
        showError(t('search.error'), error.message);
    } finally {
        showLoading(false);
    }
}

// 结果展示
function displaySearchResults(results) {
    const container = document.getElementById('search-results');
    
    if (!results.data || results.data.length === 0) {
        container.innerHTML = `
            <div class="text-center py-8">
                <p class="text-text-secondary">${t('search.no_results')}</p>
            </div>
        `;
        return;
    }
    
    const resultsHtml = results.data.map(result => `
        <div class="result-item p-4 border border-border rounded-lg mb-4">
            <h3 class="text-lg font-semibold mb-2">${result.name}</h3>
            <p class="text-text-secondary mb-2">${result.summary || ''}</p>
            <div class="flex items-center gap-4 text-sm">
                <span class="text-secondary">${t('search.entity_type')}: ${t(`entity_types.${result.entity_type}`)}</span>
                <span class="text-secondary">${t('search.relevance_score')}: ${(result.relevance_score * 100).toFixed(1)}%</span>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = resultsHtml;
}
```

### 第四阶段：样式和交互优化 (优先级：中)

#### 4.1 Tailwind CSS集成
**任务清单：**
- [ ] 配置Tailwind CSS构建流程
- [ ] 创建金融机构风格色彩系统
- [ ] 实现响应式断点配置
- [ ] 创建自定义组件样式
- [ ] 优化字体和排版

**色彩系统设计：**
```css
/* 金融机构专业色彩 */
:root {
  --color-primary: #1e40af;        /* 主色调 - 深蓝 */
  --color-primary-dark: #1e3a8a;   /* 深色主调 */
  --color-secondary: #64748b;      /* 辅助色 - 灰蓝 */
  --color-success: #059669;        /* 成功色 - 深绿 */
  --color-warning: #d97706;        /* 警告色 - 深橙 */
  --color-error: #dc2626;          /* 错误色 - 深红 */
  --color-background: #ffffff;     /* 背景色 */
  --color-surface: #f8fafc;        /* 表面色 */
  --color-text: #1e293b;           /* 文本色 */
  --color-border: #e2e8f0;         /* 边框色 */
}

[data-theme="dark"] {
  --color-primary: #3b82f6;        /* 暗色主题主调 */
  --color-background: #0f172a;     /* 暗色背景 */
  --color-surface: #1e293b;        /* 暗色表面 */
  --color-text: #f1f5f9;           /* 暗色文本 */
  --color-border: #334155;         /* 暗色边框 */
}
```

#### 4.2 响应式设计
**任务清单：**
- [ ] 实现移动端导航折叠
- [ ] 优化表单元素触摸体验
- [ ] 创建自适应表格布局
- [ ] 实现图片懒加载
- [ ] 优化加载性能

**响应式断点：**
```css
/* 移动端优先的响应式设计 */
/* 默认样式（移动端 < 768px）*/
.sidebar {
  @apply fixed inset-y-0 left-0 z-50 w-64 transform -translate-x-full;
}

/* 平板端（≥768px）*/
@media (min-width: 768px) {
  .sidebar {
    @apply relative transform-none;
  }
}

/* 桌面端（≥1024px）*/
@media (min-width: 1024px) {
  .sidebar {
    @apply w-64;
  }
}
```

#### 4.3 交互体验优化
**任务清单：**
- [ ] 实现平滑过渡动画
- [ ] 添加加载状态指示器
- [ ] 创建错误提示组件
- [ ] 实现表单验证反馈
- [ ] 添加键盘快捷键支持

### 第五阶段：测试和部署 (优先级：低)

#### 5.1 功能测试
**任务清单：**
- [ ] 单元测试JavaScript模块
- [ ] 集成测试API调用
- [ ] 端到端测试用户流程
- [ ] 跨浏览器兼容性测试
- [ ] 移动端适配测试

#### 5.2 性能优化
**任务清单：**
- [ ] CSS和JS文件压缩
- [ ] 图片资源优化
- [ ] 启用浏览器缓存
- [ ] 实现资源预加载
- [ ] 性能监控埋点

#### 5.3 部署配置
**任务清单：**
- [ ] 创建生产环境配置
- [ ] 配置Nginx反向代理
- [ ] 设置HTTPS证书
- [ ] 配置错误监控
- [ ] 创建部署文档

## 开发环境配置

### 1. 依赖安装
```bash
# 安装Python依赖
pip install jinja2 python-dotenv

# 安装Node.js依赖（用于Tailwind CSS）
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

### 2. 环境变量配置
```bash
# .env 文件
FRONTEND_LANGUAGE=zh-CN
FRONTEND_THEME=light
FRONTEND_AUTO_THEME=true
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30000
MAX_FILE_SIZE=10485760
```

### 3. 构建脚本
```json
// package.json
{
  "scripts": {
    "build:css": "tailwindcss -i ./src/frontend/static/css/input.css -o ./src/frontend/static/css/tailwind.css --watch",
    "build:prod": "tailwindcss -i ./src/frontend/static/css/input.css -o ./src/frontend/static/css/tailwind.css --minify"
  }
}
```

## 质量保障

### 1. 代码规范
- 使用语义化HTML标签
- CSS采用BEM命名规范
- JavaScript使用ES6+语法
- 添加必要的代码注释

### 2. 可访问性
- 支持键盘导航
- 提供ARIA标签
- 确保色彩对比度
- 支持屏幕阅读器

### 3. 性能标准
- 首屏加载时间 < 3秒
- 交互响应时间 < 100ms
- 支持离线缓存
- 移动端流量优化

## 风险评估与应对

### 技术风险
1. **浏览器兼容性**：使用Polyfill和渐进增强
2. **性能瓶颈**：代码分割和懒加载
3. **安全漏洞**：输入验证和XSS防护

### 项目风险
1. **进度延误**：分阶段交付，优先核心功能
2. **需求变更**：保持代码模块化，便于调整
3. **人员变动**：完善文档和代码注释

## 交付物清单

### 1. 代码交付
- [ ] 完整的前端源代码
- [ ] 配置文件和构建脚本
- [ ] 测试用例和测试报告
- [ ] 部署脚本和配置

### 2. 文档交付
- [ ] 系统架构设计文档
- [ ] API接口使用说明
- [ ] 部署和运维手册
- [ ] 用户操作手册

### 3. 培训交付
- [ ] 开发团队技术培训
- [ ] 运维团队部署培训
- [ ] 用户使用培训材料

## 时间规划

建议采用敏捷开发方式，分5个迭代完成：

1. **迭代1** (1周)：基础架构和工具配置
2. **迭代2** (1周)：核心功能开发
3. **迭代3** (1周)：页面组件和样式
4. **迭代4** (1周)：交互优化和测试
5. **迭代5** (3天)：部署和文档完善

每个迭代结束都有可演示的交付物，确保项目进度可控。