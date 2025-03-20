from src.base import AutoAdsSession
from src.logger_config import logger
from playwright.sync_api import  Page
from ..config import Config
import re


class QiaoCang(object):
    def __init__(self) -> None:
        self.user_name = None

    def navigate_to_qiaocang(self,user_page: Page)->Page:
        qiaocang_url = Config.AGENT_CREATION["url"].format(user_id = Config.ACCOUNT_MAPPING[self.user_name])
        logger.debug(f"巧舱页面url为{qiaocang_url}")
        try:
            user_page.wait_for_load_state("load",timeout=10000)
        except Exception as e:
            logger.error("导航到巧舱页面超时,尝试直接跳转巧仓页面")
        user_page.goto(qiaocang_url)
        user_page.wait_for_load_state("load",timeout=10000)
        return user_page
    
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
    
    def complete_basic_setup(self, user_page:Page) -> Page:        
        try:
            qiaocang_page = self.navigate_to_qiaocang(user_page)
            logger.info(f"账号{self.user_name}导航到智能体创建页面成功")
        except Exception as e:
            logger.error(f"账号{self.user_name}导航到智能体创建页面失败: {e}")
            raise
        
        try:
            qiaocang_page.wait_for_timeout(5000) # 等待页面跳转完成
            if 'creatorChat' in qiaocang_page.url:
                self.set_agent_name(qiaocang_page,Config.AGENT_CREATION["agent_name"])
                self.set_avatar(qiaocang_page,Config.AGENT_CREATION['img_path'])
                qiaocang_page.wait_for_timeout(2000)#等待页面返回
                self.proceed_to_next_step(qiaocang_page)
                self.set_company_description(qiaocang_page,Config.AGENT_CREATION["company_description"])
                self.set_target_users(qiaocang_page,Config.AGENT_CREATION["target_users"])
                self.proceed_to_next_step(qiaocang_page)
                self.check_to_agreement(qiaocang_page)
            else:
                logger.info("智能体基础设置之前已创建完成")
        except Exception as e:
            logger.error(f"账号{self.user_name}智能体基础设置创建失败: {e}")
            raise
        return qiaocang_page
    
    def run(self,user_info: str|list) -> Page:
        try:
            if isinstance(user_info,str):
                user_info = [user_info]
            with AutoAdsSession() as ads_session:
                for user_name in user_info:
                    user_page = ads_session.get_account_page(user_name)
                    self.user_name = user_name
                    qiaocang_page = self.complete_basic_setup(user_page)
                    ServiceAdvantages(qiaocang_page).run()
                    ServiceAdvantagesTag(qiaocang_page).run()
                    WelcomeWord(qiaocang_page).run()
                    BaseExtInfo(qiaocang_page).run()
                    qiaocang_page.wait_for_timeout(10000)
                    logger.info(f"账户{user_name}创建智能体成功")
        except Exception as e:
            logger.error(f"创建智能体失败: {e}")
            raise

            
        
        
