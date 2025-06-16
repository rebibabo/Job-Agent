<template>
    <div class="not-found-container">
      <div class="not-found-content">
        <div class="error-code">404</div>
        <div class="error-message">抱歉，您访问的页面不存在</div>
        <div class="error-desc">请检查您输入的网址是否正确，或点击下方按钮返回首页</div>
        <el-button 
          type="primary" 
          @click="goHome"
          class="home-button"
        >
          返回首页
        </el-button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NotFound',
    methods: {
      goHome() {
        this.$router.push('/');
      }
    }
  }
  </script>
  
  <style lang="scss" scoped>
  .not-found-container {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 90vh;       /* 页面高度设置为100vh会有滑动栏 */
    background-color: #f5f7fa;
    // background-image: radial-gradient(circle at 50% 50%, #e0e0e0 1px, transparent 1px);
    background-size: 20px 20px;
  }
  
  .not-found-content {
    text-align: center;
    padding: 40px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    max-width: 500px;
    width: 90%;
  }
  
  .error-code {
    font-size: 120px;
    font-weight: bold;
    color: #f56c6c;
    line-height: 1;
    margin-bottom: 20px;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .error-message {
    font-size: 24px;
    color: #606266;
    margin-bottom: 16px;
    font-weight: 500;
  }
  
  .error-desc {
    font-size: 16px;
    color: #909399;
    margin-bottom: 30px;
  }
  
  .home-button {
    padding: 12px 36px;
    font-size: 16px;
    border-radius: 20px;
    box-shadow: 0 4px 8px rgba(64, 158, 255, 0.2);
    transition: all 0.3s ease;
  
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 12px rgba(64, 158, 255, 0.3);
    }
  }
  </style>