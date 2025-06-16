const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/api": {
        // 匹配所有以 /api 开头的请求
        target: "http://localhost:8081", // 目标服务器地址
        changeOrigin: true, // 改变请求头中的 Host 为目标地址
        pathRewrite: {
          "^/api": "", // 去掉路径中的 /api 前缀
            },
            onProxyReq: function(proxyReq, req, res) {
                // 打印代理目标服务器的 IP 和端口
                console.log(
                  '[Proxy] 目标地址 ->', 
                  proxyReq.protocol, // http 或 https
                    proxyReq.host,     // 目标主机（如 localhost)
                  '完整路径:', proxyReq.path
                );
                
                // 打印原始请求信息（可选）
                console.log(
                  '[Proxy] 原始请求 ->',
                  req.method,       // GET/POST 等
                  req.originalUrl   // 前端发起的原始路径（如 /api/login）
                );
              }
      },
    },
  },
});
