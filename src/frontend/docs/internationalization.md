# 国际化(i18n)系统设计文档

## 概述
本系统采用集中式的国际化方案，所有用户可见的文本都通过统一的翻译系统进行管理，支持多语言切换和动态加载。

## 语言文件结构

### 文件组织
```
src/frontend/locales/
├── zh-CN.json      # 简体中文（默认）
├── en-US.json      # 英文（预留）
└── ja-JP.json      # 日文（预留）
```

### 语言文件格式
每个语言文件都是一个JSON对象，按照功能模块进行分层组织：

```json
{
  "模块名": {
    "键名": "翻译文本",
    "嵌套键": {
      "子键": "翻译文本"
    }
  }
}
```

## 翻译键命名规范

### 1. 模块划分
- `common`: 通用组件和常用词汇
- `navigation`: 导航相关
- `header`: 顶部标题栏
- `dashboard`: 首页面板
- `add_knowledge`: 新增知识页面
- `search`: 知识查询页面
- `settings`: 设置页面
- `errors`: 错误信息
- `footer`: 底部信息
- `entity_types`: 实体类型翻译

### 2. 键名规则
- 使用小写字母和下划线分隔
- 保持语义清晰，避免缩写
- 同类内容保持命名一致性
- 动态内容使用占位符 `{placeholder}`

### 3. 示例键名
```json
{
  "common": {
    "loading": "加载中...",
    "error": "出错了",
    "submit": "提交"
  },
  "dashboard": {
    "welcome": "欢迎使用 {system_name}",
    "no_data": "暂无{data_type}数据"
  }
}
```

## 完整中文语言文件内容

### common 模块 - 通用词汇
```json
{
  "common": {
    "loading": "加载中...",
    "error": "出错了",
    "retry": "重试",
    "cancel": "取消",
    "confirm": "确认",
    "save": "保存",
    "delete": "删除",
    "edit": "编辑",
    "view": "查看",
    "close": "关闭",
    "back": "返回",
    "next": "下一步",
    "previous": "上一步",
    "submit": "提交",
    "reset": "重置",
    "search": "搜索",
    "clear": "清空",
    "refresh": "刷新",
    "download": "下载",
    "upload": "上传",
    "yes": "是",
    "no": "否",
    "ok": "确定",
    "warning": "警告",
    "info": "信息",
    "success": "成功",
    "failed": "失败",
    "timeout": "请求超时，请稍后重试",
    "network_error": "网络连接错误，请检查网络设置",
    "server_error": "服务器错误，请联系技术支持"
  }
}
```

### navigation 模块 - 导航菜单
```json
{
  "navigation": {
    "dashboard": "首页面板",
    "add_knowledge": "新增知识",
    "search": "知识查询",
    "settings": "设置",
    "help": "帮助",
    "about": "关于",
    "logout": "退出登录"
  }
}
```

### header 模块 - 顶部标题栏
```json
{
  "header": {
    "company_logo_alt": "企业Logo",
    "project_logo_alt": "项目Logo",
    "toggle_sidebar": "切换侧边栏",
    "theme_switch": "主题切换",
    "language_switch": "语言切换",
    "user_menu": "用户菜单"
  }
}
```

### dashboard 模块 - 首页面板
```json
{
  "dashboard": {
    "title": "首页面板",
    "welcome": "欢迎使用 Graphiti 知识图谱管理系统",
    "subtitle": "智能化知识管理与图谱构建平台",
    "knowledge_graph_preview": "知识图谱预览",
    "recent_activities": "最近活动",
    "system_status": "系统状态",
    "total_knowledge": "知识总量",
    "today_added": "今日新增",
    "search_count": "查询次数",
    "system_health": "系统健康度",
    "view_full_graph": "查看完整图谱",
    "no_graph_data": "暂无图谱数据，请先添加知识内容"
  }
}
```

