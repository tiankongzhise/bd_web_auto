from src.base import BdWebAutoBase
from playwright import Page

def get_account_center_page()->Page:
    BdWebAutoBase().login()
