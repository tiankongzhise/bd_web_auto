from src.base import BdWebAutoBase
from src.logger_config import logger
from playwright.sync_api import Playwright, Page
from ..config import Config
import re

class QiaoCang(BdWebAutoBase):
    def __init__(self, playwright: Playwright) -> None:
        super().__init__(playwright)

    def navigate_to_qiaocang(self,user_page: Page)->Page:
        if self.user_name is None:
            logger.error("navigate_to_qiaocang中self.user_name为空，请检查！")
            raise ValueError("登录异常，请联系管理员排查！")
        qiaocang_button = user_page.locator("div").filter(has_text=re.compile(r"^巧舱$")).nth(4)
        with user_page.expect_popup() as qiaocang_info:
            qiaocang_button.click()
        qiaocang_page = qiaocang_info.value
        qiaocang_url = Config.AGENT_CREATION["url"].format(user_id = Config.ACCOUNT_MAPPING[self.user_name])
        logger.debug(f"巧舱页面url为{qiaocang_url}")
        qiaocang_page.goto(qiaocang_url)
        qiaocang_page.wait_for_load_state('networkidle',timeout=10000)
        return qiaocang_page
    
    def set_agent_name(self, agent_page:Page,name: str) -> None:
        """设置智能体名称
        
        Args:
            name: 智能体名称
        """
        logger.info(f"账户{self.user_name}设置智能体名称: {name}")
        try:
            agent_name_input = agent_page.get_by_role("textbox", name="请输入智能体名称")
            agent_name_input.click()
            agent_name_input.fill(name)
            logger.info(f"账户{self.user_name}设置智能体名称成功")
        except Exception as e:
            logger.error(f"设置智能体名称失败: {e}")
            raise
    def set_avatar(self,agent_page:Page,img_path:str) -> None:
        """设置智能体头像"""
        logger.info(f"账户{self.user_name}设置智能体头像")
        try:
            avatar_setting = agent_page.locator("div").filter(has_text=re.compile(r"^设置头像$")).first
            avatar_setting.click()
            upload_button = agent_page.locator(".vi > div > div > .vi")
            upload_button.click()
            with agent_page.expect_file_chooser() as fc_info:
                # paconsult_pagege.click("button#upload-button")  # 触发文件选择器弹窗
                agent_page.get_by_role("button", name="​ 本地上传").click()
            file_chooser = fc_info.value
            file_chooser.set_files(img_path)  # 设置文件路径
            agent_page.get_by_role("button", name="​ 确定").nth(1).click()
            agent_page.wait_for_timeout(5000)#等待图片处理
            agent_page.get_by_role("button", name="​ 确定").click()
        except Exception as e:
            logger.error(f"账户{self.user_name}设置智能体头像失败: {e}")
            raise
    def set_company_description(self, agent_page:Page,description: str) -> None:
        """设置公司描述
        
        Args:
            description: 公司描述文本
        """
        logger.info(f"账户{self.user_name}设置公司描述")
        try:
            company_desc_input = agent_page.get_by_role("textbox", name="本公司是一家专门做xx的公司，主要经营产品有A、B、C等。")
            company_desc_input.click()
            company_desc_input.fill(description)
        except Exception as e:
            self.logger.error(f"账户{self.user_name}设置公司描述失败: {e}")
            raise
    
    def set_target_users(self, agent_page:Page,target_users: str) -> None:
        """设置目标用户
        
        Args:
            target_users: 目标用户描述
        """
        logger.info(f"账户{self.user_name}设置目标用户")
        try:
            target_users_input = agent_page.get_by_role("textbox", name="目标用户是有xx需求的网民。")
        
            target_users_input.click()
            target_users_input.fill(target_users)
        except Exception as e:
            self.logger.error(f"账户{self.user_name}设置目标用户失败: {e}")
            raise
    def proceed_to_next_step(self,agent_page:Page) -> None:
        """进行下一步"""
        logger.info("点击下一步按钮")
        try:
            next_step_button = agent_page.get_by_text("下一步")
            next_step_button.click()
            agent_page.wait_for_load_state("networkidle",timeout=10000)
        except Exception as e:
            logger.error(f"点击下一步按钮失败: {e}")
            raise
    def check_to_agreement(self,agent_page:Page) -> None:
        '''勾选协议,确定创建智能体'''
        logger.info("勾选协议,确定创建智能体")
        try:
            # 处理同意协议
            try:
                logger.info('处理智能体协议')
                agreement_checkbox = agent_page.locator("span").filter(has_text="我已阅读并同意").first
                agreement_checkbox.click()
                agent_page.wait_for_timeout(500)
                logger.info('处理智能体协议完成')
            except Exception:
                logger.info("无需处理协议或已处理")
            logger.info("点击创建智能体按钮")
            create_agent_button = agent_page.get_by_text("创建智能体")
            create_agent_button.click()
            agent_page.wait_for_load_state("networkidle")
            logger.info("创建智能体基础设置成功")
        except Exception as e:
            logger.error(f"创建智能体失败: {e}")
            raise
    
    def complete_basic_setup(self, user_name: str) -> Page:
        try:
            center_page = self.login()
            logger.info("账户中心登录成功")
        except Exception as e:
            logger.error(f"账户中心登录失败: {e}",stack_info=True)
            raise
        
        try:
            user_page = self.user_page(user_name,center_page)
            logger.info(f"账号{user_name}登录成功")
        except  Exception as e:
            logger.error(f"账号{user_name}登录失败: {e}",stack_info=True)
            raise
        
        try:
            qiaocang_page = self.navigate_to_qiaocang(user_page)
            logger.info(f"账号{user_name}导航到智能体创建页面成功")
        except Exception as e:
            logger.error(f"账号{user_name}导航到智能体创建页面失败: {e}")
            raise
        
        try:
            self.set_agent_name(qiaocang_page,Config.AGENT_CREATION["agent_name"])
            self.set_avatar(qiaocang_page,Config.AGENT_CREATION['img_path'])
            qiaocang_page.wait_for_timeout(2000)#等待页面返回
            self.proceed_to_next_step(qiaocang_page)
            self.set_company_description(qiaocang_page,Config.AGENT_CREATION["company_description"])
            self.set_target_users(qiaocang_page,Config.AGENT_CREATION["target_users"])
            self.proceed_to_next_step(qiaocang_page)
            self.check_to_agreement(qiaocang_page)
        except Exception as e:
            logger.error(f"账号{user_name}智能体基础设置创建失败: {e}")
            raise
        return qiaocang_page
    
    def run(self,user_name: str) -> Page:
        try:
            qiaocang_page = self.complete_basic_setup(user_name)
            ServiceAdvantages(qiaocang_page).run()
            CoreBussinessTag(qiaocang_page).run()
            qiaocang_page.wait_for_timeout(10000)
            
            logger.info("创建智能体成功")
        except Exception as e:
            logger.error(f"创建智能体失败: {e}")
            raise
        return qiaocang_page
            
        
        
