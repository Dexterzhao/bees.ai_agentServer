以下是完全可复制的Markdown格式（已严格验证代码块格式）：

```markdown
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
```

2. **安装依赖**  
```bash
pip install flask requests python-dotenv flask-cors
```

3. **配置环境变量**  
创建 `.env` 文件：  
```ini
# 钉钉应用配置
DING_APP_KEY="your_app_key"
DING_APP_SECRET="your_app_secret"
AI_ASSISTANT_ID="your_assistant_id"
```

4. **启动服务**  
```bash
flask run --port 5000
```

## API接口文档

### 提问接口  
```http
POST /assistant/ask
Content-Type: application/json

{
    "question": "国际学生如何申请奖学金？",
    "sessionId": "可选会话ID"
}
```

**成功响应**：  
```json
{
    "code": 0,
    "answer": "国际学生奖学金申请流程如下...",
    "sessionId": "session_12345"
}
```

### 参数说明  
| 参数         | 类型     | 必填 | 说明                                      |
|--------------|----------|------|------------------------------------------|
| `question`   | string   | 是   | 用户提问内容（不超过2000字符）           |
| `sessionId`  | string   | 否   | 会话ID（首次请求不传，后续对话需携带）   |

## 会话管理

- **有效期**：30分钟无活动自动过期  
- **存储方式**：默认内存存储（生产环境建议使用Redis）  
- **新建会话**：不携带`sessionId`时自动生成UUID格式ID  

## 生产部署

### 使用Gunicorn部署  
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 推荐配置（`.env.production`）  
```ini
# 会话存储（需自行实现存储适配器）
SESSION_STORAGE=redis://localhost:6379/0

# 请求限流（建议50次/分钟）
RATE_LIMIT=50/minute
```

## 常见问题

### Q1: 如何获取钉钉应用凭证？  
1. 访问[钉钉开放平台](https://open.dingtalk.com)  
2. 创建企业内部应用  
3. 在"权限管理"开通"AI助理"权限  
4. 在"凭证管理"获取AppKey和AppSecret  

### Q2: 请求超时如何处理？  
- 检查钉钉AI助理是否启用  
- 确认网络可访问`api.dingtalk.com`  
- 调整轮询超时时间（默认30秒）  

### Q3: 如何查看日志？  
```bash
# 实时日志（生产环境）
tail -f /var/log/dingtalk-ai.log

# 调试模式（开发环境）
FLASK_DEBUG=1 flask run
```

## 许可证  
MIT License © 2023 国际高中技术部
```
