# Graphiti 布局系统文档

## 概述

Graphiti布局系统采用现代CSS Flexbox技术，解决了原有的header重叠问题，提供了清晰、可维护的布局架构。

## 关键修复

**2024-01-04 重要更新**：彻底解决了main区域与header区域重叠的问题
- **问题根源**：`.layout-main`的`flex: 1`属性让它从容器顶部开始计算，而不是从header下方开始
- **解决方案**：使用`height: calc(100vh - 4rem)`精确计算main区域高度，确保从header下方开始
- **结果**：main区域现在完全位于header下方，无任何重叠

## 布局结构

```
Viewport
├── Header (sticky定位，避免重叠)
├── Main Container (flex列布局)
│   ├── Content Area (flex行布局)
│   │   ├── Sidebar (固定宽度256px)
│   │   └── Main Content (自适应剩余宽度)
│   └── Footer (始终在底部)
```

## CSS类名规范

### 主容器
- `.layout-container` - 主容器，全屏flex列布局
- `.layout-header` - 顶部导航栏，sticky定位，高度4rem
- `.layout-main` - 主体内容区域，flex行布局，高度`calc(100vh - 4rem)`
- `.layout-sidebar` - 侧边栏，固定宽度256px
- `.layout-content` - 主内容区域，自适应剩余宽度
- `.layout-footer` - 底部页脚

### 辅助类
- `.layout-overlay` - 移动端遮罩层
- `.layout-full-height` - 全高度
- `.layout-scrollable` - 可滚动
- `.layout-no-scroll` - 禁止滚动

## 响应式设计

### 断点
- 移动端：≤767px
- 桌面端：≥768px

### 移动端行为
1. 侧边栏变为抽屉式菜单
2. 显示移动端菜单按钮
3. 点击遮罩层关闭菜单
4. 防止背景滚动

## 使用示例

### 基础模板结构
```html
<div class="layout-container">
    <header class="layout-header">
        <!-- 导航内容 -->
    </header>
    
    <main class="layout-main">
        <nav class="layout-sidebar">
            <!-- 侧边栏内容 -->
        </nav>
        
        <div class="layout-overlay"></div>
        
        <div class="layout-content">
            <div class="layout-content-inner">
                <!-- 主内容 -->
            </div>
        </div>
    </main>
    
    <footer class="layout-footer">
        <!-- 页脚内容 -->
    </footer>
</div>
```

### JavaScript集成
```javascript
// 切换侧边栏
window.app.toggleSidebar();

// 显示/隐藏加载状态
window.app.showLoading();
window.app.hideLoading();

// 显示通知
window.app.showSuccess('操作成功');
window.app.showError('操作失败');
```

## 主题支持

布局系统完全支持暗色主题，使用CSS变量自动适配。

## 浏览器兼容性

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## 性能优化

1. 使用CSS Flexbox，性能优于Grid布局
2. 移动端使用transform动画，硬件加速
3. 支持`prefers-reduced-motion`媒体查询

## 维护指南

1. **修改布局结构**：编辑`layout.css`文件
2. **调整响应式**：修改媒体查询部分
3. **添加新组件**：遵循BEM命名规范
4. **测试兼容性**：使用浏览器开发者工具

## 常见问题

### Q: Header重叠问题如何解决？
A: 使用sticky定位替代fixed定位，避免z-index冲突。

### Q: 移动端菜单不工作？
A: 确保正确绑定`data-sidebar-toggle`属性和JavaScript事件。

### Q: 内容区域高度不一致？
A: 使用flex布局确保sidebar和main content高度一致。

### Q: 如何添加新的布局区域？
A: 在`layout.css`中添加新的CSS类，遵循命名规范。