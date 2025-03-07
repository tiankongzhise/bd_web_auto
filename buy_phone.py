import re
from playwright.sync_api import Playwright, sync_playwright, Page
import login as login_module
import tomllib
from tqdm import tqdm

class BuyPhone:
    def __init__(self, playwright: Playwright) -> None:
        self.playwright = playwright
        self.mcc_page = None
        with open("config.toml", "rb") as f:
            config = tomllib.load(f)
        self.call_phone_number = config['call_phone_number']
    
    def login(self):
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        page = self.context.new_page()
        page = login_module.login(page)
        return page
    def close_popup(self,page:Page):
         #等待页面加载
        try:
            page.wait_for_load_state("networkidle",timeout=10000)
        except Exception as e:
            print(f'页面加载超时: {e}')
        # checkbox = page2.get_by_role("checkbox", name="我已阅读并同意《营销通服务协议》以及《数据安全与保密协议》 ​")
        # 处理弹窗
        # 处理协议弹窗
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
            marketing_element.wait_for(state="visible", timeout=1000)  # 最多等待1秒
            marketing_element.click()
        except Exception as e:
            print(f'营销通超时或出错{e}')

        print('处理营销通弹窗成功')
        # 检测并关闭营销通与爱番番双平台融合通告
        try:
            notice = page.locator("text=【营销通与爱番番双平台融合】")
            notice.wait_for(state="visible", timeout=1000)  # 最多等待3秒
            page.locator("button.one-dialog-close").click()
        except Exception as e:
            print(f'双平台融合通告超时或出错{e}')
        
        print('处理双平台融合通告成功')
        
        try:
            dls_icon = page.locator(".dls-icon").first
            dls_icon.wait_for(state="visible", timeout=1000)  # 最多等待3秒
            dls_icon.click()
        except Exception as e:
           print(f'弹窗超时或出错:{e}')
        
        print('处理弹窗成功')

        return page
    
    def target_page(self,user_name:str,project_name:str,item_name:str):
        if self.mcc_page is None:
            self.mcc_page = self.login()

        with self.mcc_page.expect_popup() as page1_info:
            self.mcc_page.get_by_text(user_name).click()
        page1 = page1_info.value
        with page1.expect_popup() as page2_info:
            page1.get_by_role("strong").filter(has_text=project_name).click()
            page2 = page2_info.value
        print('换页面')
        page2 = self.close_popup(page2)
        page2.locator("#menu-tree").get_by_text(item_name, exact=True).click()
        print('电话方案页面跳转成功')
        return page2

    def buy_phone(self,page:Page,phone_number:str = '18566120258'):
        page.get_by_text("号码资源管理").click()
        with page.expect_popup() as page2_info:
            page.get_by_role("button", name="​ 购买服务包").click()
        page2 = page2_info.value
        page2.get_by_role("textbox", name="请选择号码地域").click()
        

        
        page2.get_by_role("listitem", name="广东省").click()
        page2.get_by_role("listitem", name="深圳市").click()
        try:
            # 在此处等待元素出现
            page2.wait_for_selector("text=深圳市",timeout=5000)  # 等待包含 "深圳市" 的文本元素
        except TimeoutError:
            print("等待深圳市元素超时，元素未在指定时间内出现")
        except Exception as e:
            print(f"发生其他错误: {e}")
                #在此处等待3秒钟
        page2.wait_for_timeout(1000)
        
        page2.get_by_role("button", name="立即购买").click()
        page2.get_by_role("textbox", name="请输入手机号码").click()
        page2.get_by_role("textbox", name="请输入手机号码").fill(phone_number)
        page2.wait_for_timeout(1000)
        page2.get_by_role("button", name="提交订单").click()
        page2.get_by_text("搜索推广消费渠道优惠").click()
        page2.wait_for_timeout(1000)
        page2.get_by_role("button", name="确认付款").click()
        page2.wait_for_timeout(1000)
        with page2.expect_popup() as page3_info:
            page2.get_by_role("button", name="去应用").click()
        page3 = page3_info.value
        print('电话购买成功，正在设置电话方案')
        return page3
    def extract_phone_number(self,page: Page) -> str:
        print('正在提取号码')
        # 使用 locator 定位号码所在的元素
        phone_number_element = page.locator(".one-table-row-body-cell.one-table-row-first-cell")
        print('locator 定位成功')
        # 获取元素的文本内容
        phone_number = phone_number_element.text_content().strip()
        print('提取号码成功')
        
        return phone_number
    
    def enable_wechat_feature(self,page: Page):
        try:
            # 定位复选框元素
            checkbox = page.locator(".editor-service-wechat .one-checkbox-input")
            
            # 等待复选框可见
            checkbox.wait_for(state="visible", timeout=5000)
            
            # 如果复选框未勾选，则勾选它
            if not checkbox.is_checked():
                checkbox.click()
                print("微信功能复选框已勾选")
            else:
                print("微信功能复选框已处于勾选状态")
        except TimeoutError:
            print("等待微信功能复选框超时，元素未在指定时间内出现")
        except Exception as e:
            print(f"勾选微信功能复选框时发生错误: {e}")
    
    def select_smart_private_phone(self,page: Page):
        try:
            # 定位包含 "智能电话-私有" 文本的元素
            smart_private_element = page.locator("div.menu-card:has-text('智能电话-私有')")
            
            # 等待元素可见
            smart_private_element.wait_for(state="visible", timeout=5000)
            
            # 点击元素
            smart_private_element.click()
            print("成功选中智能电话-私有")
        except TimeoutError:
            print("等待智能电话-私有元素超时，元素未在指定时间内出现")
        except Exception as e:
            print(f"选中智能电话-私有时发生错误: {e}")
    def create_phone_scheme(self,page:Page,call_phone_number:str|None = None):
        if call_phone_number is None:
            call_phone_number = self.call_phone_number
        page.get_by_text("号码资源管理").click()
        print('进入号码咨询管理')
        vir_phone_number = self.extract_phone_number(page)
        print(f'vir_phone_number获取正常:{vir_phone_number}')
        page.get_by_text("方案管理").click()
        print('进入方案管理')
        page.get_by_role("button", name="​ 新建电话方案").click()
        # page.get_by_role("textbox", name="用于基木鱼页面引用电话方案，不超过30个字符").click()
        page.get_by_role("textbox", name="用于基木鱼页面引用电话方案，不超过30个字符").click()
        page.get_by_role("textbox", name="用于基木鱼页面引用电话方案，不超过30个字符").fill(f"{vir_phone_number}转{call_phone_number}")
        page.get_by_role("textbox", name="请输入手机号").click()
        page.get_by_role("textbox", name="请输入手机号").fill(call_phone_number)
        page.get_by_role("button", name="​ 生成推荐方案").click()
        
        page.wait_for_timeout(3000)
        self.select_smart_private_phone(page)
        
        page.get_by_role("button", name="​ 下一步").click()
        # page.locator("div").filter(has_text=re.compile(r"^客服微信启用通话结束向网民发送挂机短信，增加添加微信好友的通路$")).locator("span").nth(1).click()
        # page.locator("div").filter(has_text=re.compile(r"^客服微信启用通话结束向网民发送挂机短信，增加添加微信好友的通路$")).get_by_label("启用").check()
        self.enable_wechat_feature(page)
        page.get_by_text("请选择已购买号码").click()
        page.get_by_text("广东省, 深圳市").click()
        page.locator("div").filter(has_text=re.compile(r"^身份验证启用过滤误拨、低意愿客户，拦截后不让其看到电话号码$")).get_by_label("启用").check()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="​ 确定").click()
        page.wait_for_timeout(3000)
        return page

    def run(self,user_name) -> dict:
        try:
            page = self.target_page(user_name,'营销通','电话')
            page = self.buy_phone(page)
            self.context.close()
            self.browser.close()
            self.mcc_page = None
            page = self.target_page(user_name,'营销通','电话')
            page = self.create_phone_scheme(page)
            return {user_name:'电话方案创建成功'}
        except Exception as e:
            print(f'电话方案创建失败:{e}')
            return {user_name:f'电话方案创建失败:{e}'}
        finally:
            self.context.close()
            self.browser.close()
            self.mcc_page = None
            
        
        



with sync_playwright() as playwright:
    user_list = ["金蛛-BCSP"] #
    result = []
    by_phone = BuyPhone(playwright)
    for user_name in tqdm(user_list,desc="电话方案创建"):
        result.append(by_phone.run(user_name))
    print(result)