class ServiceAdvantagesTag(object):
    def __init__(self, page:Page) -> None:
        self.page = page
        self.add_tag_selector = "div.service-advantage-tags-add"
        self.tag_box_selectoer = "#roleSetting-baseInfoserviceTag div.service-advantage-tags-add input"
        # self.tags_selector = "#roleSetting-baseInfoserviceTag button.one-ai-button"
        self.tags_selector = "#roleSetting-baseInfoserviceTag button[class*='one-ai-tag-close-icon']"

    def del_auto_tags(self) -> None:
        try:
            logger.info("删除自动添加的标签")
            # 定位所有待删除的 span 标签
            # 或者使用更精确的类名组合（若类名稳定）
            MAX_WHILE_LOOPS = 20
            while_loops = 0
            while True:
                # current_buttons = self.page.query_selector_all(self.tags_selector)
                current_buttons = self.page.locator(self.tags_selector).all()
                current_buttons_count = self.page.locator(self.tags_selector).count()
                logger.debug(f"当前标签数量: {current_buttons_count}")
                if not current_buttons:
                    break  # 无按钮时退出循环
                current_buttons[0].click()  # 始终点击第一个按钮
                self.page.wait_for_timeout(500)
                while_loops += 1
                if while_loops > MAX_WHILE_LOOPS:
                    logger.error("循环次数过多，可能存在死循环。请检查代码。")
                    break

            logger.info(f"删除自动添加的{while_loops}个标签")
            # spans = self.page.locator(self.button_selector).all()
            # for span in spans:
            #     # 点击删除按钮并等待元素消失
            #     span.get_by_role("button").click()
            #     self.page.wait_for_timeout(500)
            # # 验证删除结果
            # remaining_spans = self.page.locator(self.button_selector).count()
            # logger.info(f"剩余未删除的 span 标签数量: {remaining_spans}")
            logger.info("删除自动添加的标签完成")
        except Exception as e:
            logger.error(f"删除自动添加的标签失败: {e}")
            raise
    def add_tag(self) -> None:
        try:
            logger.info("添加服务优势标签")
            for tag in Config.SERVICE_TAGS:
                self.page.locator(self.add_tag_selector).click()
                self.page.wait_for_selector(self.tag_box_selectoer,timeout=5000)
                self.page.locator(self.tag_box_selectoer).fill(tag)
                self.page.locator(self.tag_box_selectoer).press("Enter")
                self.page.wait_for_timeout(500)
            logger.info("添加服务优势签完成")
            remaining_spans = self.page.locator(self.tags_selector).count()
            logger.info(f"添加的 span 标签数量: {remaining_spans}")
            self.page.wait_for_timeout(1000) # 等待页面更新
        except Exception as e:
            logger.error(f"添加服务优势标签失败: {e}")
            raise
    
    def run(self) -> None:
        try:
            self.del_auto_tags()
            self.add_tag()
        except Exception as e:
            logger.error(f"自动添加服务优势标签失败: {e}")
            raise
            
class ServiceAdvantages(object):
    def __init__(self, page:Page) -> None:
        self.page = page
        # 弹出填写框
        # self.pop_box_botton = page.get_by_alt_text("暂未填写")
        self.pop_box_botton = page.get_by_text("暂未填写")
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

        #确认是否存在
        self.button_selector = "#roleSetting-baseInfoserviceTag button.one-ai-button"
    def fill_service_advantages(self) -> None:
        try:
            logger.info("填充服务优势")
            
            if self.page.locator(self.button_selector).count() > 0:
                logger.info("已存在服务优势，跳过填充")
                return

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
        
class WelcomeWord(object):
    def __init__(self, page:Page) -> None:
        self.page = page
        # 欢迎语
        self.welcome_word_text_container_selecotr = '#roleSetting-baseInfowelcomeWord > div.rich-text-container.base-info-welcome-word > div.rich-text-content > div > div > div.fr-wrapper > div'
    def fill_welcome_word(self) -> None:
        logger.info("填充欢迎语")
        try:
            self.page.locator(self.welcome_word_text_container_selecotr).click()
            self.page.locator(self.welcome_word_text_container_selecotr).fill(Config.WELCOME_WORD)
            logger.info("填充欢迎语完成")
        except Exception as e:
            logger.error(f"填充欢迎语失败: {e}")
            raise
    
    def run(self) -> None:
        try:
            self.fill_welcome_word()
        except Exception as e:
            logger.error(f"自动填充欢迎语失败: {e}")
            raise

