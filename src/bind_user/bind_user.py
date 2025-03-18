from src.base import BdWebAutoBase
from src.logger_config import logger
from playwright.sync_api import sync_playwright, Page
from .get_user_info import load_user_info
from tqdm import tqdm

class BindUser(BdWebAutoBase):
    def __init__(self, playwright):
        super().__init__(playwright)

    def navigate_to_bind_user(self, page: Page) -> Page:
        """导航到绑定用户页面"""
        page.locator("a").filter(has_text="账号管理").click()
        page.get_by_role("button", name="新增绑定").click()
        page.get_by_text("登录账号加入").click()
        logger.info("导航到绑定用户页面成功")
        return page
    
    def add_user(self, page: Page, user_name: str,password:str) -> Page:
        page.get_by_role("textbox", name="请输入账号名称").click()
        page.get_by_role("textbox", name="请输入账号名称").fill(user_name)
        page.get_by_role("textbox", name="请输入账号密码").click()
        page.get_by_role("textbox", name="请输入账号密码").fill(password)
        page.get_by_role("textbox", name="请输入右侧验证码").click()
        logger.info("正在输入验证码...")
        page.wait_for_timeout(10000)
        page.get_by_role("button", name="确定").click()
        logger.info("正在点击绑定完成")
        page.wait_for_timeout(2000)
        logger.info("点击绑定完成")
        return page

    def is_bind_success(self,page: Page, timeout=15) -> bool:
        """
        检测绑定成功提示
        :param page: 页面对象
        :param timeout: 最大等待时间（秒）
        :return: 是否存在成功提示
        """
        try:
            # 更精准的定位器建议
            success_locator = page.locator("span").filter(has_text="加入成功").locator("div").nth(2)  # 根据实际DOM结构调整
            
            # 双重验证：存在且可见
            return success_locator.is_visible(timeout=timeout*1000)
            
        except Exception as e:
            logger.warning(f"检测成功提示时发生异常：{str(e)}")
            return False


def bind_user(user_info_path:str|None =None) -> dict:
    user_info_list = load_user_info(user_info_path)
    logger.debug(f"用户信息列表：{user_info_list}")
    success_result = []
    fail_result = []
    with sync_playwright() as playwright:
        bind_user_item = BindUser(playwright)
        login_page = bind_user_item.login()
        bind_user_page = bind_user_item.navigate_to_bind_user(login_page)
        for user_info in tqdm(user_info_list,desc="绑定用户"):
            bind_user_page = bind_user_item.add_user(bind_user_page,user_info['username'],user_info['password'])
            if bind_user_item.is_bind_success(bind_user_page,10):
                success_result.append(user_info)
            else:
                fail_result.append(user_info)
    logger.info(f"成功绑定用户：{success_result}")
    logger.info(f"失败绑定用户：{fail_result}")
