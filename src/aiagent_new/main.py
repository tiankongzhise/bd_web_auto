from .page.qiaocang import QiaoCang
from playwright.sync_api import  sync_playwright

def create_aiagent(user_name: str) -> dict:
    with sync_playwright() as playwright:
        rsp = QiaoCang(playwright).create_aiagent(user_name)
    if rsp:
        return {"status": "success", "message": "智能体创建成功"}
    return {"status": "error", "message": "智能体创建失败"}

