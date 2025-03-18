from src.base import BdWebAutoBase
from playwright import Page

def get_account_page(user_name:str,user_center_page:Page)->Page:
    return BdWebAutoBase().user_page(user_name,user_center_page)