class BaseExtInfo(object):
    def __init__(self, page:Page) -> None:
        self.page = page
        # 添加角色扩展信息按钮信息
        self.filled_celector = "#roleSetting-baseExtInfo:has-text('门店地址')"
        self.add_base_ext_info_selector = "#roleSetting-baseExtInfo div.common-title-display div.common-title-display-right"
        self.fill_short_name_selector = "#roleSetting-baseExtInfoagentShortName   input"
        self.select_theme_selector = '#baseExtInfo div.one-ai-checkbox-group.one-ai-theme-light-d22.light-ai.one-ai-checkbox-group-medium.one-ai-checkbox-group-row:has-text("线下业务")'
        # self.select_theme_ischeck_selector = '.one-ai-checkbox-button-input'
        self.upload_address_template_button_selector = "#baseExtInfo div.base-ext-address div.common-title-display button"
        self.upload_address_file_select_selector = 'button.one-ai-button:has(span:text("点击选择文件"))'
        self.upload_address_file_del_old_file_selector = 'body > div:nth-child(5) > div > div.one-ai-dialog > div.one-ai-dialog-content.agent-common-modal-content > div.one-ai-dialog-body > div > div > div.uploadwithpkg-cotainer > div > svg'
        self.upload_address_file_upload_selector = 'button.one-ai-button-primary:has-text("开始上传")'
        self.upload_address_file_confirm_selector = 'button.one-ai-button-primary:has-text("确认")'
        self.upload_address_success_selector = 'div.address-upload-two-success:has-text("上传成功")'
        self.upload_address_back_selector = "#roleSetting > div.new-role-second-edit-page-back-container > div > div > div > div > div"
        self.upload_address_back_success_selector = "#roleSetting-baseExtInfo > div > div.common-tags-display > div.one-ai-tag.common-tags-display-tags.light-ai.light-ai.one-ai-tag-medium.one-ai-tag-no-bordered.one-ai-tag-fill-solid"

        
        
    def goto_base_ext_info(self) -> None:
        logger.info("点击添加角色扩展信息按钮")
        try:
            self.page.locator(self.add_base_ext_info_selector).click()
            logger.info("点击添加角色扩展信息按钮完成")
        except Exception as e:
            logger.error(f"点击添加角色扩展信息按钮失败: {e}")
            raise
    #roleSetting-baseExtInfoagentShortName > div > div > div > input
    def fill_short_name(self):
        logger.info("填写角色扩展信息-商家简称")
        try:
            self.page.locator(self.fill_short_name_selector).fill(Config.BASE_EXT_INFO["short_name"])
            logger.info("填写角色扩展信息-商家简称完成")
        except Exception as e:
            logger.error(f"填写角色扩展信息-商家简称失败: {e}")
            raise

    #baseExtInfo > div > div.one-ai-checkbox-group.one-ai-theme-light-d22.light-ai.one-ai-checkbox-group-medium.one-ai-checkbox-group-row > div > label:nth-child(2) > span.one-ai-checkbox-button-item
    #//*[@id="baseExtInfo"]/div/div[6]/div/label[2]/span[2]
    #//span[contains(@class, 'one-ai-checkbox-button-item') and text()='线下业务']
    def select_theme(self):
        logger.info("选择角色扩展信息-经营类型")
        if self.page.locator(self.select_theme_selector).count() == 0: #如果元素不存在，则跳过
            logger.info("线下业务元素不存在，跳过")
            raise "线下业务元素不存在"
        try:
            theme_box = self.page.get_by_role('checkbox',name= '线下业务')
            if theme_box.is_checked():
                logger.info("线下业务已选中，跳过")
            else:
                self.page.locator(self.select_theme_selector).click()
            logger.info("选择角色扩展信息-经营类型完成")
        except Exception as e:
            logger.error(f"选择角色扩展信息-经营类型失败: {e}")
            raise

    def upload_address_template(self):
        logger.info("上传地址模板")
        try:
            self.page.locator(self.upload_address_template_button_selector).click()
            if self.page.locator(self.upload_address_file_del_old_file_selector).count() > 0: #如果存在删除按钮，则先删除
                self.page.locator(self.upload_address_file_del_old_file_selector).click()
            if not upload_file(self.page,self.upload_address_file_select_selector,Config.BASE_EXT_INFO["address_path"]):
                raise '文件上传失败'
            self.page.wait_for_selector(self.upload_address_file_upload_selector,timeout=10000) #等待确认上传按钮出现
            logger.debug("出现确认上传按钮，且可以点击")
            self.page.locator(self.upload_address_file_upload_selector).click()
            logger.debug("点击确认上传按钮")
            self.page.wait_for_selector(self.upload_address_success_selector,timeout=10000)
            logger.debug('上传成功标识出现')
            self.page.locator(self.upload_address_file_confirm_selector).click()
            logger.debug("点击确认按钮成功")
            logger.info("上传地址模板完成")
        except Exception as e:
            logger.error(f"上传地址模板失败: {e}")
            raise
    def back_to_agent_setting(self):
        logger.info("返回到角色设置页面")
        try:
            self.page.locator(self.upload_address_back_selector).click()
            self.page.wait_for_selector(self.upload_address_back_success_selector,timeout=10000)
            logger.info("返回到角色设置页面完成")
        except Exception as e:
            logger.error(f"返回到角色设置页面失败: {e}")
            raise
    def filled_check(self):
        if self.page.locator(self.filled_celector).count()>0:
            logger.info("角色扩展信息,之前已经被填写过")
            return True
        else:
            return False
    def run(self):
        try:
            logger.info("开始执行角色扩展信息上传")
            if self.filled_check():
                logger.info("跳过角色扩展信息填充")
                return None
            self.goto_base_ext_info()
            self.fill_short_name()
            self.select_theme()
            self.upload_address_template()
            self.back_to_agent_setting()
        except Exception as e:
            logger.error(f"执行角色扩展信息上传失败: {e}")
            raise

