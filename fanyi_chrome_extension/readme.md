一个浏览器插件，选中后可以翻译。

本地ollama跑大模型，浏览器插件调用本地的接口。
因为有cross-origin限制，所以需要本地server.py做转发，才可以请求ollama的api。

支持chrome插件。

启动方式：
1 安装ollama
2 下载并run一个大模型
3 根据模型名称，调整server.py中post请求中body的model参数
