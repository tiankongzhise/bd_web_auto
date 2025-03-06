from playwright.sync_api import Playwright, sync_playwright, Page
import json
import os
import login as login_module

class CreateForm(object):
    def __init__(self, playwright: Playwright) -> None:
        self.playwright = playwright
        self.mcc_page = None


    def login(self) -> Page:
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        page = self.context.new_page()
        page = login_module.login(page)
        return page

    def page_to_form_page(self,user_name) -> Page:
        if self.mcc_page is None:
            self.mcc_page = self.login()

        with self.mcc_page.expect_popup() as page1_info:
            self.mcc_page.get_by_text(user_name).click()
        page1 = page1_info.value
        with page1.expect_popup() as page2_info:
            page1.get_by_role("strong").filter(has_text="营销通").click()
            page2 = page2_info.value
        print('换页面')
        #等待页面加载
        try:
            page2.wait_for_load_state("networkidle")
        except:
            print(f'页面加载超时')
        # checkbox = page2.get_by_role("checkbox", name="我已阅读并同意《营销通服务协议》以及《数据安全与保密协议》 ​")
        # 处理弹窗
        # 处理协议弹窗
        try:
            agreement_text = page2.get_by_text("我已阅读并同意《营销通服务协议》以及《数据安全与保密协议》")
            agreement_text.wait_for(state="visible", timeout=1000)  # 最多等待1秒
            agreement_text.click()
            page2.get_by_role("button", name="​ 确定").click()
        except:
            pass  # 如果超时或元素不存在则跳过
        print('跳过保密协议成功')
        try:
            marketing_element = page2.get_by_role("strong").filter(has_text="营销通")
            marketing_element.wait_for(state="visible", timeout=1000)  # 最多等待1秒
            marketing_element.click()
        except:
            pass  # 如果超时或元素不存在则跳过

        print('跳过营销通成功')
        # 检测并关闭营销通与爱番番双平台融合通告
        try:
            notice = page2.locator("text=【营销通与爱番番双平台融合】")
            notice.wait_for(state="visible", timeout=1000)  # 最多等待3秒
            page2.locator("button.one-dialog-close").click()
        except Exception as e:
            pass  # 如果超时或元素不存在则跳过
        
        try:
            dls_icon = page2.locator(".dls-icon").first
            dls_icon.wait_for(state="visible", timeout=1000)  # 最多等待3秒
            dls_icon.click()
        except:
            pass #容错
        
        page2.locator("#menu-tree").get_by_text("表单", exact=True).click()
        return page2

    def create_base_form_page(self,page:Page):
        page.get_by_role("button", name="​ 新建表单").click()
        page.get_by_text("基础模板", exact=True).click()
        # 定位基础表单元素
        target = page.locator("div.item-content:has(div.item-title:has-text('基础表单'))")
        # 先滚动到元素位置
        target.scroll_into_view_if_needed()
        # 使用force参数强制hover
        target.hover(force=True)
        # 等待悬浮内容出现
        page.wait_for_timeout(1000)  # 等待1秒
        # 使用更精确的选择器定位创建按钮
        create_button = page.locator("div.item-hover-content:has(div.item-hover-title:has-text('基础表单')) button.item-hover-btn")
        create_button.click()
        return page

    def add_exc_form_item(self,page:Page,exc_info:dict):
        page.get_by_role("button", name="​+ 添加表单项").click()
        page.get_by_text(exc_info['表单项']).click()
        buttons = page.get_by_role("row", name=exc_info['样式']).get_by_role("button").all()
        if len(buttons) > 1:
            buttons[1].click()
        else:
            buttons[0].click()
        exc_stutas = exc_info.get('是否必填','否')
        if exc_stutas == '否':
            switch_button = page.locator(exc_info['样式标识']).first
            switch_button.click()
        page.get_by_role("button", name="​ 确定").click()
        return page


    def create_form(self,page:Page,form_setting:dict):
        # page2.get_by_role("button", name="​ 创建").click()
        # page.locator(".form-container-preview-wrap > .container").click()
        page.get_by_role("textbox", name="请输入表单名称").click()
        page.get_by_role("textbox", name="请输入表单名称").fill(form_setting['表单名称'])
        page.get_by_role("textbox", name="选填，请输入表单标题").click()
        page.get_by_role("textbox", name="选填，请输入表单标题").fill(form_setting['表单标题'])
    
        if form_setting.get('添加表单项'):
            for exc_info in form_setting['添加表单项']:
                page = self.add_exc_form_item(page,exc_info)
        # page2.get_by_role("textbox", name="选填，请输入表单标题").press("ControlOrMeta+a")
        page.get_by_role("textbox", name="请输入提交按钮文案").dblclick()
        page.get_by_role("textbox", name="请输入提交按钮文案").fill(form_setting['提交按钮文案'])
        page.get_by_role("button", name="​ 下一步").click()
        page.get_by_role("textbox", name="请输入提交成功提示语").click()
        page.get_by_role("textbox", name="请输入提交成功提示语").fill(form_setting['提交成功文案'])
        page.get_by_role("button", name="​ 提交").click()
        return page



    def run(self,user_name:str,setting_file_path:str|os.PathLike) -> dict:
        try:
            if isinstance(setting_file_path,str):
                setting_file_path = os.path.abspath(setting_file_path)

            with open(setting_file_path,'r',encoding='utf-8') as f:
                form_setting = json.load(f)

            page = self.page_to_form_page(user_name)
            for form_info in form_setting:
                page = self.create_base_form_page(page)
                page = self.create_form(page,form_info)
            return {user_name:'success'}
        except Exception as e:
            return {user_name:f'fail:{e}'}
        finally:
            self.mcc_page = None
            self.context.close()
            self.browser.close()
        # ---------------------

if __name__ == "__main__":
    with sync_playwright() as playwright:
        result = {}
        user_list = ["金蛛-BCSP"]
        form_setting_file = 'form_setting.json'
        page = CreateForm(playwright)
        for user_name in user_list:
            result.update(page.run(user_name,form_setting_file))
        print(result)
