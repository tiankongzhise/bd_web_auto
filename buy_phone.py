import re
from playwright.sync_api import Playwright, sync_playwright, Page
import login as login_module


class BuyPhone:
    def __init__(self, playwright: Playwright) -> None:
        self.playwright = playwright
        self.mcc_page = None
    
    def login(self):
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        page = self.context.new_page()
        page = login_module.login(page)
        return page
    def close_popup(self,page:Page):
         #等待页面加载
        try:
            page.wait_for_load_state("networkidle")
        except:
            print(f'页面加载超时')
        # checkbox = page2.get_by_role("checkbox", name="我已阅读并同意《营销通服务协议》以及《数据安全与保密协议》 ​")
        # 处理弹窗
        # 处理协议弹窗
        try:
            agreement_text = page.get_by_text("我已阅读并同意《营销通服务协议》以及《数据安全与保密协议》")
            agreement_text.wait_for(state="visible", timeout=1000)  # 最多等待1秒
            agreement_text.click()
            page.get_by_role("button", name="​ 确定").click()
        except:
            pass  # 如果超时或元素不存在则跳过
        print('跳过保密协议成功')
        try:
            marketing_element = page.get_by_role("strong").filter(has_text="营销通")
            marketing_element.wait_for(state="visible", timeout=1000)  # 最多等待1秒
            marketing_element.click()
        except:
            pass  # 如果超时或元素不存在则跳过

        print('跳过营销通成功')
        # 检测并关闭营销通与爱番番双平台融合通告
        try:
            notice = page.locator("text=【营销通与爱番番双平台融合】")
            notice.wait_for(state="visible", timeout=1000)  # 最多等待3秒
            page.locator("button.one-dialog-close").click()
        except Exception as e:
            pass  # 如果超时或元素不存在则跳过
        
        try:
            dls_icon = page.locator(".dls-icon").first
            dls_icon.wait_for(state="visible", timeout=1000)  # 最多等待3秒
            dls_icon.click()
        except:
            pass #容错

        return page
    
    def target_page(self,user_name:str,project_name:str,page_name:str,item_name:str|None = None):
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
        page2.locator("#menu-tree").get_by_text("电话", exact=True).click()
        return page2

    def buy_phone(self,page:Page,phone_number:str):
        page.get_by_text("号码资源管理").click()
        with page.expect_popup() as page2_info:
            page.get_by_role("button", name="​ 购买服务包").click()
        page2 = page2_info.value
        page2.get_by_role("textbox", name="请选择号码地域").click()
        page2.get_by_role("listitem", name="广东省").click()
        page2.get_by_role("listitem", name="深圳市").click()
        page2.get_by_role("button", name="立即购买").click()
        page2.get_by_role("textbox", name="请输入手机号码").click()
        page2.get_by_role("textbox", name="请输入手机号码").fill("18566120258")
        page2.get_by_role("button", name="提交订单").click()
        page2.get_by_text("搜索推广消费渠道优惠").click()
        page2.get_by_role("button", name="确认付款").click()

    def create_phone_scheme(self,page:Page,scheme_name:str,phone_number:str):
        page.get_by_text("号码资源管理").click()
        with page.expect_popup() as page2_info:
            page.get_by_role("button", name="​ 购买服务包").click()
        page2 = page2_info.value

def run(playwright: Playwright) -> None:
    with page.expect_popup() as page7_info:
        page.get_by_text("金蛛-新账户4").click()
    page7 = page7_info.value
    with page7.expect_popup() as page8_info:
        page7.get_by_role("strong").filter(has_text="营销通").click()
    page8 = page8_info.value
    page8.get_by_role("dialog").get_by_role("button", name="​", exact=True).click()
    page8.locator("#menu-tree").get_by_text("电话", exact=True).click()
    page8.get_by_text("号码资源管理").click()
    with page8.expect_popup() as page9_info:
        page8.get_by_role("button", name="​ 购买服务包").click()
    page9 = page9_info.value
    page9.get_by_role("textbox", name="请选择号码地域").click()
    page9.get_by_role("listitem", name="广东省").click()
    page9.get_by_role("listitem", name="深圳市").click()
    page9.get_by_role("button", name="立即购买").click()
    page9.get_by_role("textbox", name="请输入手机号码").click()
    page9.get_by_role("textbox", name="请输入手机号码").fill("18566120258")
    page9.get_by_role("button", name="提交订单").click()
    page9.get_by_text("搜索推广消费渠道优惠").click()
    page9.get_by_role("button", name="确认付款").click()
    with page9.expect_popup() as page10_info:
        page9.get_by_role("button", name="去应用").click()
    page10 = page10_info.value
    page10.locator("path").first.click()
    page10.get_by_text("电话", exact=True).click()
    page10.get_by_text("号码资源管理").click()
    page10.get_by_text("18466200531").click()
    page10.get_by_text("18466200531").dblclick()
    page10.get_by_text("18466200531").click()
    page10.get_by_text("18466200531").click()
    page10.get_by_text("方案管理").click()
    page10.get_by_role("button", name="​ 新建电话方案").click()
    page10.get_by_role("textbox", name="用于基木鱼页面引用电话方案，不超过30个字符").click()
    page10.get_by_role("textbox", name="用于基木鱼页面引用电话方案，不超过30个字符").click()
    page10.get_by_role("textbox", name="用于基木鱼页面引用电话方案，不超过30个字符").fill("18466200531转18806662618")
    page10.get_by_role("textbox", name="请输入手机号").click()
    page10.get_by_role("textbox", name="请输入手机号").fill("18806662618")
    page10.get_by_role("button", name="​ 生成推荐方案").click()
    page10.locator("div").filter(has_text=re.compile(r"^智能电话-私有自费网民拨打显示您的私有中间号，有效期内拨打私号均可联系到您$")).nth(1).click()
    page10.get_by_role("button", name="​ 下一步").click()
    page10.locator("div").filter(has_text=re.compile(r"^客服微信启用通话结束向网民发送挂机短信，增加添加微信好友的通路$")).locator("span").nth(1).click()
    page10.locator("div").filter(has_text=re.compile(r"^客服微信启用通话结束向网民发送挂机短信，增加添加微信好友的通路$")).get_by_label("启用").check()
    page10.get_by_text("请选择已购买号码").click()
    page10.get_by_text("广东省, 深圳市").click()
    page10.locator("div").filter(has_text=re.compile(r"^身份验证启用过滤误拨、低意愿客户，拦截后不让其看到电话号码$")).get_by_label("启用").check()
    page10.get_by_role("button", name="​ 确定").click()
    page10.goto("https://yingxiaotong.baidu.com/vector/user/64951864/component/phone/list")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