### add_knowledge 模块 - 新增知识
```json
{
  "add_knowledge": {
    "title": "新增知识",
    "subtitle": "将新的知识内容添加到图谱中",
    "input_method": "输入方式",
    "text_input": "文本输入",
    "file_upload": "文件上传",
    "text_content": "文本内容",
    "text_placeholder": "请输入要添加到知识图谱的文本内容，支持长文本输入...",
    "text_description": "描述信息（可选）",
    "text_description_placeholder": "为这段知识内容添加简要描述",
    "reference_time": "参考时间",
    "reference_time_placeholder": "格式: yyyyMMdd 或 yyyyMM",
    "reference_time_help": "指定知识内容的时间参考点，不填写则使用当前时间",
    "file_select": "选择文件",
    "file_drag_drop": "或将文件拖拽到此处",
    "file_types": "支持格式: .txt, .md, .csv",
    "max_file_size": "最大文件大小: 10MB",
    "file_reading": "正在读取文件内容...",
    "file_read_success": "文件读取成功",
    "file_read_error": "文件读取失败，请检查文件格式",
    "submit_button": "提交到知识图谱",
    "submitting": "正在提交...",
    "submit_success": "知识添加成功",
    "submit_error": "知识添加失败，请稍后重试",
    "validation": {
      "content_required": "文本内容不能为空",
      "file_required": "请选择一个文件",
      "file_too_large": "文件大小超过限制（最大10MB）",
      "file_type_invalid": "不支持的文件格式",
      "reference_time_invalid": "参考时间格式不正确，请使用 yyyyMMdd 或 yyyyMM 格式"
    }
  }
}
```

### search 模块 - 知识查询
```json
{
  "search": {
    "title": "知识查询",
    "subtitle": "在知识图谱中搜索相关信息",
    "search_input": "搜索关键词",
    "search_placeholder": "输入关键词搜索知识图谱，支持实体名称、关系类型等...",
    "search_button": "搜索",
    "searching": "搜索中...",
    "advanced_search": "高级搜索",
    "search_filters": "搜索筛选",
    "result_limit": "结果数量",
    "result_limit_placeholder": "每页显示结果数量",
    "entity_type": "实体类型",
    "all_types": "全部类型",
    "sort_by": "排序方式",
    "sort_relevance": "相关度",
    "sort_time": "时间",
    "sort_name": "名称",
    "no_results": "未找到相关结果",
    "results_count": "找到 {count} 个相关结果",
    "results_total": "共 {total} 个结果",
    "showing_results": "显示第 {start} - {end} 条结果",
    "entity_info": "实体信息",
    "entity_type": "实体类型",
    "relevance_score": "相关度",
    "confidence_score": "置信度",
    "properties": "属性",
    "relationships": "关系",
    "view_details": "查看详情",
    "export_results": "导出结果",
    "clear_search": "清空搜索",
    "search_tips": "搜索提示：可以尝试输入人名、公司名、职位、技能等关键词"
  }
}
```

### entity_types 模块 - 实体类型翻译
```json
{
  "entity_types": {
    "PERSON": "人员",
    "COMPANY": "公司",
    "ORGANIZATION": "组织",
    "POSITION": "职位",
    "SKILL": "技能",
    "PROJECT": "项目",
    "PRODUCT": "产品",
    "LOCATION": "地点",
    "EVENT": "事件",
    "WORKS_AS": "职位关系",
    "HAS_ROLE": "角色关系",
    "SPECIALIZES_IN": "专业关系",
    "RESPONSIBLE_FOR": "责任关系",
    "WORKS_AT": "工作地点关系"
  }
}
```

### settings 模块 - 系统设置
```json
{
  "settings": {
    "title": "系统设置",
    "general": "常规设置",
    "appearance": "外观设置",
    "language": "语言设置",
    "theme": "主题设置",
    "language_select": "选择语言",
    "theme_select": "选择主题",
    "theme_light": "亮色主题",
    "theme_dark": "暗色主题",
    "theme_auto": "跟随系统",
    "auto_theme_switch": "自动切换主题",
    "auto_theme_description": "根据系统设置自动切换亮色/暗色主题",
    "save_settings": "保存设置",
    "settings_saved": "设置已保存",
    "reset_settings": "重置为默认值"
  }
}
```

