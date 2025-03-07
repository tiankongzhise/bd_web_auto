from base import BdWebAutoBase
from playwright.sync_api import sync_playwright, Page
import os
from dotenv import load_dotenv
from tqdm import tqdm
load_dotenv()


class YiliaoAuth(BdWebAutoBase):
    def __init__(self, playwright):
        super().__init__(playwright)
        
    def yiliao_auth(self,marketing_page:Page):
        marketing_page.get_by_text("通用咨询").click()
        marketing_page.get_by_text("客服账号授权").click()
        marketing_page.get_by_role("button", name="​ 新增授权").click()
        with marketing_page.expect_popup() as auth_page_info:
            marketing_page.get_by_role("dialog").get_by_text("全时易聊").click()
        auth_page = auth_page_info.value
        auth_page.get_by_role("textbox", name="请输入客服ID").click()
        auth_page.get_by_role("textbox", name="请输入客服ID").fill(os.getenv('YILIAO_USERNAME'))
        auth_page.get_by_role("textbox", name="请输入客服密码").click()
        auth_page.get_by_role("textbox", name="请输入客服密码").fill(os.getenv('YILIAO_PASSWORD'))
        auth_page.locator("label").click()
        auth_page.get_by_role("button", name="立 即 授 权").click()
        marketing_page.close()
        return auth_page
    
    def delay(self,page:Page,err_msg:str = '延迟完成',seconds:int = 5) -> None:
        try:
            page.wait_for_load_state('networkidle',timeout=seconds*1000)
        except Exception:
            print(err_msg)
    def run(self,user_name:str)->None:
        func_str = '易聊授权'
        try:
            if self.page.get('user_center') is None:
                self.page['user_center'] = self.login()
            center_page = self.page['user_center']
            print(f'{user_name}{func_str}登录成功')
        except Exception as e:
            return {user_name:f'{func_str}登录失败:{e}'}
        
        try:
            user_page = self.user_page(user_name,center_page)
            print(f'{user_name}{func_str}获取用户页成功')
        except Exception as e:
            return {user_name:f'{func_str}获取账户页失败:{e}'}
        
        self.delay(user_page,f'{user_name}{func_str}获取用户页超时,容错')

        try:
            marketing_page = self.navigate_to_marketing(user_page)
            print(f'{user_name}{func_str}获取营销通页成功')
        except Exception as e:
            return {user_name:f'{func_str}获取营销通页失败:{e}'}

        self.delay(marketing_page,f'{user_name}{func_str}获取营销通页超时,容错')
        
        try:
            marketing_page = self.close_popup(marketing_page)
            print(f'{user_name}{func_str}关闭弹窗成功')
        except Exception as e:
            return {user_name:f'{func_str}关闭弹窗失败:{e}'}
        try:
            auth_page = self.yiliao_auth(marketing_page)
            print(f'{user_name}{func_str}获取易聊授权成功')
        except Exception as e:
            return {user_name:f'{func_str}授权失败:{e}'}
        try:
            auth_page.wait_for_load_state("networkidle",timeout=10000)
            auth_page.close()
            marketing_page.close()
            user_page.close()
            print('正常结束')
        except Exception as e:
            return {user_name:f'{func_str}授权成功，但在收尾时关闭页失败:{e}'}
        return {user_name:'易聊授权成功'}



if __name__ == '__main__':
    user_list = ['金蛛-新账户4']
    result = []
    with sync_playwright() as playwright:
        yiliao_auth = YiliaoAuth(playwright)
        for user_name in tqdm(user_list,desc="易聊授权"):
             result.append(yiliao_auth.run(user_name))
        print(result)
        yiliao_auth.close()
