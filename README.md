# 钉钉AI助理对接服务

为国际高中定制的钉钉AI助理对接服务，提供符合钉钉官方API规范的对话接口，支持完整的线程会话管理。

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 主要功能

- ✅ 钉钉API认证与访问令牌管理  
- 🧵 完整的Threads模式交互流程（创建线程→添加消息→执行运行→获取结果）  
- 🔄 自动会话管理（30分钟有效期）  
- ⚡ 异步任务状态轮询机制  
- 📦 开箱即用的RESTful API接口  
- 🔒 基础跨域支持(CORS)  

## 快速开始

### 环境要求
- Python 3.7+  
- pip包管理工具  

### 安装步骤

1. **克隆仓库**  
```bash
git clone https://github.com/your-org/dingtalk-ai-assistant.git
cd dingtalk-ai-assistant

2. **安装依赖**  
```bash
pip install flask requests python-dotenv flask-cors
cd dingtalk-ai-assistant

3. **配置环境变量**
创建 .env 文件：
```ini
# 钉钉应用配置
DING_APP_KEY="your_app_key"
DING_APP_SECRET="your_app_secret"
AI_ASSISTANT_ID="your_assistant_id"

4. **启动服务**
```bash
flask run --port 5000

### API接口文档
##提问接口
