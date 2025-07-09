<template>
    <div v-if="visible" class="loading-container">
      <div class="loading-content">
        <span class="loading-text">{{ message }}</span>
        <span class="dot" v-for="i in 3" :key="i" :style="{ animationDelay: `${i * 0.2}s` }">.</span>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoadingDots',
    props: {
      message: {
        type: String,
        default: '加载中，请稍候'
      },
      visible: {
        type: Boolean,
        default: true
      }
    }
  }
  </script>
  
  <style scoped>
  .loading-container {
    position: fixed; /* 固定定位*/
    top: 32px;
    left: 600px;
    transform: translate(-50%, -50%);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none; /* 不影响鼠标事件 */
  }
  
  .loading-content {
    font-size: 16px;
    color: #409EFF; /* Element Plus 主色 */
    display: flex;
    align-items: center;
  }
  
  .loading-text {
    font-weight: 500;
    margin-right: 4px;
  }
  
  .dot {
    font-weight: bold;
    animation: bounce 1s infinite;
    font-size: 18px;
    color: #409EFF;
    line-height: 1;
  }
  
  /* 小跳动动画 */
  @keyframes bounce {
    0%, 80%, 100% {
      transform: scale(1);
      opacity: 0.3;
    }
    40% {
      transform: scale(1.4);
      opacity: 1;
    }
  }
  </style>
  