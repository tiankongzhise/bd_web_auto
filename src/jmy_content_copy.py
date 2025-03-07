from base import BdWebAutoBase
from playwright.sync_api import sync_playwright, Page
import os
from dotenv import load_dotenv
from tqdm import tqdm
load_dotenv()


class JmyContentCopy(BdWebAutoBase):
    def __init__(self, playwright):
        super().__init__(playwright)
        
    def jmy_content_copy(self,jmy_page:Page):
        with jmy_page.expect_popup() as content_info:
            jmy_page.get_by_text("内容中心").click()
        content_page = content_info.value
        content_page.locator("li:nth-child(2) > .one-menu-item-span").click()
        try:
            content_page.wait_for_selector("text=复制账号金蛛教育的22篇文章，160个产品，11个问答，",timeout=10000)
            print("已经人工复制")
            return content_page
        except Exception as e:
            print(f'未发现人工复制')
        content_page.get_by_role("button", name="​ 物料共享").click()
        content_page.get_by_role("button", name="​ 复制物料").click()
        content_page.get_by_role("button", name="​ 开始复制").click()
        content_page.get_by_role("button", name="​ 确定").click()
        try:
            content_page.wait_for_selector("text=操作成功，物料开始复制",timeout=10000)
            print("已经自动复制")
        except Exception as e:
            print(f'未发现自动复制')
        finally:
            return content_page
    
    def close_popup(self, page:Page):
        try:
            if 'pageAndShopAiCreatorChat' in page.url:
                page.goto(self.page['jmy_page'].url)
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="​", exact=True).click()
            # page.once("dialog", lambda dialog: dialog.dismiss())
            # page.get_by_role("button", name="​", exact=True).click()
            # super().close_popup(page)
            # page.wait_for_timeout(3000)
        except Exception as e:
            print(f'基木鱼内容复制关闭弹窗容错，尝试返回')
        finally:
            return page

    def delay(self,page:Page,err_msg:str = '延迟完成',seconds:int = 5) -> None:
        try:
            page.wait_for_load_state('networkidle',timeout=seconds*1000)
        except Exception:
            print(err_msg)
    def run(self,user_name:str)->None:
        func_str = '基木鱼内容复制'
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
            jmy_page = self.navigate_to_jmy(user_name)
            print(f'{user_name}{func_str}获取基木鱼页面成功')
        except Exception as e:
            return {user_name:f'{func_str}获取基木鱼页面失败:{e}'}

        self.delay(jmy_page,f'{user_name}{func_str}获取基木鱼页超时,容错')
        
        try:
            jmy_page = self.close_popup(jmy_page)
            print(f'{user_name}{func_str}关闭弹窗成功')
        except Exception as e:
            return {user_name:f'{func_str}关闭弹窗失败:{e}'}
        try:
            copy_page = self.jmy_content_copy(jmy_page)
            print(f'{user_name}{func_str}复制基木鱼内容成功')
        except Exception as e:
            return {user_name:f'{func_str}授权失败:{e}'}
        try:
            copy_page.wait_for_load_state("networkidle",timeout=10000)
            copy_page.close()
            jmy_page.close()
            user_page.close()
            print('正常结束')
        except Exception as e:
            return {user_name:f'{func_str}授权成功，但在收尾时关闭页失败:{e}'}
        return {user_name:'基木鱼物料复制成功'}



if __name__ == '__main__':
    user_list = ["金蛛-JAVA","金蛛-BCNT","金蛛-PYTHON"]
    result = []
    with sync_playwright() as playwright:
        yiliao_auth = JmyContentCopy(playwright)
        for user_name in tqdm(user_list,desc="基木鱼物料复用授权"):
             result.append(yiliao_auth.run(user_name))
        for item in result:
            print(item)
        yiliao_auth.close()
