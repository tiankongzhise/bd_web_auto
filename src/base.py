from playwright.sync_api import Playwright, Page,sync_playwright
from tkzs_bd_db_tool import get_session,models
from logger_config import logger
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
        self.user_name = None
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
            user_center.get_by_text(user_name).first.click()
        user_page = user_page_info.value
        self.page[f'{user_name}_page'] = user_page
        self.user_name = user_name
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
        
class BrowserManager:
    def __init__(self)->None:
        self.playwright = sync_playwright().start()
        
    def launch_browser(self)->Playwright:
        return self.playwright.chromium.launch(headless=False)

    def close(self)->None:
        self.playwright.stop()

class PageSession:
    def __init__(self, context)->None:
        self.context = context
        self.pages = {}
        
    def new_page(self, name:str)->Page:
        self.pages[name] = self.context.new_page()
        return self.pages[name]
    
    def new_page_wait(self, name:str,page:Page):
        try:
            page.wait_for_timeout(5000)
        except Exception as e:
            logger.error(f'等待页面加载失败:{e}')
            raise(f'等待页面加载失败:{e}')
        self.pages[name] = self.context.new_page()
        return self.pages[name]
    
class AuthManager:
    def __init__(self, page:Page):
        self.page = page
        
    def baidu_login(self, username:str|None = None, password:str|None = None)->Page:
        '''
        百度ADS登录，如果未传入用户名密码，则从环境变量中获取
        '''
        self.page.goto("https://cas.baidu.com/?tpl=www2&fromu=https%3A%2F%2Fwww2.baidu.com%2Fcommon%2Fappinit.ajax")
        self.page.get_by_role("textbox", name="请输入账号").fill(username or os.getenv("BDCC_USERNAME"))
        self.page.get_by_role("textbox", name="请输入密码").fill(password or os.getenv("BDCC_PASSWORD"))
        self.page.get_by_role("button", name="登录").click()
        return self.page

class AdsAccountManager:
    def __init__(self, page:Page):
        self.page = page
    
    def get_account_mapping(self)->dict:
        try:
            with get_session() as session:
                rsp = session.query(models.BdAdCenterBindTable).all()
                account_map = models.BdAdCenterBindTable.to_account_mapping(rsp)
            return account_map
        except Exception as e:
            logger.error(f'获取账户映射失败{e}')
    
    def goto_account_page(self,user_name:str)->Page:
        account_maping = self.get_account_mapping()
        user_id = account_maping[user_name]
        try:
            self.page.goto(f'https://tuiguang.baidu.com/oneWeb.html?userid={user_id}')
            self.page.wait_for_load_state(state='load',timeout=10000)
            logger.info(f'导航到账户{user_name}页面成功')
            return self.page
        except Exception as e:
            logger.error(f'导航到账户页面失败{e}')
    
    def select_max_account(self)->Page:
        logger.debug('开始选择100条/页面')
        # 定位下拉框并点击
        dropdown = self.page.locator('div.one-pagination .one-select-medium.one-main.one-select.one-select-enabled')
        dropdown.click()
        logger.debug('下拉框点击成功')
        # 定位并选择 "100条/页" 选项
        option = self.page.locator('li.one-select-dropdown-menu-item >> span', has_text='100条/页')
        option.click()
        logger.debug('选择100条/页成功')
        self.page.wait_for_load_state("networkidle",timeout=10000)
        logger.debug('切换到100条/页面成功')
    
    def click_into_user_page(self,user_name:str):
        logger.debug(f"点击进入用户页面：{user_name}")
        with self.page.expect_popup() as user_page_info:
            self.page.locator('span', has_text=re.compile(r'^{user_name}$'.format(user_name=user_name))).click()
            logger.debug(f"点击进入用户页面：{user_name}成功")
        user_page = user_page_info.value
        user_page.wait_for_load_state("load",timeout=10000)
        logger.debug(f"切换到用户页面：{user_name}成功")
        return user_page
        
    def run(self,user_name:str):
        try:
            logger.info(f"开始切换到用户页面：{user_name}")
            self.select_max_account()
            user_page = self.click_into_user_page(user_name)
            logger.info(f"切换到用户页面：{user_name}成功")
        except Exception as e:
            logger.error(f"切换到用户页面：{user_name}失败，原因：{e}")
            raise e
        return user_page
        
        
        
        
class AutoAdsSession:
    def __init__(self,browser_manager: BrowserManager|None = None):
        self.browser_manager = browser_manager or BrowserManager()
        self.user_name = None
        self.browser = None
        self.context = None
        self.page_session:PageSession|None = None

    def __enter__(self):
        self.browser = self.browser_manager.launch_browser()
        self.context = self.browser.new_context()
        self.page_session = PageSession(self.context)

        # 执行逻辑
        main_page = self.page_session.new_page("main")
        AuthManager(main_page).baidu_login()
        return self

    def get_account_page(self,user_name:str,*kwargs)->PageSession:
        center_page = self.page_session.pages['main']
        self.user_name = user_name
        user_page = AdsAccountManager(center_page).run(self.user_name)

        return user_page

    def __exit__(self, exc_type, exc_value, traceback):
        # 确保资源释放
        self.context.close()
        self.browser_manager.close()
