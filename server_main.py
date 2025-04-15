"""
DingTalk AI Assistant API Server (Threads模式)
环境要求：Python 3.7+，需安装 flask requests python-dotenv
"""
import os
import json
import time
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

# 初始化环境
load_dotenv()
app = Flask(__name__)
CORS(app)

# 钉钉API配置
DINGTALK_API = "https://api.dingtalk.com"
APP_KEY = os.getenv("DING_APP_KEY")
APP_SECRET = os.getenv("DING_APP_SECRET")
AI_ASSISTANT_ID = os.getenv("AI_ASSISTANT_ID")

# 全局缓存
_access_token = None
_token_expire = 0
_session_map = {}  # session_id: {thread_id, last_active}

def get_access_token():
    """获取钉钉访问令牌（带缓存）"""
    global _access_token, _token_expire
    
    if time.time() < _token_expire and _access_token:
        return _access_token
    
    url = f"{DINGTALK_API}/v1.0/oauth2/accessToken"
    payload = {"appKey": APP_KEY, "appSecret": APP_SECRET}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        _access_token = data["accessToken"]
        _token_expire = time.time() + data["expireIn"] - 300
        return _access_token
    except Exception as e:
        app.logger.error(f"Token获取失败: {str(e)}")
        raise

def ding_request(method, endpoint, payload=None):
    """统一钉钉API请求方法"""
    url = f"{DINGTALK_API}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "x-acs-dingtalk-access-token": get_access_token()
    }
    
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        app.logger.error(f"API Error: {e.response.text}")
        raise

def create_thread():
    """创建对话线程"""
    response = ding_request("POST", "/v1.0/assistant/threads")
    return response["threadId"]

def add_message(thread_id, content):
    """添加用户消息到线程"""
    endpoint = f"/v1.0/assistant/threads/{thread_id}/messages"
    payload = {
        "content": content,
        "role": "user"
    }
    return ding_request("POST", endpoint, payload)

def create_run(thread_id):
    """启动AI运行"""
    endpoint = f"/v1.0/assistant/threads/{thread_id}/runs"
    payload = {"assistantId": AI_ASSISTANT_ID}
    response = ding_request("POST", endpoint, payload)
    return response["runId"]

def get_run_status(thread_id, run_id):
    """获取运行状态"""
    endpoint = f"/v1.0/assistant/threads/{thread_id}/runs/{run_id}"
    return ding_request("GET", endpoint)

def get_messages(thread_id):
    """获取对话消息列表"""
    endpoint = f"/v1.0/assistant/threads/{thread_id}/messages"
    response = ding_request("GET", endpoint)
    return response["data"]

def process_session(session_id):
    """管理会话线程"""
    if session_id in _session_map:
        session = _session_map[session_id]
        if time.time() - session["last_active"] < 1800:  # 30分钟有效期
            session["last_active"] = time.time()
            return session["thread_id"]
    
    # 新建会话
    thread_id = create_thread()
    _session_map[session_id] = {
        "thread_id": thread_id,
        "last_active": time.time()
    }
    return thread_id

@app.route('/assistant/ask', methods=['POST'])
def ask_assistant():
    """完整交互流程入口"""
    try:
        data = request.json
        if not data or "question" not in data:
            return jsonify({"code": 400, "error": "参数错误"}), 400
        
        # 会话管理
        session_id = data.get("sessionId", str(uuid.uuid4()))
        thread_id = process_session(session_id)
        
        # 添加用户消息
        add_message(thread_id, data["question"])
        
        # 创建并等待运行完成
        run_id = create_run(thread_id)
        start_time = time.time()
        
        while time.time() - start_time < 30:  # 超时30秒
            status = get_run_status(thread_id, run_id)
            if status["status"] == "completed":
                break
            time.sleep(1)
        else:
            return jsonify({"code": 408, "error": "请求超时"}), 408
        
        # 获取最新AI回复
        messages = get_messages(thread_id)
        assistant_messages = [
            msg["content"] for msg in messages 
            if msg["role"] == "assistant"
        ]
        
        return jsonify({
            "code": 0,
            "answer": assistant_messages[-1] if assistant_messages else "",
            "sessionId": session_id
        })
        
    except Exception as e:
        app.logger.error(f"处理失败: {str(e)}")
        return jsonify({"code": 500, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)