def upload_file(page:Page,upload_selector:str,file_path:str):
    try:
        logger.info("开始上传文件")
        with page.expect_file_chooser() as fc_info:
            # paconsult_pagege.click("button#upload-button")  # 触发文件选择器弹窗
            page.locator(upload_selector).click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_path)  # 设置文件路径
        logger.info("上传文件完成")
        return True
    except Exception as e:
        logger.error(f"上传文件失败: {e}")
        return False

class LeadsCollection(object):
    def __init__(self,page:Page):
        self.page = page
        self.leads_collection_selector = "div.one-ai-collapse-item-title:has-text('线索收集')"
        self.phone_box_selector = 'div.clue-type-obtain:has-text("电话方案")'
        self.phone_auto_send_selector = "div.one-ai-checkbox-item:has-text('主动发送')"
        self.phone_select_selection_selector = 'div.one-ai-select-selection__rendered:has-text("请选择电话方案")'
        self.phone_select_menu_selector = 'li.one-ai-select-dropdown-menu-item:has-text("转")'
        self.phone_push_selector = 'span.one-ai-checkbox-item:has-text("优先发送客服电话")'
        self.wechat_box_selector = 'div.clue-type-obtain:has-text("微信方案")'
        self.wechat_anser_selector = 'span.one-ai-checkbox-item:has-text("被动回答")'
    def explan_leads_collection_setting(self)->None:
        try:
            logger.info("设置线索收集")
            self.page.locator(self.leads_collection_selector).click()
            logger.info("展开线索收集设置")
        except Exception as e:
            logger.error(f"设置线索收集失败: {e}")
            return
        
        
    
    def check_phone_auto_send_checkbox(self)->None:
        try:
            logger.info("勾选电话线索获取方式，电话主动发送")
            self.page.locator(self.phone_box_selector).locator(self.phone_auto_send_selector).click()
            logger.info("设置电话主动发送成功")
        except Exception as e:
            logger.error(f"设置手机号自动发送失败: {e}")
            raise
    def select_phone_selection(self)->None:
        try:
            logger.info("开始设置电话方案")
            self.page.locator(self.phone_select_selection_selector).click()
            logger.info("选择虚拟号转接方案")
            self.page.locator(self.phone_select_menu_selector).click()
            logger.info("电话方案设置完成")
        except Exception as e:
            logger.error(f'设置电话方案失败:{e}')
            raise
        
    def check_push_phone(self):
        try:
            logger.info("勾选发送客服电话")
            self.page.locator(self.phone_push_selector).click()
            logger.info('设置发送客户电话完成')
        except Exception as e:
            logger.error(f'设置发送客服电话失败，{e}')
    
    def check_wechat_anser(self):
        try:
            logger.info("勾选微信线索获取方式，被动应答")
            self.page.locator(self.wechat_box_selector).locator(self.wechat_anser_selector).click()
            logger.info("设置微信被动应答成功")
        except Exception as e:
            logger.error(f"设置微信被动应答失败: {e}")
            raise
        
    
    def run(self):
        try:
            logger.info('设置线索收集方式')
            self.explan_leads_collection_setting()
            self.check_phone_auto_send_checkbox()
            self.select_phone_selection()
            self.check_push_phone()
            self.check_wechat_anser()
        except Exception as e:
            logger.error(f'自动设置线索手机方式失败:{e}')
        
        
        
        
