import json
import os.path
from datetime import datetime
from typing import Any
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from openai import OpenAI
import logging
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db import AiPreset,session_factory

# 创建FastAPI实例
app = FastAPI(title="AI智能伴侣", version="1.0.0")

# 会话数据目录
SESSIONS_DIR = "sessions"
# 常量
PRESETS_FILE_PATH = "data/companion_presets.json"
# 系统提示词模板
SYSTEM_PROMPT_TEMPLATE = """你叫 %s，现在是用户的真实伴侣，请完全代入伴侣角色。
    规则：
        1. 每次只回1条消息
        2. 禁止任何场景或状态描述性文字
        3. 匹配用户的语言
        4. 回复简短，像微信聊天一样
        5. 有需要的话可以用❤️🌸等emoji表情
        6. 用符合伴侣性格的方式对话
        7. 回复的内容, 要充分体现伴侣的性格特征
        8. 不要太肉麻（比如想你之类的，就日常聊天）
    伴侣性格：
        - %s
    你必须严格遵守上述规则来回复用户。
    """

# 初始化OpenAI客户端
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url="https://api.deepseek.com")
# 配置日志
logging.basicConfig(
    level=logging.INFO, # 只会输出当前日志级别及以上日志级别的日志
    format="%(asctime)s - %(levelname)s - [%(filename)s : %(lineno)d] - %(message)s"
)


if not os.path.exists(SESSIONS_DIR):
    os.mkdir(SESSIONS_DIR)

# ==================== 工具函数 ====================
def generate_session_name():
    """生成会话标识"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def get_session_path(session_name: str) -> str:
    """获取会话文件路径"""
    return os.path.join(SESSIONS_DIR, f"{session_name}.json")

async def get_session():
    session = session_factory()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


# 数据模型
# 统一响应模型
class ApiResponse(BaseModel):
    code: int = 200
    message: str = "操作成功"
    data: Any | None = None

# 新建回话请求模型
class CreateSessionRequest(BaseModel):
    nick_name: str
    nature: str

class ChatRequest(BaseModel):
    session_name: str     #  会话标识
    message: str        #  用户消息
    nick_name: str      #  伴侣昵称
    nature: str         #  伴侣性格

@app.get("/")
async def root():
    # print("访问项目首页")
    logging.info("访问项目首页")

@app.get("/api/presets", summary="获取预设伴侣信息列表")
async def presets(session:AsyncSession = Depends(get_session)):
    result = await session.execute(select(AiPreset).order_by(AiPreset.sort_order.asc()))
    presets_list =jsonable_encoder((result.scalars().all()))
    return ApiResponse(code=200, message="获取预设伴侣信息成功", data=presets_list)



@app.post("/api/sessions", summary="创建新会话", response_model=ApiResponse)
def create_session(request: CreateSessionRequest) -> ApiResponse:
    """创建新会话"""
    #print(f"创建会话: {request}")
    logging.info(f"创建会话: {request}")
    session_name = generate_session_name()
    session_data = {
        "nick_name": request.nick_name,
        "nature": request.nature,
        "session_name": session_name,
        "messages": []
    }
    with open(get_session_path(session_name), "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    return ApiResponse(code=200, message="创建会话成功", data=session_name)


@app.post("/api/chat", summary="与AI交互", response_model=ApiResponse)
def chat(request: ChatRequest) -> ApiResponse:
    """与AI对话（非流式）"""
    logging.info(f"与AI交互: {request.session_name}:{request.message}")

    # 1. 加载json文件中的会话数据
    session_path = get_session_path(request.session_name)
    with open(session_path, "r", encoding="utf-8") as f:
        session_data = json.load(f)

    # 2. 构建系统提示词
    system_prompt = SYSTEM_PROMPT_TEMPLATE % (request.nick_name, request.nature)

    # 3. 构建消息列表
    messages = [{"role": "system", "content": system_prompt}]
    for msg in session_data["messages"]:
        messages.append(msg)
    messages.append({"role": "user", "content": request.message})

    # print(f"----> 请求的会话信息: {messages}")
    logging.info(f"----> 请求的会话信息: {messages}")

    # 4. 调用DeepSeek API
    response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=messages,
            stream=False
    )

    # 5. 获取响应的数据
    ai_response = response.choices[0].message.content
    logging.info(f"<---- AI大模型响应的数据: {ai_response}")

    # 6. 更新消息列表中的消息
    messages.pop(0)
    messages.append({"role": "assistant", "content": ai_response})
    session_data["messages"] = messages

    session_data["nature"] = request.nature
    session_data["nick_name"] = request.nick_name

    # print(f"更新后的会话信息: {session_data}")
    logging.info(f"更新后的会话信息: {session_data}")

    # 7. 保存会话信息到json文件中
    with open(session_path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    # 8. 返回数据
    return ApiResponse(code=200, message="请求成功", data=ai_response)


@app.get("/api/sessions", summary="获取会话列表", response_model=ApiResponse)
def list_sessions() -> ApiResponse:
    """获取所有会话列表（按时间降序）"""
    # print("获取会话列表")
    logging.info("获取会话列表")
    session_list = []
    if os.path.exists(SESSIONS_DIR):
        for filename in os.listdir(SESSIONS_DIR):
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True)
    return ApiResponse(code=200, message="获取会话列表成功", data=session_list)

@app.get("/api/sessions/{session_name}", summary="获取指定会话信息", response_model=ApiResponse)
def get_session_message(session_name: str) -> ApiResponse:
    """获取指定会话信息"""
    # print(f"获取会话信息: {session_name}")
    logging.info(f"获取会话信息: {session_name}")
    session_path = get_session_path(session_name)
    if not os.path.exists(session_path):
        return ApiResponse(code=404, message="会话不存在")
    else:
        with open(session_path, "r", encoding="utf-8") as f:
            session_data = json.load(f)
        return ApiResponse(code=200, message="获取会话信息成功", data=session_data)

@app.delete("/api/sessions/{session_name}", summary="删除指定会话", response_model=ApiResponse)
def delete_session(session_name: str) -> ApiResponse:
    """删除指定会话"""
    #print(f"删除会话: {session_name}")
    logging.info(f"删除会话: {session_name}")
    session_path = get_session_path(session_name)
    if not os.path.exists(session_path):
        return ApiResponse(code=404, message="会话不存在")
    else:
        os.remove(session_path)
        return ApiResponse(code=200, message="删除会话成功")


# 启动服务
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)