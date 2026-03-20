# Graphiti 前端系统设计文档

## 1. 系统架构

### 1.1 整体架构
```
┌─────────────────────────────────────────────────────────────┐
│                        浏览器层                              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   HTML模板   │  │  CSS样式文件  │  │  JavaScript逻辑   │  │
│  │  (Jinja2)   │  │  (Tailwind)  │  │   (原生JS)       │  │
│  └──────┬──────┘  └──────┬───────┘  └────────┬─────────┘  │
├────────┼────────────────┼──────────────────┼──────────────┤
│        │                │                  │              │
│  ┌─────▼──────┐  ┌──────▼──────┐  ┌───────▼────────┐  │
│  │  国际化系统  │  │  主题系统     │  │   API客户端     │  │
│  │ (i18n.js)  │  │ (theme.js)  │  │   (api.js)     │  │
│  └─────┬──────┘  └──────┬──────┘  └───────┬────────┘  │
├────────┼────────────────┼──────────────────┼──────────────┤
│        │                │                  │              │
│  ┌─────▼──────────────────────────────────────▼────────┐  │
│  │              FastAPI + Jinja2模板引擎                 │  │
│  └─────┬──────────────────────────────────────┬────────┘  │
├────────┼────────────────────────────────────────┼────────────┤
│        │                                        │            │
│  ┌─────▼──────────────────────────────────────▼────────┐  │
│  │              后端API (Graphiti服务)                  │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 技术选型理由

**FastAPI + Jinja2模板**
- 与现有后端技术栈保持一致
- 天然集成，无需额外部署
- 支持服务端渲染，SEO友好
- 模板继承机制，代码复用性高

**Tailwind CSS**
- 原子化CSS，开发效率高
- 金融机构风格设计系统完善
- 响应式设计内置支持
- 主题切换实现简单

**原生JavaScript**
- 无需构建步骤，部署简单
- 与现代浏览器API兼容性好
- 学习成本低，维护简单
- 性能开销最小

## 2. 国际化系统设计

### 2.1 语言文件结构
```json
{
  "common": {
    "loading": "加载中...",
    "error": "出错了",
    "retry": "重试",
    "cancel": "取消",
    "confirm": "确认"
  },
  "navigation": {
    "dashboard": "首页面板",
    "add_knowledge": "新增知识",
    "search": "知识查询",
    "settings": "设置"
  },
  "dashboard": {
    "welcome": "欢迎使用 Graphiti 知识图谱管理系统",
    "subtitle": "智能化知识管理与图谱构建平台",
    "knowledge_graph_preview": "知识图谱预览"
  },
  "add_knowledge": {
    "title": "新增知识",
    "text_input": "文本输入",
    "file_upload": "文件上传",
    "text_placeholder": "请输入要添加到知识图谱的文本内容...",
    "reference_time": "参考时间",
    "reference_time_placeholder": "格式: yyyyMMdd 或 yyyyMM",
    "submit": "提交到知识图谱",
    "file_types": "支持格式: .txt, .md, .csv",
    "max_file_size": "最大文件大小: 10MB"
  },
  "search": {
    "title": "知识查询",
    "placeholder": "输入关键词搜索知识图谱...",
    "search_button": "搜索",
    "no_results": "未找到相关结果",
    "results_count": "找到 {count} 个相关结果",
    "entity_type": "实体类型",
    "relevance_score": "相关度"
  },
  "theme": {
    "light": "亮色主题",
    "dark": "暗色主题",
    "auto": "跟随系统"
  }
}
```

### 2.2 国际化实现机制
```javascript
// i18n.js
class I18n {
    constructor() {
        this.currentLanguage = this.getDefaultLanguage();
        this.translations = {};
        this.loadTranslations();
    }
    
    async loadTranslations() {
        try {
            const response = await fetch(`/static/locales/${this.currentLanguage}.json`);
            this.translations = await response.json();
        } catch (error) {
            console.error('加载语言文件失败:', error);
        }
    }
    
    t(key, params = {}) {
        const keys = key.split('.');
        let value = this.translations;
        
        for (const k of keys) {
            value = value[k];
            if (!value) return key;
        }
        
        // 参数替换
        return value.replace(/\{(\w+)\}/g, (match, param) => params[param] || match);
    }
    
    getDefaultLanguage() {
        // 从环境配置、浏览器语言、本地存储中获取
        return window.FRONTEND_CONFIG?.language || 
               localStorage.getItem('language') || 
               navigator.language || 
               'zh-CN';
    }
}

// 全局i18n实例
window.i18n = new I18n();
```

## 3. 主题系统设计

### 3.1 色彩系统
```css
/* 亮色主题 */
:root {
  --color-primary: #1e40af;
  --color-primary-dark: #1e3a8a;
  --color-secondary: #64748b;
  --color-background: #ffffff;
  --color-surface: #f8fafc;
  --color-text: #1e293b;
  --color-text-secondary: #64748b;
  --color-border: #e2e8f0;
  --color-success: #059669;
  --color-warning: #d97706;
  --color-error: #dc2626;
}

