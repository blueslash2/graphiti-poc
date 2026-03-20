/**
 * 主应用逻辑
 * 负责页面初始化、事件绑定和全局功能
 */

class App {
    constructor() {
        this.currentPage = null;
        this.loadingCount = 0;
        this.init();
    }
    
    /**
     * 初始化应用
     */
    init() {
        this.bindGlobalEvents();
        this.setupNavigation();
        this.setupLoadingIndicator();
        this.setupErrorHandling();
        this.initializeCurrentPage();
        
        console.log('Graphiti前端系统初始化完成');
    }
    
    /**
     * 绑定全局事件
     */
    bindGlobalEvents() {
        // 监听语言切换
        window.addEventListener('languagechange', (e) => {
            console.log('语言已切换至:', e.detail.language);
            this.onLanguageChange(e.detail.language);
        });
        
        // 监听主题切换
        window.addEventListener('themechange', (e) => {
            console.log('主题已切换至:', e.detail.theme);
            this.onThemeChange(e.detail.theme);
        });
        
        // 监听页面加载
        window.addEventListener('load', () => {
            this.onPageLoad();
        });
        
        // 监听页面可见性变化
        document.addEventListener('visibilitychange', () => {
            this.onVisibilityChange();
        });
    }
    
    /**
     * 设置导航功能
     */
    setupNavigation() {
        // 侧边栏切换
        const sidebarToggle = document.querySelector('[data-sidebar-toggle]');
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => {
                this.toggleSidebar();
            });
        }
        
        // 导航链接点击
        document.addEventListener('click', (e) => {
            const navLink = e.target.closest('[data-nav-link]');
            if (navLink) {
                e.preventDefault();
                const page = navLink.getAttribute('data-nav-link');
                this.navigateToPage(page);
            }
        });
        
        // 浏览器后退/前进
        window.addEventListener('popstate', (e) => {
            this.handlePopState(e);
        });
    }
    
    /**
     * 设置加载指示器
     */
    setupLoadingIndicator() {
        // 监听API请求开始
        document.addEventListener('apiRequestStart', () => {
            this.showLoading();
        });
        
        // 监听API请求结束
        document.addEventListener('apiRequestEnd', () => {
            this.hideLoading();
        });
    }
    
    /**
     * 设置错误处理
     */
    setupErrorHandling() {
        // 全局错误处理
        window.addEventListener('error', (e) => {
            console.error('全局错误:', e.error);
            this.handleError(e.error);
        });
        
        // Promise拒绝处理
        window.addEventListener('unhandledrejection', (e) => {
            console.error('未处理的Promise拒绝:', e.reason);
            this.handleError(e.reason);
        });
        
        // API错误处理
        window.addEventListener('apiError', (e) => {
            this.handleApiError(e.detail);
        });
    }
    
    /**
     * 初始化当前页面
     */
    initializeCurrentPage() {
        const currentPath = window.location.pathname;
        let page = 'dashboard';
        
        if (currentPath.includes('add-knowledge')) {
            page = 'add-knowledge';
        } else if (currentPath.includes('search')) {
            page = 'search';
        }
        
        this.currentPage = page;
        this.updateActiveNavigation();
        this.initializePageSpecificLogic(page);
    }
    
    /**
     * 初始化页面特定逻辑
     */
    initializePageSpecificLogic(page) {
        switch (page) {
            case 'dashboard':
                this.initDashboardPage();
                break;
            case 'add-knowledge':
                this.initAddKnowledgePage();
                break;
            case 'search':
                this.initSearchPage();
                break;
        }
    }
    
    /**
     * 初始化首页面板
     */
    initDashboardPage() {
        console.log('初始化首页面板');
        
        // 系统健康检查
        this.checkSystemHealth();
        
        // 加载统计数据
        this.loadDashboardStats();
    }
    
    /**
     * 初始化新增知识页面
     */
    initAddKnowledgePage() {
        console.log('初始化新增知识页面');
        
        // 绑定输入方式切换
        this.bindInputMethodToggle();
        
        // 绑定文件上传
        this.bindFileUpload();
        
        // 绑定表单提交
        this.bindKnowledgeForm();
    }
    
    /**
     * 初始化搜索页面
     */
    initSearchPage() {
        console.log('初始化搜索页面');
        
        // 绑定搜索表单
        this.bindSearchForm();
        
        // 绑定高级搜索
        this.bindAdvancedSearch();
    }
    
    /**
     * 绑定输入方式切换
     */
    bindInputMethodToggle() {
        const textRadio = document.getElementById('input-method-text');
        const fileRadio = document.getElementById('input-method-file');
        
        if (textRadio && fileRadio) {
            const toggleMethod = () => {
                const textSection = document.getElementById('text-input-section');
                const fileSection = document.getElementById('file-upload-section');
                
                if (textRadio.checked) {
                    textSection.classList.remove('hidden');
                    fileSection.classList.add('hidden');
                    // 清空文件选择
                    document.getElementById('file-input').value = '';
                } else {
                    textSection.classList.add('hidden');
                    fileSection.classList.remove('hidden');
                    // 清空文本输入
                    document.getElementById('text-content').value = '';
                }
            };
            
            textRadio.addEventListener('change', toggleMethod);
            fileRadio.addEventListener('change', toggleMethod);
        }
    }
    
    /**
     * 绑定文件上传
     */
    bindFileUpload() {
        const fileInput = document.getElementById('file-input');
        const fileDropZone = document.getElementById('file-drop-zone');
        
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    this.handleFileUpload(file);
                }
            });
        }
        
        if (fileDropZone) {
            // 拖拽上传
            fileDropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                fileDropZone.classList.add('drag-over');
            });
            
            fileDropZone.addEventListener('dragleave', () => {
                fileDropZone.classList.remove('drag-over');
            });
            
            fileDropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                fileDropZone.classList.remove('drag-over');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.handleFileUpload(files[0]);
                }
            });
        }
    }
    
    /**
     * 处理文件上传
     */
    async handleFileUpload(file) {
        // 验证文件
        if (!this.validateFile(file)) {
            return;
        }
        
        this.showLoading();
        
        try {
            const content = await this.readFileContent(file);
            
            // 将文件内容填入隐藏字段
            const fileContentField = document.getElementById('file-content');
            if (fileContentField) {
                fileContentField.value = content;
            }
            
            // 显示文件名
            const fileNameDisplay = document.getElementById('selected-file-name');
            if (fileNameDisplay) {
                fileNameDisplay.textContent = file.name;
            }
            
            this.showSuccess('文件读取成功');
            
        } catch (error) {
            console.error('文件读取失败:', error);
            this.showError('文件读取失败，请检查文件格式');
        } finally {
            this.hideLoading();
        }
    }
    
    /**
     * 验证文件
     */
    validateFile(file) {
        const maxSize = 10 * 1024 * 1024; // 10MB
        const allowedTypes = ['text/plain', 'text/markdown', 'text/csv'];
        
        if (file.size > maxSize) {
            this.showError('文件大小超过限制（最大10MB）');
            return false;
        }
        
        if (!allowedTypes.includes(file.type)) {
            this.showError('不支持的文件格式');
            return false;
        }
        
        return true;
    }
    
    /**
     * 读取文件内容
     */
    readFileContent(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = () => reject(new Error('文件读取失败'));
            reader.readAsText(file);
        });
    }
    
    /**
     * 绑定知识表单提交
     */
    bindKnowledgeForm() {
        const form = document.getElementById('add-knowledge-form');
        if (!form) return;
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.submitKnowledgeForm(form);
        });
    }
    
    /**
     * 提交知识表单
     */
    async submitKnowledgeForm(form) {
        const submitButton = form.querySelector('[type="submit"]');
        const originalText = submitButton.textContent;
        
        try {
            // 验证表单
            const validation = this.validateKnowledgeForm(form);
            if (!validation.valid) {
                this.showError(validation.message);
                return;
            }
            
            // 准备数据
            const formData = new FormData(form);
            const data = {
                content: formData.get('content') || formData.get('file-content'),
                description: formData.get('description') || '文本信息',
                name: formData.get('name') || null,
                reference_time: formData.get('reference_time') || null
            };
            
            // 更新按钮状态
            submitButton.textContent = window.t ? window.t('add_knowledge.submitting') : '正在提交...';
            submitButton.disabled = true;
            
            this.showLoading();
            
            // 提交到API
            const result = await api.addTextEpisode(data);
            
            if (result.success) {
                this.showSuccess('知识添加成功');
                form.reset(); // 清空表单
                
                // 清空文件内容隐藏字段
                const fileContentField = document.getElementById('file-content');
                if (fileContentField) {
                    fileContentField.value = '';
                }
                
                // 清空文件名显示
                const fileNameDisplay = document.getElementById('selected-file-name');
                if (fileNameDisplay) {
                    fileNameDisplay.textContent = '';
                }
            } else {
                throw new Error(result.message || '知识添加失败');
            }
            
        } catch (error) {
            console.error('知识添加失败:', error);
            this.showError(error.message || '知识添加失败，请稍后重试');
        } finally {
            submitButton.textContent = originalText;
            submitButton.disabled = false;
            this.hideLoading();
        }
    }
    
    /**
     * 验证知识表单
     */
    validateKnowledgeForm(form) {
        const formData = new FormData(form);
        const inputMethod = formData.get('input-method');
        
        if (inputMethod === 'text') {
            const content = formData.get('content');
            if (!content || content.trim() === '') {
                return { valid: false, message: '文本内容不能为空' };
            }
        } else if (inputMethod === 'file') {
            const fileContent = formData.get('file-content');
            if (!fileContent || fileContent.trim() === '') {
                return { valid: false, message: '请先上传文件' };
            }
        }
        
        // 验证参考时间格式
        const referenceTime = formData.get('reference_time');
        if (referenceTime) {
            const timePattern = /^\d{6}$|^\d{8}$/;
            if (!timePattern.test(referenceTime)) {
                return { valid: false, message: '参考时间格式不正确，请使用 yyyyMMdd 或 yyyyMM 格式' };
            }
        }
        
        return { valid: true };
    }
    
    /**
     * 绑定搜索表单
     */
    bindSearchForm() {
        const form = document.getElementById('search-form');
        if (!form) return;
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.performSearch(form);
        });
        
        // 实时搜索（可选）
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    if (e.target.value.trim().length > 2) {
                        this.performSearch(form);
                    }
                }, 500);
            });
        }
    }
    
    /**
     * 执行搜索
     */
    async performSearch(form) {
        const formData = new FormData(form);
        const query = formData.get('query');
        const limit = parseInt(formData.get('limit') || '10');
        
        if (!query || query.trim() === '') {
            this.showError('请输入搜索关键词');
            return;
        }
        
        this.showLoading();
        
        try {
            const results = await api.searchEntities(query.trim(), limit);
            this.displaySearchResults(results);
        } catch (error) {
            console.error('搜索失败:', error);
            this.showError(error.message || '搜索失败，请稍后重试');
        } finally {
            this.hideLoading();
        }
    }
    
    /**
     * 显示搜索结果
     */
    displaySearchResults(results) {
        const container = document.getElementById('search-results');
        const resultsInfo = document.getElementById('search-results-info');
        
        if (!container) return;
        
        // 清空之前的结果
        container.innerHTML = '';
        
        if (!results || !results.results || results.results.length === 0) {
            container.innerHTML = `
                <div class="text-center py-8">
                    <div class="text-text-secondary mb-2">未找到相关结果</div>
                    <div class="text-sm text-text-secondary/70">可以尝试使用不同的关键词搜索</div>
                </div>
            `;
            
            if (resultsInfo) {
                resultsInfo.textContent = '';
            }
            return;
        }
        
        // 显示结果信息
        if (resultsInfo) {
            resultsInfo.textContent = `找到 ${results.total_count} 个相关结果`;
        }
        
        // 渲染结果
        const resultsHtml = results.results.map(result => `
            <div class="result-item p-4 border border-border rounded-lg mb-4 hover:bg-surface/50 transition-colors">
                <div class="flex justify-between items-start mb-2">
                    <h3 class="text-lg font-semibold text-text">${result.name}</h3>
                    <span class="text-sm text-secondary bg-secondary/10 px-2 py-1 rounded">
                        ${this.getEntityTypeName(result.entity_type)}
                    </span>
                </div>
                
                ${result.summary ? `<p class="text-text-secondary mb-3">${result.summary}</p>` : ''}
                
                <div class="flex items-center gap-4 text-sm text-text-secondary">
                    <span>相关度: ${(result.relevance_score * 100).toFixed(1)}%</span>
                    ${result.entity_type ? `<span>类型: ${this.getEntityTypeName(result.entity_type)}</span>` : ''}
                </div>
                
                ${result.properties && Object.keys(result.properties).length > 0 ? `
                    <div class="mt-3 pt-3 border-t border-border">
                        <div class="text-sm text-text-secondary">
                            <strong>属性:</strong>
                            ${Object.entries(result.properties).map(([key, value]) => 
                                `<span class="inline-block bg-surface px-2 py-1 rounded text-xs mr-2 mb-1">${key}: ${value}</span>`
                            ).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>
        `).join('');
        
        container.innerHTML = resultsHtml;
    }
    
    /**
     * 获取实体类型显示名称
     */
    getEntityTypeName(entityType) {
        if (!entityType) return '未知';
        
        // 尝试从i18n获取翻译
        const translated = window.i18n?.t(`entity_types.${entityType}`);
        return translated !== entityType ? translated : entityType;
    }
    
    /**
     * 绑定高级搜索
     */
    bindAdvancedSearch() {
        const toggle = document.getElementById('advanced-search-toggle');
        const panel = document.getElementById('advanced-search-panel');
        
        if (toggle && panel) {
            toggle.addEventListener('click', () => {
                const isHidden = panel.classList.contains('hidden');
                panel.classList.toggle('hidden');
                toggle.textContent = isHidden ? '隐藏高级搜索' : '高级搜索';
            });
        }
    }
    
    /**
     * 系统健康检查
     */
    async checkSystemHealth() {
        try {
            const health = await api.healthCheck();
            this.updateHealthIndicator(health);
        } catch (error) {
            console.error('系统健康检查失败:', error);
            this.updateHealthIndicator({ status: 'unhealthy' });
        }
    }
    
    /**
     * 更新健康指示器
     */
    updateHealthIndicator(health) {
        const indicator = document.getElementById('system-health-indicator');
        if (!indicator) return;
        
        const isHealthy = health.status === 'healthy';
        indicator.className = `inline-block w-3 h-3 rounded-full ${
            isHealthy ? 'bg-success' : 'bg-error'
        }`;
        indicator.title = isHealthy ? '系统正常' : '系统异常';
    }
    
    /**
     * 加载面板统计数据
     */
    async loadDashboardStats() {
        // 这里可以添加实际的统计数据加载逻辑
        // 暂时显示模拟数据
        const stats = {
            total_knowledge: 0,
            today_added: 0,
            search_count: 0
        };
        
        this.updateDashboardStats(stats);
    }
    
    /**
     * 更新面板统计数据
     */
    updateDashboardStats(stats) {
        const elements = {
            'total-knowledge': stats.total_knowledge,
            'today-added': stats.today_added,
            'search-count': stats.search_count
        };
        
        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value.toLocaleString();
            }
        });
    }
    
    /**
     * 显示加载状态
     */
    showLoading() {
        this.loadingCount++;
        const loading = document.getElementById('global-loading');
        if (loading) {
            loading.classList.remove('hidden');
        }
    }
    
    /**
     * 隐藏加载状态
     */
    hideLoading() {
        this.loadingCount--;
        if (this.loadingCount <= 0) {
            this.loadingCount = 0;
            const loading = document.getElementById('global-loading');
            if (loading) {
                loading.classList.add('hidden');
            }
        }
    }
    
    /**
     * 显示成功消息
     */
    showSuccess(message) {
        this.showNotification(message, 'success');
    }
    
    /**
     * 显示错误消息
     */
    showError(message) {
        this.showNotification(message, 'error');
    }
    
    /**
     * 显示通知
     */
    showNotification(message, type = 'info') {
        // 创建通知元素
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transition-all transform translate-x-full ${
            type === 'success' ? 'bg-success/90 text-white' :
            type === 'error' ? 'bg-error/90 text-white' :
            'bg-info/90 text-white'
        }`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // 显示动画
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // 自动隐藏
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    /**
     * 切换侧边栏（移动端）- 适配新布局系统
     */
    toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        
        if (sidebar && overlay) {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('show');
            
            // 防止背景滚动
            if (sidebar.classList.contains('open')) {
                document.body.classList.add('layout-no-scroll');
            } else {
                document.body.classList.remove('layout-no-scroll');
            }
        }
    }
    
    /**
     * 更新活动导航
     */
    updateActiveNavigation() {
        const navLinks = document.querySelectorAll('[data-nav-link]');
        navLinks.forEach(link => {
            const page = link.getAttribute('data-nav-link');
            if (page === this.currentPage) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }
    
    /**
     * 导航到指定页面
     */
    navigateToPage(page) {
        const urls = {
            'dashboard': '/',
            'add-knowledge': '/add-knowledge',
            'search': '/search'
        };
        
        const url = urls[page];
        if (url) {
            // 对于服务端渲染的多页面应用，直接跳转到新页面
            // 而不是使用pushState，因为需要服务端重新渲染页面内容
            window.location.href = url;
        }
    }
    
    /**
     * 处理浏览器历史变化
     */
    handlePopState(e) {
        // 对于服务端渲染的多页面应用，浏览器前进/后退会自动重新加载页面
        // 不需要手动处理页面状态，因为服务端会重新渲染整个页面
        console.log('浏览器历史变化，页面将重新加载');
    }
    
    /**
     * 处理错误
     */
    handleError(error) {
        console.error('应用错误:', error);
        
        // 显示用户友好的错误信息
        const message = error.message || '发生了未知错误';
        this.showError(message);
    }
    
    /**
     * 处理API错误
     */
    handleApiError(error) {
        console.error('API错误:', error);
        
        // 根据错误类型显示不同的信息
        let message = '操作失败';
        
        if (error.code === 'NETWORK_ERROR') {
            message = '网络连接错误，请检查网络设置';
        } else if (error.code === 'TIMEOUT') {
            message = '请求超时，请稍后重试';
        } else if (error.code >= 500) {
            message = '服务器错误，请联系技术支持';
        } else if (error.code >= 400) {
            message = error.message || '请求参数错误';
        }
        
        this.showError(message);
    }
    
    /**
     * 语言变更处理
     */
    onLanguageChange(language) {
        console.log('语言变更为:', language);
        // 可以在这里添加语言变更后的特定逻辑
    }
    
    /**
     * 主题变更处理
     */
    onThemeChange(theme) {
        console.log('主题变更为:', theme);
        // 可以在这里添加主题变更后的特定逻辑
    }
    
    /**
     * 页面加载完成处理
     */
    onPageLoad() {
        console.log('页面加载完成');
        // 可以在这里添加页面加载后的初始化逻辑
    }
    
    /**
     * 页面可见性变化处理
     */
    onVisibilityChange() {
        if (document.hidden) {
            console.log('页面进入后台');
        } else {
            console.log('页面进入前台');
            // 可以在这里刷新数据
        }
    }
}

// 创建全局应用实例
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});

/**
 * 便捷的全局函数
 */
window.showLoading = () => window.app?.showLoading();
window.hideLoading = () => window.app?.hideLoading();
window.showSuccess = (message) => window.app?.showSuccess(message);
window.showError = (message) => window.app?.showError(message);
window.showNotification = (message, type) => window.app?.showNotification(message, type);