### errors 模块 - 错误信息
```json
{
  "errors": {
    "404": {
      "title": "页面未找到",
      "message": "抱歉，您访问的页面不存在",
      "back_home": "返回首页"
    },
    "500": {
      "title": "服务器错误",
      "message": "服务器遇到了错误，请稍后重试",
      "contact_support": "联系技术支持"
    },
    "generic": {
      "title": "出错了",
      "message": "发生了意外错误，请稍后重试",
      "retry": "重试"
    }
  }
}
```

### footer 模块 - 底部信息
```json
{
  "footer": {
    "copyright": "© 2024 {company_name}. 保留所有权利。",
    "version": "版本 {version}",
    "build_time": "构建时间: {build_time}",
    "links": {
      "privacy": "隐私政策",
      "terms": "使用条款",
      "support": "技术支持",
      "documentation": "文档中心"
    }
  }
}
```

## JavaScript国际化实现

### i18n.js 核心实现
```javascript
/**
 * 国际化系统核心类
 * 负责语言文件加载、翻译键解析和参数替换
 */
class I18n {
    constructor() {
        this.currentLanguage = this.getDefaultLanguage();
        this.translations = {};
        this.fallbackLanguage = 'zh-CN';
        this.loadTranslations();
    }
    
    /**
     * 获取默认语言设置
     * 优先级：配置 > 本地存储 > 浏览器语言 > 默认值
     */
    getDefaultLanguage() {
        // 从全局配置获取
        if (window.FRONTEND_CONFIG?.language) {
            return window.FRONTEND_CONFIG.language;
        }
        
        // 从本地存储获取
        const saved = localStorage.getItem('language');
        if (saved) {
            return saved;
        }
        
        // 从浏览器语言获取
        const browserLang = navigator.language;
        if (browserLang) {
            // 转换为我们的语言代码格式
            if (browserLang.startsWith('zh')) {
                return 'zh-CN';
            } else if (browserLang.startsWith('en')) {
                return 'en-US';
            }
        }
        
        return this.fallbackLanguage;
    }
    
    /**
     * 异步加载翻译文件
     */
    async loadTranslations() {
        try {
            const response = await fetch(`/static/locales/${this.currentLanguage}.json`);
            
            if (!response.ok) {
                throw new Error(`语言文件加载失败: ${response.status}`);
            }
            
            this.translations = await response.json();
            
            // 触发语言变更事件
            window.dispatchEvent(new CustomEvent('languagechange', {
                detail: { language: this.currentLanguage }
            }));
            
        } catch (error) {
            console.error('加载语言文件失败:', error);
            
            // 如果当前语言加载失败，尝试回退语言
            if (this.currentLanguage !== this.fallbackLanguage) {
                this.currentLanguage = this.fallbackLanguage;
                await this.loadTranslations();
            }
        }
    }
    
    /**
     * 翻译函数
     * @param {string} key - 翻译键，支持点分隔的嵌套路径
     * @param {Object} params - 参数对象，用于替换模板中的占位符
     * @param {string} fallback - 回退文本，当翻译键不存在时使用
     * @returns {string} 翻译后的文本
     */
    t(key, params = {}, fallback = null) {
        if (!key) return '';
        
        const keys = key.split('.');
        let value = this.translations;
        
        // 遍历嵌套键路径
        for (const k of keys) {
            if (value && typeof value === 'object' && k in value) {
                value = value[k];
            } else {
                // 如果键不存在，返回回退文本或原始键
                console.warn(`翻译键不存在: ${key}`);
                return fallback || key;
            }
        }
        
        // 确保返回值是字符串
        if (typeof value !== 'string') {
            console.warn(`翻译键对应的值不是字符串: ${key}`);
            return fallback || key;
        }
        
        // 参数替换
        return this.replaceParams(value, params);
    }
    
    /**
     * 替换模板参数
     * @param {string} text - 模板文本
     * @param {Object} params - 参数对象
     * @returns {string} 替换后的文本
     */
    replaceParams(text, params) {
        return text.replace(/\{(\w+)\}/g, (match, paramName) => {
            return params.hasOwnProperty(paramName) ? params[paramName] : match;
        });
    }
    
    /**
     * 切换语言
     * @param {string} language - 新语言代码
     */
    async setLanguage(language) {
        if (language === this.currentLanguage) return;
        
        this.currentLanguage = language;
        localStorage.setItem('language', language);
        
        await this.loadTranslations();
        
        // 重新渲染页面上的所有翻译元素
        this.refreshTranslations();
    }
    
    /**
     * 刷新页面上的翻译元素
     */
    refreshTranslations() {
        // 刷新所有带有 data-i18n 属性的元素
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const params = this.parseParams(element.getAttribute('data-i18n-params'));
            element.textContent = this.t(key, params);
        });
        
        // 刷新所有带有 data-i18n-placeholder 属性的输入元素
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            element.placeholder = this.t(key);
        });
    }
    
    /**
     * 解析参数字符串
     * @param {string} paramString - JSON格式的参数字符串
     * @returns {Object} 参数对象
     */
    parseParams(paramString) {
        if (!paramString) return {};
        
        try {
            return JSON.parse(paramString);
        } catch (error) {
            console.warn('解析i18n参数失败:', error);
            return {};
        }
    }
}

// 创建全局i18n实例
window.i18n = new I18n();

/**
 * 便捷的翻译函数
 * 全局可用的翻译快捷方式
 */
window.t = function(key, params, fallback) {
    return window.i18n.t(key, params, fallback);
};
```

