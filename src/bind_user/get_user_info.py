from src.logger_config import logger
from pathlib import Path
from typing import List, Dict



def load_user_info(file_path: str = None) -> List[Dict[str, str]]:
    """
    读取用户信息文件，返回结构化数据
    
    参数：
        file_path: 可自定义文件路径，默认读取 src/bind_user/user_info.txt
        
    返回：
        [{'username': 'user1', 'password': 'pwd1'}, ...]
    """
    users = []
    # default_path = Path(__file__).parent.parent / "src" / "bind_user" / "user_info.txt"
    default_path = Path(__file__).parent/ "user_info.txt"
    
    try:
        target_path = Path(file_path) if file_path else default_path
        
        with open(target_path, 'r', encoding='utf-8') as f:
            logger.info(f"开始读取用户文件：{target_path}")
            
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):  # 跳过空行和注释
                    continue
                    
                parts = [p.strip() for p in line.split(',')]
                if len(parts) != 2:
                    logger.warning(f"第{line_num}行格式错误：{line}")
                    continue
                    
                users.append({
                    'username': parts[0],
                    'password': parts[1]
                })
                
        logger.info(f"成功加载 {len(users)} 条用户记录")
        return users
        
    except FileNotFoundError:
        logger.error(f"用户文件不存在：{target_path}")
        return []
    except Exception as e:
        logger.error(f"读取用户文件失败：{str(e)}")
        return []

# 使用示例
if __name__ == '__main__':
    user_list = load_user_info()
    print(user_list)
