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