## HTML中的使用方式

### 1. 静态翻译
```html
<!-- 使用 data-i18n 属性 -->
<h1 data-i18n="dashboard.welcome">欢迎使用 Graphiti 知识图谱管理系统</h1>

<!-- 使用 data-i18n-placeholder 属性 -->
<input type="text" data-i18n-placeholder="search.search_placeholder" 
       placeholder="输入关键词搜索知识图谱...">

<!-- 带参数的翻译 -->
<span data-i18n="search.results_count" data-i18n-params='{"count": 5}'>
  找到 5 个相关结果
</span>
```

### 2. JavaScript中的使用
```javascript
// 简单翻译
const title = i18n.t('dashboard.title');

// 带参数的翻译
const message = i18n.t('search.results_count', { count: resultCount });

// 使用全局快捷函数
const buttonText = t('common.submit');

// 错误信息翻译
const errorMessage = i18n.t(`errors.${errorCode}.message`, {}, '未知错误');
```

## 开发规范

### 1. 添加新翻译
1. 在相应的语言文件中添加键值对
2. 确保所有语言文件都包含相同的键结构
3. 使用有意义的键名，避免过于简单

### 2. 参数使用
- 使用花括号 `{param}` 表示参数
- 参数名使用小写字母和下划线
- 在代码中提供对应的参数对象

### 3. 代码注释
在HTML模板中使用翻译时，添加中文注释说明原始文本：
```html
<!-- 原文：欢迎使用 Graphiti 知识图谱管理系统 -->
<h1 data-i18n="dashboard.welcome"></h1>
```

## 测试建议

### 1. 完整性测试
- 检查所有翻译键是否都有对应的翻译
- 验证参数替换是否正确
- 测试回退机制是否正常工作

### 2. 语言切换测试
- 测试动态语言切换功能
- 验证页面刷新后语言设置是否保持
- 检查浏览器语言检测功能

### 3. 边界情况测试
- 测试翻译键不存在的情况
- 验证参数缺失时的表现
- 测试网络错误时的回退行为