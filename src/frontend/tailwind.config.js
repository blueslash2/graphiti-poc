/**
 * Tailwind CSS 配置文件
 * 针对金融机构风格的专业设计
 */
module.exports = {
  content: [
    "./src/frontend/templates/**/*.html",
    "./src/frontend/static/js/**/*.js"
  ],
  
  darkMode: 'class', // 使用类名切换暗色主题
  
  theme: {
    extend: {
      // 扩展颜色系统 - 金融机构专业配色
      colors: {
        // 主色调 - 深蓝 (金融机构常用)
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',  // 主色调
          600: '#2563eb',  // 悬停状态
          700: '#1d4ed8',  // 激活状态
          800: '#1e40af',  // 深色模式主色调
          900: '#1e3a8a',
        },
        
        // 辅助色 - 中性灰蓝
        secondary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',  // 主辅助色
          600: '#475569',  // 文本次要色
          700: '#334155',  // 边框色
          800: '#1e293b',  // 文本主色
          900: '#0f172a',  // 深色背景
        },
        
        // 背景色系统
        background: {
          DEFAULT: 'var(--color-background)',
          surface: 'var(--color-surface)',
          elevated: 'var(--color-surface-elevated)',
        },
        
        // 文本色系统
        text: {
          DEFAULT: 'var(--color-text)',
          secondary: 'var(--color-text-secondary)',
          disabled: 'var(--color-text-disabled)',
        },
        
        // 边框色系统
        border: {
          DEFAULT: 'var(--color-border)',
          light: 'var(--color-border-light)',
          dark: 'var(--color-border-dark)',
        },
        
        // 状态色 - 成功
        success: {
          50: '#ecfdf5',
          100: '#d1fae5',
          500: '#10b981',  // 亮色主题
          600: '#059669',  // 深色主题
        },
        
        // 状态色 - 警告
        warning: {
          50: '#fffbeb',
          100: '#fef3c7',
          500: '#f59e0b',  // 亮色主题
          600: '#d97706',  // 深色主题
        },
        
        // 状态色 - 错误
        error: {
          50: '#fef2f2',
          100: '#fee2e2',
          500: '#ef4444',  // 亮色主题
          600: '#dc2626',  // 深色主题
        },
        
        // 状态色 - 信息
        info: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#06b6d4',  // 亮色主题
          600: '#0891b2',  // 深色主题
        },
      },
      
      // 扩展字体系统
      fontFamily: {
        sans: [
          'Inter',
          'system-ui',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'sans-serif'
        ],
        mono: [
          'JetBrains Mono',
          'Monaco',
          'Consolas',
          'Liberation Mono',
          'Menlo',
          'monospace'
        ],
      },
      
      // 扩展字体大小
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
        '5xl': ['3rem', { lineHeight: '1' }],
        '6xl': ['3.75rem', { lineHeight: '1' }],
      },
      
      // 扩展间距系统
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
        '144': '36rem',
      },
      
      // 扩展圆角系统
      borderRadius: {
        '4xl': '2rem',
      },
      
      // 扩展阴影系统
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'medium': '0 4px 25px -5px rgba(0, 0, 0, 0.1), 0 15px 30px -5px rgba(0, 0, 0, 0.06)',
        'strong': '0 10px 40px -8px rgba(0, 0, 0, 0.15), 0 20px 40px -10px rgba(0, 0, 0, 0.08)',
        
        // 暗色主题阴影
        'dark-soft': '0 2px 15px -3px rgba(0, 0, 0, 0.2), 0 10px 20px -2px rgba(0, 0, 0, 0.15)',
        'dark-medium': '0 4px 25px -5px rgba(0, 0, 0, 0.25), 0 15px 30px -5px rgba(0, 0, 0, 0.2)',
        'dark-strong': '0 10px 40px -8px rgba(0, 0, 0, 0.3), 0 20px 40px -10px rgba(0, 0, 0, 0.25)',
      },
      
      // 扩展动画
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'bounce-in': 'bounceIn 0.5s ease-out',
      },
      
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { 
            opacity: '0',
            transform: 'translateY(10px)',
          },
          '100%': { 
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
        slideDown: {
          '0%': { 
            opacity: '0',
            transform: 'translateY(-10px)',
          },
          '100%': { 
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
        scaleIn: {
          '0%': { 
            opacity: '0',
            transform: 'scale(0.95)',
          },
          '100%': { 
            opacity: '1',
            transform: 'scale(1)',
          },
        },
        bounceIn: {
          '0%': {
            opacity: '0',
            transform: 'scale(0.3)',
          },
          '50%': {
            opacity: '1',
            transform: 'scale(1.05)',
          },
          '70%': {
            transform: 'scale(0.9)',
          },
          '100%': {
            opacity: '1',
            transform: 'scale(1)',
          },
        },
      },
      
      // 扩展断点 - 针对金融机构用户常用的设备
      screens: {
        'xs': '475px',   // 超小屏手机
        'sm': '640px',   // 小屏手机
        'md': '768px',   // 平板
        'lg': '1024px',  // 小屏笔记本
        'xl': '1280px',  // 标准笔记本
        '2xl': '1536px', // 大屏显示器
        '3xl': '1920px', // 超大屏显示器
      },
      
      // 扩展z-index
      zIndex: {
        '60': '60',
        '70': '70',
        '80': '80',
        '90': '90',
        '100': '100',
      },
    },
  },
  
  plugins: [
    // 自定义插件 - 添加金融机构特定的工具类
    function({ addUtilities, theme }) {
      const newUtilities = {
        // 文本安全优化
        '.text-safe': {
          'font-feature-settings': '"liga" 1, "calt" 1',
          'text-rendering': 'optimizeLegibility',
        },
        
        // 金融数字样式
        '.number-mono': {
          'font-variant-numeric': 'tabular-nums lining-nums',
          'font-family': theme('fontFamily.mono'),
        },
        
        // 高对比度文本
        '.text-high-contrast': {
          'color': 'var(--color-text)',
          'font-weight': '500',
        },
        
        // 卡片阴影 - 专业级别
        '.card-shadow': {
          'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        },
        
        '.card-shadow-hover': {
          'box-shadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        },
        
        // 表单焦点样式 - 专业级别
        '.form-focus': {
          'outline': '2px solid transparent',
          'outline-offset': '2px',
          '--tw-ring-color': theme('colors.primary.500'),
          '--tw-ring-offset-shadow': 'var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color)',
          '--tw-ring-shadow': 'var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color)',
          'box-shadow': 'var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000)',
          'border-color': theme('colors.primary.500'),
        },
        
        // 渐变背景 - 专业级别
        '.gradient-primary': {
          'background': `linear-gradient(135deg, ${theme('colors.primary.500')} 0%, ${theme('colors.primary.600')} 100%)`,
        },
        
        '.gradient-surface': {
          'background': `linear-gradient(135deg, ${theme('colors.secondary.50')} 0%, ${theme('colors.secondary.100')} 100%)`,
        },
        
        // 暗色主题工具类
        '.dark \&': {
          '.dark\:bg-surface-dark': {
            'background-color': theme('colors.secondary.900'),
          },
          '.dark\:text-text-dark': {
            'color': theme('colors.secondary.100'),
          },
          '.dark\:border-border-dark': {
            'border-color': theme('colors.secondary.700'),
          },
        },
      };
      
      addUtilities(newUtilities);
    },
  ],
}