from playwright.sync_api import Page


def login(page:Page) -> Page:
    page.goto("https://cas.baidu.com/?tpl=www2&fromu=https%3A%2F%2Fwww2.baidu.com%2Fcommon%2Fappinit.ajax")
    page.get_by_role("textbox", name="请输入账号").click()
    page.get_by_role("textbox", name="请输入账号").fill("BDCC-金蛛账号中心")
    page.get_by_role("textbox", name="请输入密码").click()
    page.get_by_role("textbox", name="请输入密码").fill("JinZhu2025#")
    page.get_by_role("button", name="登录").click()
    return page



