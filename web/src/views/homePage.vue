<template>
    <div class="home-container">
        <main class="main-content">
            <!-- 欢迎区域 -->
            <section class="hero-section">
                <div class="hero-content">
                    <h1>欢迎使用 Job Agent：AI驱动的求职助手</h1>
                    <p class="hero-description">
                        Job Agent是一款基于大数据、爬虫和人工智能技术的求职助手，专为BOSS直聘等招聘网站设计。
                        <br>它通过分析职位描述、匹配简历、提供行业趋势等方式，帮助您快速评估职位并找到最合适的工作机会。
                    </p>
                </div>
            </section>

            <!-- 功能区域 -->
            <section class="features-section feature-card-analysis">
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-header">
                            <span class="feature-icon">💼</span>
                            <h3 class="feature-title">职位搜集</h3>
                        </div>
                        <p class="feature-description">
                            通过爬虫技术，根据查询规则，获取BOSS直聘招聘网站各行各业岗位信息。
                        </p>
                    </div>

                    <div class="feature-card">
                        <div class="feature-header">
                            <span class="feature-icon">🔍</span>
                            <h3 class="feature-title">岗位分析</h3>
                        </div>
                        <p class="feature-description">
                            对数据库中存放的岗位信息进行多维度分析，以及行业所需技能词云图的生成。
                        </p>
                    </div>

                    <div class="feature-card">
                        <div class="feature-header">
                            <span class="feature-icon">✨</span>
                            <h3 class="feature-title">自动化投递简历</h3>
                        </div>
                        <p class="feature-description">
                            对所选岗位批量投递简历，根据简历和岗位描述针对性润色问候语，提高Boss回复率。
                        </p>
                    </div>

                    <div class="feature-card">
                        <div class="feature-header">
                            <span class="feature-icon">🗣️</span>
                            <h3 class="feature-title">智能岗位匹配</h3>
                        </div>
                        <p class="feature-description">
                            通过用户自然语言描述，过滤不感兴趣岗位，并根据简历和岗位信息进行匹配度评估。
                        </p>
                    </div>
                </div>
            </section>

            <!-- 底部区域 -->
            <section class="footer-section">
                <p class="footer-text">
                    Job Agent是您效率和效益求职的最佳选择，帮助您轻松应对职场竞争。🌟
                </p>
                <el-button type="primary" size="large" class="github-button" @click="openGitHub">
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
        align-items: center;
        gap: 1rem;
    }

    .hero-section {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0rem;

        .hero-content {
            flex: 1;

            h1 {
                font-size: 2rem;
                margin-bottom: 1.5rem;
                margin-top: -1.5rem;
                color: #2c3e50;
            }

            .hero-description {
                font-size: 1rem;
                line-height: 1.6;
                color: #666;
                margin-bottom: 0rem;
                text-align: center;
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
            margin-bottom: 0rem;
            color: #2c3e50;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(2, 300px);
            justify-content: center;
            margin-top: 1rem;
            margin-bottom: -2rem;
            gap: 2rem;

            .feature-card {
                height: 110px;
                background: #fff;
                border-radius: 8px;
                padding: 1.5rem;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;

                &:hover {
                    transform: translateY(-5px);
                }

                .feature-header {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    margin-bottom: 0.5rem;

                    .feature-icon {
                        font-size: 1.5rem;
                        margin: 0;
                    }

                    .feature-title {
                        font-size: 1.2rem;
                        margin: 0;
                        color: #2c3e50;
                    }
                }

                .feature-description {
                    font-size: 1rem;
                    line-height: 1.5;
                    color: #666;
                    margin: 0;
                }
            }
        }

    }

    .footer-section {
        text-align: center;
        margin-top: 0rem;
        padding: 2rem 0;
        border-top: 1px solid #eee;

        .footer-text {
            font-size: 1.1rem;
            margin-bottom: 1rem;
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

// 小屏下自动变一列
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
  