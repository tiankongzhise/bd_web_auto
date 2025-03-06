from dotenv import load_dotenv
import os

try:
    # 添加verbose参数以获取更多信息
    load_dotenv(dotenv_path=r'j:\uv_code_lib\auto_web\.env', verbose=True)
    print("成功加载.env文件")
except Exception as e:
    print(f"加载.env文件时出错: {e}")

# 调试：打印所有环境变量
print("当前环境变量：")
print(os.environ)

def main():
    username = os.getenv('BD_USER_NAME')
    password = os.getenv('BD_USER_PASSWORD')
    print(f"用户名: {username}")
    print(f"密码: {password}")


if __name__ == "__main__":
    main()
