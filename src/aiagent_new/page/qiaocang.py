from playwright import Page
from ..config import Config
import re
def get_qiaocang_page(user_page:Page,user_name)->Page:
    qiaocang_button = user_page.locator("div").filter(has_text=re.compile(r"^巧舱$")).nth(4)
    with user_page.expect_popup() as qiaocang_page_info:
        qiaocang_button.click()
    qiaocang_page = qiaocang_page_info.value
    qiaocang_page.goto(Config.AGENT_CREATION["url"].format(user_id = Config.ACCOUNT_MAPPING[user_page.title()]))