class CoreBussinessTag(object):
    def __init__(self, page:Page) -> None:
        self.page = page
        self.add_tag_button = page.locator("#roleSetting-baseInfoserviceTag").get_by_text("添加")
        self.tag_box = page.locator("#roleSetting-baseInfoserviceTag").get_by_role("textbox")

    def del_auto_tags(self) -> None:
        try:
            logger.info("删除自动添加的标签")
            # 定位所有待删除的 span 标签
            spans = self.page.locator('span.one-ai-tag-text').all()
            for span in spans:
                # 点击删除按钮并等待元素消失
                span.get_by_role("button").click()
                self.page.wait_for_timeout(500)
            # 验证删除结果
            remaining_spans = self.page.locator('span.one-ai-tag-text').count()
            logger.info(f"剩余未删除的 span 标签数量: {remaining_spans}")
            logger.info("删除自动添加的标签完成")
        except Exception as e:
            logger.error(f"删除自动添加的标签失败: {e}")
            raise
    def add_core_bussiness_tag(self) -> None:
        try:
            logger.info("添加核心业务标签")
            for tag in Config.SERVICE_TAGS:
                self.add_tag_button.click()
                self.tag_box.fill(tag)
                self.tag_box.press("Enter")
                self.page.wait_for_timeout(500)
            logger.info("添加核心业务标签完成")
            remaining_spans = self.page.locator('span.one-ai-tag-text').count()
            logger.info(f"添加的 span 标签数量: {remaining_spans}")
            self.page.wait_for_timeout(1000) # 等待页面更新
        except Exception as e:
            logger.error(f"添加核心业务标签失败: {e}")
            raise
    
    def run(self) -> None:
        try:
            self.del_auto_tags()
            self.add_core_bussiness_tag()
        except Exception as e:
            logger.error(f"自动添加核心业务标签失败: {e}")
            raise
            
