from base import BdWebAutoBase
from playwright.sync_api import sync_playwright, Page
import os
import re
from dotenv import load_dotenv
from tqdm import tqdm
load_dotenv()


class YxtDirectConsult(BdWebAutoBase):
    def __init__(self, playwright):
        super().__init__(playwright)
    

    def create_shop_card(self,consult_page:Page):
        ...

    def create_direct_consult(self,consult_page:Page):
    
        consult_page.get_by_text("通用咨询").click()
        try:
            consult_page.wait_for_selector("一跳",timeout=5000)
            print("已经人工创建")
            return consult_page
        except Exception as e:
            print(f'未发现人工创建')
        consult_page.get_by_role("button", name="​ 新建咨询方案").click()
        consult_page.get_by_role("button", name="​ 创建").click()
        consult_page.get_by_role("textbox", name="咨询方案名称").click()
        consult_page.get_by_role("textbox", name="咨询方案名称").fill("一跳")
        consult_page.get_by_text("请选择客服账号").nth(1).click()
        consult_page.get_by_text("全时易聊").click()
        consult_page.get_by_text("请选择一级").nth(1).click()
        consult_page.get_by_role("option", name="百度基木鱼接待组").click()
        consult_page.get_by_role("button", name="​ 下一步").click()
        consult_page.get_by_role("button", name="​ 新建商家卡片").click()
        consult_page.get_by_role("textbox", name="卡片名称").click()
        consult_page.get_by_role("textbox", name="卡片名称").fill("北大青鸟深圳总校")
        try:
            consult_page.wait_for_selector("text=商家卡片名称重复",timeout=2000)
            print("已经人工创建")
            consult_page.get_by_role("button", name="​", exact=True).nth(1).click()
            consult_page.get_by_role("dialog").get_by_role("button", name="​ 确定").click()
        except Exception as e:
            print(f'未发现人工创建')
            consult_page.locator("span").filter(has_text="请上传长图（建议1140*500，最大1M），最多上传5").get_by_role("img").click()
            consult_page.get_by_role("button", name="​ 本地上传").click()
            consult_page.get_by_role("dialog").filter(has_text="上传图片 图片格式：JPG、JPEG、PNG、BMP、").get_by_label("关闭").set_input_files('https://jmy-pic.baidu.com/0/pic/915332669_-2084204044_-569106030.png')
            consult_page.wait_for_timeout(5000)
            consult_page.get_by_role("button", name="​ 确定").nth(2).click()
            consult_page.get_by_role("dialog").get_by_role("button", name="​ 确定").click()
            consult_page.get_by_role("textbox", name="卡片标题").click()
            consult_page.get_by_role("textbox", name="卡片标题").fill("北大青鸟深圳总校")
            consult_page.get_by_role("textbox", name="卡片内容").click()
            consult_page.get_by_role("textbox", name="卡片内容").fill("专注IT职业教育26年,18门专业零基础可学,全程指导小班 制实操，入学签订就业协议，毕业推荐就业")
            consult_page.wait_for_timeout(2000)
            consult_page.get_by_role("button", name="​ 确定").click()
        consult_page.get_by_text("请选择或输入名称").click()
        consult_page.get_by_role("listitem", name="高级图文卡片").click()
        consult_page.get_by_text("北大青鸟深圳总校").click()
        consult_page.get_by_role("banner").filter(has_text="品牌优势卡展示商家服务特色，突出优势标签信息").get_by_role("switch").click()
        consult_page.get_by_text("请选择或输入名称").nth(1).click()
        consult_page.get_by_text("北大青鸟", exact=True).click()
        consult_page.locator("div:nth-child(2) > .item-card-wrap-item > .item-card-wrap-item-label > .item-card-wrap-item-radio > .one-radio-group > .one-radio-group-items > label:nth-child(3) > .one-radio > .one-radio-inner").click()
        # consult_page.get_by_text("不选择").nth(1).click()
        # consult_page.get_by_text("不选择").nth(1).click()
        consult_page.get_by_text("不选择").nth(1).click()
        consult_page.get_by_role("button", name="​ 下一步").click()
        consult_page.get_by_role("banner").filter(has_text="欢迎语访客进入后自动显示的问候语，为保障体验，如未设置则展示默认欢迎语").get_by_role("switch").click()
        # 在 create_direct_consult 方法中替换原有定位
        welcome_selector = """
        div.form-consult-senior-welcomeword-rich-edit-content 
        div.w-e-text[contenteditable='true']
        """
        consult_page.locator(welcome_selector).fill(
            "您好，是想咨询什么专业呢？如果比较迷茫也可以直接让老师给你推荐专业。"
        )
        consult_page.get_by_text("快捷咨询底部常驻按钮，访客点击按钮即可获得相关信息").click()
        consult_page.get_by_role("banner").filter(has_text="快捷咨询底部常驻按钮，访客点击按钮即可获得相关信息").get_by_role("switch").click()
        consult_page.get_by_role("radio", name="表单回复 ​").check()
        consult_page.get_by_text("选择已有表单").click()
        consult_page.get_by_text("请选择或输入名称").nth(1).click()
        consult_page.get_by_role("option", name="咨询-预约看校").click()
        consult_page.get_by_role("textbox", name="请输入按钮文案，最多10个字符").click()
        consult_page.get_by_role("textbox", name="请输入按钮文案，最多10个字符").fill("预约看校")
        consult_page.get_by_text("添加快捷咨询").click()
        consult_page.get_by_text("添加快捷咨询").click()
        consult_page.locator("div").filter(has_text=re.compile(r"^添加快捷咨询$")).get_by_role("img").click()
        consult_page.locator("div").filter(has_text=re.compile(r"^\*回复内容图文回复文字回复页面跳转表单回复卡券发放热门商品请选择或输入名称$")).get_by_label("表单回复").check()
        consult_page.locator("div").filter(has_text=re.compile(r"^\*回复内容图文回复文字回复页面跳转表单回复卡券发放热门商品\*表单方案新建表单选择已有表单\*表单模版请选择预约式表单标题8/50按钮文案8\/30$")).get_by_label("选择已有表单").check()
        consult_page.locator("div:nth-child(2) > div:nth-child(3) > .consult-detail-container-quickconsulting-content > .consult-detail-common-replay > .consult-detail-common-replay-child > .form-reply-wrapper > div:nth-child(2) > .one-select-medium").click()
        consult_page.get_by_role("option", name="咨询-学费补贴").click()
        consult_page.locator("div").filter(has_text=re.compile(r"^\*按钮文案0/10$")).get_by_placeholder("请输入按钮文案，最多10个字符").click()
        consult_page.locator("div").filter(has_text=re.compile(r"^\*按钮文案0/10$")).get_by_placeholder("请输入按钮文案，最多10个字符").click()
        consult_page.locator("div").filter(has_text=re.compile(r"^\*按钮文案0/10$")).get_by_placeholder("请输入按钮文案，最多10个字符").fill("学费补贴")
        consult_page.get_by_role("banner").filter(has_text="电话设置客户可在咨询页设置电话方案、按钮文字等内容").get_by_role("switch").click()
        consult_page.get_by_role("textbox", name="请输入按钮文字，最多10个字符").click()
        consult_page.get_by_role("textbox", name="请输入按钮文字，最多10个字符").fill("咨询电话")
        consult_page.locator(".consult-detail-container-quickconsulting-item > .one-select-medium").click()
        consult_page.get_by_role("option", name="智能-18466200090转").click()
        consult_page.locator("input[name=\"checkbox\"]").check()
        consult_page.get_by_role("button", name="​ 创建").click()
        consult_page.get_by_text("创建成功").click()

    page14.get_by_text("表单回复").nth(1).click()
    page14.get_by_text("选择已有表单").nth(1).click()
    page14.get_by_text("请选择或输入名称").nth(2).click()
    page14.get_by_role("option", name="咨询-学费补贴").locator("span").click()
    page14.locator("div").filter(has_text=re.compile(r"^\*按钮文案0/10$")).get_by_placeholder("请输入按钮文案，最多10个字符").click()


        try:
            consult_page.wait_for_selector("text=创建成功",timeout=5000)
            print("已经自动复制")
        except Exception as e:
            print(f'未发现自动复制')
        finally:
            return consult_page
    
    # def close_popup(self, page:Page):
    #     try:
    #         if 'pageAndShopAiCreatorChat' in page.url:
    #             page.goto(self.page['jmy_page'].url)
    #         page.wait_for_timeout(3000)
    #         page.get_by_role("button", name="​", exact=True).click()
    #         # page.once("dialog", lambda dialog: dialog.dismiss())
    #         # page.get_by_role("button", name="​", exact=True).click()
    #         # super().close_popup(page)
    #         # page.wait_for_timeout(3000)
    #     except Exception as e:
    #         print(f'常见一跳咨询方案关闭弹窗容错，尝试返回')
    #     finally:
    #         return page

    def delay(self,page:Page,err_msg:str = '延迟完成',seconds:int = 5) -> None:
        try:
            page.wait_for_load_state('networkidle',timeout=seconds*1000)
        except Exception:
            print(err_msg)
    def run(self,user_name:str)->None:
        func_str = '创建一跳咨询方案'
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
            yxt_page = self.navigate_to_marketing(user_page)
            print(f'{user_name}{func_str}获取营销通页面成功')
        except Exception as e:
            return {user_name:f'{func_str}获取营销通页面失败:{e}'}

        self.delay(yxt_page,f'{user_name}{func_str}获取营销通超时,容错')
        
        try:
            yxt_page = self.close_popup(yxt_page)
            print(f'{user_name}{func_str}关闭弹窗成功')
        except Exception as e:
            return {user_name:f'{func_str}关闭弹窗失败:{e}'}
        try:
            consult_page = self.create_direct_consult(yxt_page)
            print(f'{user_name}{func_str}复制基木鱼内容成功')
        except Exception as e:
            return {user_name:f'{func_str}授权失败:{e}'}
        try:
            consult_page.wait_for_load_state("networkidle",timeout=10000)
            consult_page.close()
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
