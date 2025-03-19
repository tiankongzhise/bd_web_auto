from tkzs_bd_db_tool import init_db,get_session
from tkzs_bd_db_tool import models
from src.logger_config import logger
import os
from dotenv import load_dotenv
load_dotenv()



init_db()

def get_account_list():
    with get_session() as session:
        rsp = session.query(models.BdAdCenterBindTable).all()
        account_list = [account.user_name for account in rsp]
    return account_list

def get_account_mapping():
    with get_session() as session:
        rsp = session.query(models.BdAdCenterBindTable).all()
        account_map = models.BdAdCenterBindTable.to_account_mapping(rsp)
        logger.debug(account_map)
    return account_map


# 配置文件

class Config:
    # 浏览器配置
    BROWSER_CONFIG = {
        "headless": False,
        "slow_mo": 50,  # 减慢操作速度，增加稳定性
        "timeout": 30000  # 默认超时时间（毫秒）
    }
    
    # 登录信息
    LOGIN = {
        "url": "https://cas.baidu.com/?tpl=www2&fromu=https%3A%2F%2Fwww2.baidu.com%2Fcommon%2Fappinit.ajax",
        "username": os.getenv('BDCC_USERNAME'),
        "password": os.getenv('BDCC_PASSWORD') # 注意：实际应用中应使用环境变量或安全存储
    }
    ACCOUNT_LIST = get_account_list()
    ACCOUNT_MAPPING = get_account_mapping()
    
    # 智能体创建页面
    AGENT_CREATION = {
        "url": "https://aiagent.baidu.com/mbot/user/{user_id}/creatorChat?relationSource=mbotIndex&ucUserId={user_id}",
        "agent_name": "深圳北大青鸟教师助理",
        "img_path":r'E:\OneDrive\2025年项目\教育类\嘉华\素材\在用素材\北大青鸟鸟标.png',
        "company_description": '专注IT培训教育26年，培养100W学员从事IT互联网行业。学AI，好工作，就找北大青鸟。 北大青鸟始终践行"职业教育就是就业教育"的教育本质， 坚持帮助学员成功就业，永远是硬道理，始终保持回归职业教育的本真，即坚守"教学为本，师爱为魂"的教育理念， 以及"内育职业素养，外塑专业技能"的青鸟校训，主要业务有软件开发培训，网络工程培训，AI开发培训，Java培训，大数据培训，Python培训，电商培训，新媒体培训，UI培训等。',
        "target_users": "目标用户是希望通过学一门技术获得好发展的人群。"
    }

    
    # 商家优势信息
    BUSINESS_ADVANTAGES = {
        "network": "全国60多个城市200余家分校，800+所合作学校，20000+家合作用人企业。",
        "textbook": '教材被纳入国家"十三五"和"十四五"规划高校教学用书',
        "talent_training": "26年培养了100万+IT互联网技术人才，与华/阿等企业深度合作，参与大数据等岗位行业标准制定。",
        "rd_team": "拥有200余人的研发团队，覆盖教育学、软件开发、网络安全等多个领域，课程每10-18个月更新一次，确保技术前沿性。",
        "facilities": "配备青鸟AI实验室、NovaAI开放平台等先进教学设施，提供真实企业项目实训环境。",
        "service": "入学签订协议，提供全程就业跟踪服务，​技能学历双认证。",
        "policy": "完善奖助学金政策，提供先学后付，特殊群体专项补贴或学费减免。"
    }
    
    # 服务标签
    SERVICE_TAGS = [
        "权威教材",
        "26年教学沉淀",
        "100W+学员选择",
        "行业定制标准",
        "全真项目实战",
        "AI+全新升级"
    ]

    WELCOME_WORD = '北大青鸟针对不同年龄段人群开设不同的专业课程，小班授课，实战教学，学历+技能双修，毕业推荐就业，点击咨询学校详细'
    
    BASE_EXT_INFO = {
        'short_name':'深圳北大青鸟',
        'address_path':r'C:\Users\tiank\OneDrive\2025年项目\教育类\嘉华\素材\在用素材\addressTemplate.xlsx'
    }
    # 线索收集配置
    LEAD_COLLECTION = {
        "phone_plan": "转18806662618",
        "wechat_plan": "挂机短信默认方案_2618"
    }
    
    # 文件路径
    FILES = {
        "address_template": "addressTemplate.xlsx"
    }
