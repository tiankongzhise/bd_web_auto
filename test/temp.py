from dotenv import load_dotenv
import os
load_dotenv()

if __name__ == '__main__':
    print(os.getenv("BDCC_PASSWORD"))
    print(os.getenv("BDCC_USERNAME"))