/* 暗色主题 */
[data-theme="dark"] {
  --color-primary: #3b82f6;
  --color-primary-dark: #2563eb;
  --color-secondary: #94a3b8;
  --color-background: #0f172a;
  --color-surface: #1e293b;
  --color-text: #f1f5f9;
  --color-text-secondary: #cbd5e1;
  --color-border: #334155;
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
}
```

### 3.2 主题切换实现
```javascript
// theme.js
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
    
    getInitialTheme() {
        const saved = localStorage.getItem('theme');
        if (saved) return saved;
        
        const config = window.FRONTEND_CONFIG;
        if (config?.theme && config.theme !== 'auto') {
            return config.theme;
        }
        
        return 'light'; // 默认亮色主题
    }
    
    setupAutoTheme() {
        if (!this.autoTheme) return;
        
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        const handleChange = (e) => {
            if (this.getSavedTheme() === 'auto') {
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        };
        
        mediaQuery.addEventListener('change', handleChange);
        handleChange(mediaQuery);
    }
    
    setTheme(theme) {
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);
        this.applyTheme(theme);
    }
    
    applyTheme(theme) {
        const root = document.documentElement;
        
        if (theme === 'dark') {
            root.setAttribute('data-theme', 'dark');
        } else {
            root.removeAttribute('data-theme');
        }
        
        // 触发主题变更事件
        window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
    }
}

// 全局主题管理器
window.themeManager = new ThemeManager();
```

## 4. API客户端设计

### 4.1 API封装
```javascript
// api.js
class ApiClient {
    constructor() {
        this.baseURL = window.FRONTEND_CONFIG?.apiBaseUrl || 'http://localhost:8000';
        this.timeout = window.FRONTEND_CONFIG?.apiTimeout || 30000;
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const controller = new AbortController();
        
        // 设置超时
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        
        try {
            const response = await fetch(url, {
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
            
            if (error.name === 'AbortError') {
                throw new Error('请求超时');
            }
            
            throw error;
        }
    }
    
    // 健康检查
    async healthCheck() {
        return this.request('/health');
    }
    
    // 添加文本情节
    async addTextEpisode(data) {
        return this.request('/api/episodes/text', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    // 搜索实体
    async searchEntities(query, limit = 10) {
        const params = new URLSearchParams({ query, limit: limit.toString() });
        return this.request(`/api/episodes/search?${params}`);
    }
}

// 全局API客户端
window.apiClient = new ApiClient();
```

## 5. 页面组件设计

### 5.1 基础布局
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="{{ language }}" data-theme="{{ theme }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ page_title }}{% endblock %}</title>
    
    <!-- Tailwind CSS -->
    <link href="{{ url_for('static', path='css/tailwind.css') }}" rel="stylesheet">
    <link href="{{ url_for('static', path='css/components.css') }}" rel="stylesheet">
    <link href="{{ url_for('static', path='css/themes.css') }}" rel="stylesheet">
    
    <!-- 配置注入 -->
    <script>
        window.FRONTEND_CONFIG = {{ frontend_config | tojson }};
    </script>
</head>
<body class="bg-background text-text font-sans">
    <!-- 顶部导航 -->
    {% include 'components/header.html' %}
    
    <div class="flex min-h-screen">
        <!-- 侧边栏 -->
        {% include 'components/sidebar.html' %}
        
        <!-- 主内容区 -->
        <main class="flex-1 p-6">
            {% block content %}{% endblock %}
        </main>
    </div>
    
    <!-- 底部 -->
    {% include 'components/footer.html' %}
    
    <!-- 加载状态 -->
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

### 5.2 导航组件
```html
<!-- sidebar.html -->
<nav class="w-64 bg-surface border-r border-border">
    <div class="p-4">
        <div class="space-y-2">
            <a href="/" class="nav-item {% if active_page == 'dashboard' %}active{% endif %}">
                <svg><!-- 首页图标 --></svg>
                <span data-i18n="navigation.dashboard">首页面板</span>
            </a>
            <a href="/add-knowledge" class="nav-item {% if active_page == 'add-knowledge' %}active{% endif %}">
                <svg><!-- 添加图标 --></svg>
                <span data-i18n="navigation.add_knowledge">新增知识</span>
            </a>
            <a href="/search" class="nav-item {% if active_page == 'search' %}active{% endif %}">
                <svg><!-- 搜索图标 --></svg>
                <span data-i18n="navigation.search">知识查询</span>
            </a>
        </div>
    </div>
</nav>
```

## 6. 响应式设计

### 6.1 断点设置
```css
/* 移动端优先的响应式设计 */
/* 默认样式（移动端）*/
.nav-item {
    @apply flex items-center px-3 py-2 text-sm rounded-md;
}

/* 平板端 */
@media (min-width: 768px) {
    .nav-item {
        @apply px-4 py-3 text-base;
    }
}

/* 桌面端 */
@media (min-width: 1024px) {
    .nav-item {
        @apply px-4 py-3 text-base;
    }
}
```

### 6.2 移动端适配
- 侧边栏折叠为汉堡菜单
- 表格横向滚动
- 表单元素自适应宽度
- 触摸友好的按钮大小

## 7. 性能优化策略

### 7.1 资源优化
- CSS文件压缩和合并
- JavaScript文件压缩
- 图片资源WebP格式
- 字体子集化

### 7.2 加载优化
- 关键CSS内联
- JavaScript异步加载
- 资源预加载
- 浏览器缓存

### 7.3 运行时优化
- API请求防抖
- 虚拟滚动（大量数据时）
- 懒加载图片
- 事件委托

## 8. 安全考虑

### 8.1 XSS防护
- 模板自动转义
- 用户输入验证
- CSP策略

### 8.2 CSRF防护
- 同源策略
- 请求头验证

### 8.3 数据安全
- API响应验证
- 敏感信息脱敏
- HTTPS强制使用

## 9. 部署方案

### 9.1 开发环境
```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建生产版本
npm run build
```

### 9.2 生产环境
- 静态文件CDN部署
- Nginx反向代理
- Docker容器化
- 监控和日志

## 10. 维护计划

### 10.1 定期更新
- 依赖库安全更新
- 浏览器兼容性检查
- 性能监控优化

### 10.2 用户反馈
- 错误收集
- 性能指标
- 用户体验改进