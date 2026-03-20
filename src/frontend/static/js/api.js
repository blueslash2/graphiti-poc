/**
 * API客户端
 * 封装与后端API的通信逻辑，提供统一的请求接口
 */
class ApiClient {
    constructor() {
        this.baseURL = window.FRONTEND_CONFIG?.apiBaseUrl || 'http://localhost:8000';
        this.timeout = window.FRONTEND_CONFIG?.apiTimeout || 30000;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };
    }
    
    /**
     * 基础请求方法
     * @param {string} endpoint - API端点
     * @param {Object} options - 请求选项
     * @returns {Promise} 响应数据
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const controller = new AbortController();
        
        // 设置超时
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        
        // 合并请求头
        const headers = {
            ...this.defaultHeaders,
            ...options.headers
        };
        
        // 构建请求配置
        const config = {
            method: options.method || 'GET',
            headers: headers,
            signal: controller.signal,
            ...options
        };
        
        // 如果是POST/PUT请求且没有body，移除Content-Type
        if (!options.body && (config.method === 'POST' || config.method === 'PUT')) {
            delete headers['Content-Type'];
        }
        
        try {
            console.log(`API请求: ${config.method} ${url}`);
            
            const response = await fetch(url, config);
            
            clearTimeout(timeoutId);
            
            // 检查响应状态
            if (!response.ok) {
                const errorData = await this.parseErrorResponse(response);
                throw new ApiError(
                    `HTTP ${response.status}: ${response.statusText}`,
                    response.status,
                    errorData
                );
            }
            
            // 解析响应数据
            const data = await response.json();
            
            console.log(`API响应成功: ${config.method} ${url}`, data);
            return data;
            
        } catch (error) {
            clearTimeout(timeoutId);
            
            if (error.name === 'AbortError') {
                throw new ApiError('请求超时，请稍后重试', 'TIMEOUT');
            }
            
            if (error instanceof ApiError) {
                throw error;
            }
            
            // 网络错误或其他异常
            console.error(`API请求失败: ${config.method} ${url}`, error);
            throw new ApiError('网络连接错误，请检查网络设置', 'NETWORK_ERROR');
        }
    }
    
    /**
     * 解析错误响应
     * @param {Response} response - 错误响应
     * @returns {Object} 错误数据
     */
    async parseErrorResponse(response) {
        try {
            const text = await response.text();
            if (!text) return null;
            
            return JSON.parse(text);
        } catch (error) {
            return { message: response.statusText };
        }
    }
    
    /**
     * GET请求
     */
    async get(endpoint, params = {}, options = {}) {
        const url = new URL(endpoint, this.baseURL);
        Object.keys(params).forEach(key => {
            if (params[key] !== null && params[key] !== undefined) {
                url.searchParams.append(key, params[key]);
            }
        });
        
        return this.request(url.pathname + url.search, {
            method: 'GET',
            ...options
        });
    }
    
    /**
     * POST请求
     */
    async post(endpoint, data = {}, options = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
            ...options
        });
    }
    
    /**
     * PUT请求
     */
    async put(endpoint, data = {}, options = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
            ...options
        });
    }
    
    /**
     * DELETE请求
     */
    async delete(endpoint, options = {}) {
        return this.request(endpoint, {
            method: 'DELETE',
            ...options
        });
    }
    
    // 具体的API方法
    
    /**
     * 健康检查
     */
    async healthCheck() {
        return this.get('/health');
    }
    
    /**
     * 添加文本情节
     * @param {Object} data - 文本数据
     * @returns {Promise} 添加结果
     */
    async addTextEpisode(data) {
        // 验证必需字段
        if (!data.content || data.content.trim() === '') {
            throw new Error('文本内容不能为空');
        }
        
        // 验证参考时间格式
        if (data.reference_time) {
            const timePattern = /^\d{6}$|^\d{8}$/;
            if (!timePattern.test(data.reference_time)) {
                throw new Error('参考时间格式不正确，请使用 yyyyMMdd 或 yyyyMM 格式');
            }
        }
        
        return this.post('/api/episodes/text', data);
    }
    
    /**
     * 搜索实体
     * @param {string} query - 搜索关键词
     * @param {number} limit - 结果数量限制
     * @returns {Promise} 搜索结果
     */
    async searchEntities(query, limit = 10) {
        if (!query || query.trim() === '') {
            throw new Error('搜索关键词不能为空');
        }
        
        if (limit < 1 || limit > 50) {
            throw new Error('结果数量必须在1-50之间');
        }
        
        return this.get('/api/episodes/search', {
            query: query.trim(),
            limit: limit
        });
    }
    
    /**
     * 获取系统信息
     */
    async getSystemInfo() {
        return this.get('/');
    }
}

/**
 * API错误类
 * 封装API请求错误的详细信息
 */
class ApiError extends Error {
    constructor(message, code, data = null) {
        super(message);
        this.name = 'ApiError';
        this.code = code;
        this.data = data;
        this.timestamp = new Date().toISOString();
    }
    
    toString() {
        return `ApiError: ${this.message} (code: ${this.code})`;
    }
    
    toJSON() {
        return {
            name: this.name,
            message: this.message,
            code: this.code,
            data: this.data,
            timestamp: this.timestamp
        };
    }
}

/**
 * 请求重试工具
 * @param {Function} requestFunc - 请求函数
 * @param {number} maxRetries - 最大重试次数
 * @param {number} delay - 重试延迟（毫秒）
 */
async function retryRequest(requestFunc, maxRetries = 3, delay = 1000) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await requestFunc();
        } catch (error) {
            if (i === maxRetries - 1) {
                throw error; // 最后一次重试失败，抛出错误
            }
            
            // 只在网络错误或超时时重试
            if (error.code === 'NETWORK_ERROR' || error.code === 'TIMEOUT') {
                console.log(`请求失败，${delay}ms后重试 (${i + 1}/${maxRetries})`);
                await new Promise(resolve => setTimeout(resolve, delay));
            } else {
                throw error; // 其他错误不重试
            }
        }
    }
}

// 创建全局API客户端实例
window.apiClient = new ApiClient();

/**
 * 便捷的API调用函数
 */
window.api = {
    healthCheck: () => window.apiClient.healthCheck(),
    addTextEpisode: (data) => window.apiClient.addTextEpisode(data),
    searchEntities: (query, limit) => window.apiClient.searchEntities(query, limit),
    getSystemInfo: () => window.apiClient.getSystemInfo()
};