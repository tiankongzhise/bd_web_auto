from playwright.sync_api import Playwright, sync_playwright, Page
import tomllib
import os
import re
from dotenv import load_dotenv
load_dotenv()

class NavigationError(Exception):
    """自定义异常类，用于表示导航失败的错误"""
    pass

class BdWebAutoBase(object):
    def __init__(self, playwright: Playwright) -> None:
        self.playwright = playwright
        self.page = {}
        with open("config.toml", "rb") as f:
            self.config = tomllib.load(f)
    
    def login(self):
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        page = self.context.new_page()
        page.goto("https://cas.baidu.com/?tpl=www2&fromu=https%3A%2F%2Fwww2.baidu.com%2Fcommon%2Fappinit.ajax")
        page.get_by_role("textbox", name="请输入账号").click()
        page.get_by_role("textbox", name="请输入账号").fill(os.getenv("BDCC_USERNAME"))
        page.get_by_role("textbox", name="请输入密码").click()
        page.get_by_role("textbox", name="请输入密码").fill(os.getenv("BDCC_PASSWORD"))
        page.get_by_role("button", name="登录").click()
        return page
    
    
    def close_popup(self,page:Page):
        try:
            agreement_text = page.get_by_text("我已阅读并同意《营销通服务协议》以及《数据安全与保密协议》")
            agreement_text.wait_for(state="visible", timeout=1000)  # 最多等待1秒
            agreement_text.click()
            page.get_by_role("button", name="​ 确定").click()
        except Exception as e:
            print(f'保密协议超时或出错{e}')
        print('处理保密协议成功')
        try:
            marketing_element = page.get_by_role("strong").filter(has_text="营销通")
            marketing_element.wait_for(state="visible", timeout=3000)  # 最多等待1秒
            marketing_element.click()
        except Exception as e:
            print(f'营销通超时或出错{e}')

        print('处理营销通弹窗成功')
        # 检测并关闭营销通与爱番番双平台融合通告
        try:
            notice = page.locator("text=【营销通与爱番番双平台融合】")
            notice.wait_for(state="visible", timeout=3000)  # 最多等待3秒
            page.locator("button.one-dialog-close").click()
        except Exception as e:
            print(f'双平台融合通告超时或出错{e}')
        
        print('处理双平台融合通告成功')
        
        try:
            dls_icon = page.locator(".dls-icon").first
            dls_icon.wait_for(state="visible", timeout=3000)  # 最多等待3秒
            dls_icon.click()
        except Exception as e:
           print(f'弹窗超时或出错:{e}')
        
        print('处理弹窗成功')

        return page
        
    def user_page(self,user_name:str,user_center:Page|None = None)->Page:
        if user_center is None:
            if self.page.get('user_center') is None:
                self.page['user_center'] = self.login()
            user_center = self.page['user_center']
        with user_center.expect_popup() as user_page_info:
            user_center.get_by_text(user_name).click()
        user_page = user_page_info.value
        self.page[f'{user_name}_page'] = user_page
        return user_page
    
    def navigate_to_marketing(self, page: Page) -> Page:
        """
        从当前页面点击营销通，访问营销通系统
        
        Args:
            page: 当前页面对象
            
        Returns:
            营销通系统页面对象
        """
        try:
            # 点击营销通入口
            with page.expect_popup() as marketing_info:
                page.get_by_role("strong").filter(has_text="营销通").click()
            marketing_page = marketing_info.value
            print("成功导航到营销通系统")
            self.page['marketing_page'] = marketing_page
            return marketing_page
        except Exception as e:
            raise(f"导航到营销通系统失败: {e}")
    
    def navigate_to_jmy_from_page(self, page: Page) -> Page:
        """
        从当前页面点击基木鱼，访问基木鱼自建站系统
        
        Args:
            page: 当前页面对象
            
        Returns:
            基木鱼系统页面对象
        """
        try:
            # 点击营销通入口
            with page.expect_popup() as jmy_info:
                # page.get_by_role("strong").filter(has_text="基木鱼").click()
                page.get_by_role("strong").filter(has_text=re.compile(r"^基木鱼$")).click()
            jmy_page = jmy_info.value
            print("成功导航到基木鱼系统")
            self.page['jmy_page'] = jmy_page
            return jmy_page
        except Exception as e:
            raise NavigationError(f"导航到基木鱼系统失败: {e}")

    def navigate_to_jmy(self, user_name:str) -> Page:
        """
        通过用户名直接访问基木鱼自建站系统，跳过可能存在的初始化智能建站
        
        Args:
            用户名: 账户名称
            
        Returns:
            基木鱼系统页面对象
        """
        user_id = self.config['user_map'][user_name]
        try:
            # 点击营销通入口
            jmy_page = self.context.new_page()
            jmy_page.goto(f'https://wutong.baidu.com/platform/user/{user_id}/home?ucUserId={user_id}')
            print("成功导航到基木鱼系统")
            self.page['jmy_page'] = jmy_page
            return jmy_page
        except Exception as e:
            raise NavigationError(f"导航到基木鱼系统失败: {e}")
    def close(self):
        self.context.close()
        self.browser.close()
        self.page = {}
        
