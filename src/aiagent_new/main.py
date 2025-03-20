from .page.qiaocang import QiaoCang

def create_aiagent(user_name: str) -> dict:
    rsp = QiaoCang().run(user_name)
    if rsp:
        return {"status": "success", "message": "智能体创建成功"}
    return {"status": "error", "message": "智能体创建失败"}

