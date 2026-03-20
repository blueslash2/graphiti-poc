/**
 * 主题管理系统
 * 负责主题切换、自动主题检测和本地存储
 */
class ThemeManager {
    constructor() {
        this.currentTheme = this.getInitialTheme();
        this.autoTheme = this.getAutoThemeSetting();
        this.init();
    }
    
    /**
     * 初始化主题系统
     */
    init() {
        this.applyTheme(this.currentTheme);
        this.setupAutoTheme();
        this.bindEvents();
    }
    
    /**
     * 获取初始主题设置
     */
    getInitialTheme() {
        const saved = localStorage.getItem('theme');
        if (saved) return saved;
        
        const config = window.FRONTEND_CONFIG;
        if (config?.theme && config.theme !== 'auto') {
            return config.theme;
        }
        
        return 'light'; // 默认亮色主题
    }
    
    /**
     * 获取自动主题设置
     */
    getAutoThemeSetting() {
        const config = window.FRONTEND_CONFIG;
        return config?.auto_theme !== false; // 默认启用
    }
    
    /**
     * 设置自动主题监听
     */
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
    
    /**
     * 绑定事件监听器
     */
    bindEvents() {
        // 监听主题切换按钮点击
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-theme-toggle]')) {
                this.toggleTheme();
            }
        });
        
        // 监听主题选择器变化
        document.addEventListener('change', (e) => {
            if (e.target.matches('[data-theme-selector]')) {
                this.setTheme(e.target.value);
            }
        });
    }
    
    /**
     * 切换主题
     */
    toggleTheme() {
        const themes = ['light', 'dark', 'auto'];
        const currentIndex = themes.indexOf(this.currentTheme);
        const nextTheme = themes[(currentIndex + 1) % themes.length];
        this.setTheme(nextTheme);
    }
    
    /**
     * 设置主题
     * @param {string} theme - 主题名称 (light, dark, auto)
     */
    setTheme(theme) {
        if (theme === this.currentTheme) return;
        
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);
        
        if (theme === 'auto') {
            // 如果是自动模式，根据系统设置应用主题
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            this.applyTheme(mediaQuery.matches ? 'dark' : 'light');
        } else {
            this.applyTheme(theme);
        }
        
        // 更新UI状态
        this.updateUIState();
        
        // 触发自定义事件
        window.dispatchEvent(new CustomEvent('themechange', { 
            detail: { theme: this.currentTheme } 
        }));
    }
    
    /**
     * 应用主题到DOM
     * @param {string} theme - 实际应用的主题 (light, dark)
     */
    applyTheme(theme) {
        const root = document.documentElement;
        
        if (theme === 'dark') {
            root.setAttribute('data-theme', 'dark');
        } else {
            root.removeAttribute('data-theme');
        }
        
        // 更新body的类名
        document.body.className = document.body.className.replace(/theme-\w+/g, '');
        document.body.classList.add(`theme-${theme}`);
    }
    
    /**
     * 更新UI状态
     */
    updateUIState() {
        // 更新主题选择器
        const selectors = document.querySelectorAll('[data-theme-selector]');
        selectors.forEach(selector => {
            if (selector.value !== undefined) {
                selector.value = this.currentTheme;
            }
        });
        
        // 更新主题切换按钮文本
        const toggles = document.querySelectorAll('[data-theme-toggle]');
        toggles.forEach(toggle => {
            const themeText = this.getThemeDisplayName(this.currentTheme);
            if (toggle.tagName === 'BUTTON') {
                toggle.textContent = themeText;
            } else {
                toggle.setAttribute('title', themeText);
            }
        });
        
        // 更新活动主题指示器
        const indicators = document.querySelectorAll('[data-theme-indicator]');
        indicators.forEach(indicator => {
            indicator.textContent = this.getThemeDisplayName(this.currentTheme);
        });
    }
    
    /**
     * 获取主题的显示名称
     * @param {string} theme - 主题名称
     * @returns {string} 显示名称
     */
    getThemeDisplayName(theme) {
        const names = {
            'light': '亮色主题',
            'dark': '暗色主题',
            'auto': '跟随系统'
        };
        return names[theme] || theme;
    }
    
    /**
     * 获取保存的主题设置
     */
    getSavedTheme() {
        return localStorage.getItem('theme') || 'light';
    }
    
    /**
     * 获取当前主题
     */
    getCurrentTheme() {
        return this.currentTheme;
    }
    
    /**
     * 检查是否为暗色主题
     */
    isDarkTheme() {
        if (this.currentTheme === 'auto') {
            return window.matchMedia('(prefers-color-scheme: dark)').matches;
        }
        return this.currentTheme === 'dark';
    }
    
    /**
     * 销毁主题管理器
     */
    destroy() {
        // 清理事件监听器
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        mediaQuery.removeEventListener('change', this.handleThemeChange);
    }
}

// 创建全局主题管理器实例
window.themeManager = new ThemeManager();

/**
 * 便捷的主题检查函数
 */
window.isDarkTheme = function() {
    return window.themeManager.isDarkTheme();
};

/**
 * 获取当前主题
 */
window.getCurrentTheme = function() {
    return window.themeManager.getCurrentTheme();
};