class ServiceAdvantages(object):
    def __init__(self, page:Page) -> None:
        self.page = page
        # 弹出填写框
        self.pop_box_botton = page.get_by_alt_text("暂未填写")
        # 等级规模
        self.scale_and_grade_box = page.get_by_role("textbox", name="xx公司是xx地区最大的xx设备生产商，累积服务国内外xx")
        # 荣誉认证
        self.honors_and_certifications_box = page.get_by_role("textbox", name="荣获“xx奖”、“xx企业”，全线产品均已通过国际CE")
        # 业务经验
        self.business_experience_box = page.get_by_role("textbox", name="公司xx年来专注于xx、xx等领域。")
        # 专家团队
        self.expert_team_box = page.get_by_role("textbox", name="拥有N+研发人员，X")
        # 技术设备
        self.technology_and_equipment_box = page.get_by_role("textbox", name="有集xx、xx")
        # 保障承诺
        self.service_guarantees_box = page.get_by_role("textbox", name="我公司免费xx，终身售后，提供全年7*24")
        # 优惠政策
        self.preferential_policies_box = page.get_by_role("textbox", name="采买超过x台设备的客户可享受大客户N折优惠。")
        # 确认按钮
        self.confirm_botton = page.get_by_role("button", name="​ 确认")
    def fill_service_advantages(self) -> None:
        try:
            logger.info("填充服务优势")
            
            logger.info("点击弹出优势弹窗")
            self.pop_box_botton.click()
            
            logger.info("填写等级规模")
            self.scale_and_grade_box.click()
            self.scale_and_grade_box.fill(Config.BUSINESS_ADVANTAGES["network"])
            
            logger.info("填写荣誉认证")
            self.honors_and_certifications_box.click()
            self.honors_and_certifications_box.fill(Config.BUSINESS_ADVANTAGES["textbook"])
            
            logger.info("填写业务经验")
            self.business_experience_box.click()
            self.business_experience_box.fill(Config.BUSINESS_ADVANTAGES["talent_training"])
            
            logger.info("填写专家团队")
            self.expert_team_box.click()
            self.expert_team_box.fill(Config.BUSINESS_ADVANTAGES["rd_team"])
            
            logger.info("填写技术设备")
            self.technology_and_equipment_box.click()
            self.technology_and_equipment_box.fill(Config.BUSINESS_ADVANTAGES["facilities"])
            
            logger.info("填写保证承诺")
            self.service_guarantees_box.click()
            self.service_guarantees_box.fill(Config.BUSINESS_ADVANTAGES["service"])
            
            logger.info("填写优惠政策")
            self.preferential_policies_box.click()
            self.preferential_policies_box.fill(Config.BUSINESS_ADVANTAGES["policy"])
            
            logger.info("点击确认按钮")
            self.confirm_botton.click()
            self.page.wait_for_load_state("networkidle",timeout=10000)
            logger.info("填充服务优势完成")
        except Exception as e:
            logger.error(f"填充服务优势失败: {e}")
            raise
        
    def run(self):
        try:
            self.fill_service_advantages()
        except Exception as e:
            logger.error(f"自动填充服务优势失败: {e}")
            raise
        
