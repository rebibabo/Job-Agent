<template>
    <div class="home-container">
      <!-- 主要内容 -->
      <main class="main-content">
        <!-- 欢迎区域 -->
        <section class="hero-section">
          <div class="hero-content">
            <h1>欢迎使用 Job Agent：AI驱动的求职助手</h1>
            <p class="hero-description">
              Job Agent是一款基于人工智能技术的求职助手，专为BOSS直聘等招聘网站设计。
              <br>它通过分析职位描述、匹配简历、提供行业趋势等方式，帮助您快速评估职位并找到最合适的工作机会。
            </p>
          </div>
          <!-- <div class="hero-image">
            <img src="@/assets/hero-image.png" alt="AI求职助手">
          </div> -->
        </section>
  
        <!-- 功能区域 -->
        <section class="features-section">
          <div class="features-grid">
            <div class="feature-card">
              <div class="feature-icon">💼</div>
              <h3 class="feature-title">职位分析</h3>
              <p class="feature-description">
                通过BOSS直聘等招聘网站快速评估职位并获取行业信息，帮助您快速找到最适合自己的职位。
              </p>
            </div>
  
            <div class="feature-card">
              <div class="feature-icon">📄</div>
              <h3 class="feature-title">简历匹配与提交</h3>
              <p class="feature-description">
                自动匹配简历并提交至适合的职位，节省您的时间和精力。
              </p>
            </div>
  
            <div class="feature-card">
              <div class="feature-icon">✨</div>
              <h3 class="feature-title">简历优化</h3>
              <p class="feature-description">
                提供个性化的简历建议，使您的简历更加吸引人。
              </p>
            </div>
  
            <div class="feature-card">
              <div class="feature-icon">🗣️</div>
              <h3 class="feature-title">面试准备</h3>
              <p class="feature-description">
                提供经过筛选的面试题目和参考答案，帮助您在面试中更加自信。
              </p>
            </div>
          </div>
        </section>
  
        <!-- 底部区域 -->
        <section class="footer-section">
          <p class="footer-text">
            Job Agent是您效率和效益求职的最佳选择，帮助您轻松应对职场竞争。🌟
          </p>
          <el-button 
            type="primary" 
            size="large" 
            class="github-button"
            @click="openGitHub"
          >
            <i class="el-icon-star-off"></i> 访问我们的GitHub网站
          </el-button>
        </section>
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomePage',
    methods: {
      openGitHub() {
        window.open('https://github.com/rebibabo/Job-Agent', '_blank');
      }
    }
  }
  </script>
  
  <style lang="scss" scoped>
  .home-container {
    font-family: 'Arial', sans-serif;
    color: #333;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  
    .main-content {
      display: flex;
      flex-direction: column;
      gap: 3rem;
    }
  
    .hero-section {
      display: flex;
      align-items: center;
      gap: 3rem;
      margin-bottom: 2rem;
  
      .hero-content {
        flex: 1;
        
        h1 {
          font-size: 2.5rem;
          margin-bottom: 1.5rem;
          color: #2c3e50;
        }
  
        .hero-description {
          font-size: 1.1rem;
          line-height: 1.6;
          color: #666;
          margin-bottom: 2rem;
        }
      }
  
      .hero-image {
        flex: 1;
        text-align: center;
        
        img {
          max-width: 100%;
          height: auto;
          border-radius: 8px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
      }
    }
  
    .features-section {
      .section-title {
        font-size: 2rem;
        text-align: center;
        margin-bottom: 2rem;
        color: #2c3e50;
      }
  
      .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
  
        .feature-card {
          background: #fff;
          border-radius: 8px;
          padding: 2rem;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
          transition: transform 0.3s ease;
  
          &:hover {
            transform: translateY(-5px);
          }
  
          .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
          }
  
          .feature-title {
            font-size: 1.3rem;
            margin-bottom: 1rem;
            color: #2c3e50;
          }
  
          .feature-description {
            font-size: 1rem;
            line-height: 1.6;
            color: #666;
          }
        }
      }
    }
  
    .footer-section {
      text-align: center;
      margin-top: 3rem;
      padding: 2rem 0;
      border-top: 1px solid #eee;
  
      .footer-text {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        line-height: 1.6;
      }
  
      .github-button {
        background-color: #24292e;
        border-color: #24292e;
        font-weight: 500;
  
        &:hover {
          background-color: #2d3338;
          border-color: #2d3338;
        }
  
        i {
          margin-right: 8px;
        }
      }
    }
  }
  
  @media (max-width: 768px) {
    .home-container {
      padding: 1rem;
  
      .hero-section {
        flex-direction: column;
        gap: 1.5rem;
  
        .hero-content {
          h1 {
            font-size: 2rem;
          }
        }
      }
  
      .features-grid {
        grid-template-columns: 1fr;
      }
    }
  }
  </style>