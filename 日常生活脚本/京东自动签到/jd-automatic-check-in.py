"""
京东多账号自动签到领京豆脚本（防重复签到版）
功能说明：
1. 本地记录+接口双重校验重复签到
2. 支持多设备登录状态检测
3. 优化错误码识别机制
"""

import os
import json
import requests
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


class JDCookieManager:
    """Cookie管理工具类"""

    def __init__(self):
        # self.cookie_file = "jd_cookies.json"
        self.cookie_file = "/home/jasonkun/script/JD-Automatic-sign-in/jd_cookies.json"
        self.sign_record = "/home/jasonkun/script/JD-Automatic-sign-in/jd_sign_records.json"  # 新增签到记录文件

    def get_cookie_manually(self):
        """手动获取Cookie指引"""
        # print("请按以下步骤获取Cookie：")
        # print("1. 使用Chrome浏览器访问 https://m.jd.com")
        # print("2. 使用手机验证码登录（有效期更长）")
        # print("3. 按F12打开开发者工具，选择Network标签")
        # print("4. 刷新页面，找到任意log.gif请求")
        # print("5. 复制Request Headers中的完整Cookie")
        cookie = input("请输入获取到的Cookie：").strip()
        remark = input("请输入账号备注：").strip()
        return {"remark": remark, "cookie": cookie}

    def save_cookie(self, cookie_data):
        """保存Cookie到文件"""
        cookies = self.load_cookies()
        if any(item["cookie"] == cookie_data["cookie"] for item in cookies):
            print("⚠️ 该Cookie已存在")
            return
        cookies.append(cookie_data)
        with open(self.cookie_file, 'w') as f:
            json.dump(cookies, f, indent=2)
        print("✅ Cookie保存成功")

    def load_cookies(self):
        """从文件加载Cookie"""
        if not os.path.exists(self.cookie_file):
            return []
        try:
            with open(self.cookie_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Cookie文件加载失败: {str(e)}")
            return []

    def _load_sign_records(self):
        """加载签到记录"""
        if not os.path.exists(self.sign_record):
            return {}
        try:
            with open(self.sign_record, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"签到记录加载失败: {str(e)}")
            return {}

    def _save_sign_record(self, remark):
        """更新签到记录"""
        records = self._load_sign_records()
        today = datetime.now().strftime("%Y-%m-%d")
        records[remark] = today
        with open(self.sign_record, 'w') as f:
            json.dump(records, f, indent=2)

    def check_today_signed(self, remark):
        """检查本地签到记录"""
        records = self._load_sign_records()
        today = datetime.now().strftime("%Y-%m-%d")
        return records.get(remark) == today


class JDSign:
    """京东签到处理器"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Referer": "https://home.m.jd.com/"
        }
        self.cookie_manager = JDCookieManager()  # 新增Cookie管理器引用
        self._init_logger()

    def _init_logger(self):
        """初始化日志系统"""
        self.logger = logging.getLogger('JDSign')
        self.logger.setLevel(logging.DEBUG)

        # 按天滚动日志，保留7天
        handler = TimedRotatingFileHandler(
            'jd_sign.log',
            when='midnight',
            backupCount=7,
            encoding='utf-8'
        )
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(account)s] %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # 控制台输出
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def parse_cookie(self, cookie_str):
        """Cookie字符串转字典"""
        return {k:v for item in cookie_str.split(';') if '=' in item
                for k,v in [item.strip().split('=', 1)]}

    def _check_response_status(self, result, cookie_data):
        """新增：综合判断签到状态"""
        log_info = {'account': cookie_data['remark']}
        today = datetime.now().strftime("%Y-%m-%d")

        # 情况1：本地已有今日记录
        if self.cookie_manager.check_today_signed(cookie_data['remark']):
            self.logger.warning(f"重复签到（本地记录）", extra=log_info)
            print(f"⏰ {cookie_data['remark']} 今日已签到（本地记录）")
            return False

        # 情况2：接口返回已签到
        error_msg = result.get("errorMessage", "").lower()
        if result.get("code") in ["138", "158"] or any(x in error_msg for x in ["已签到", "重复签到"]):
            self.logger.warning(f"重复签到（接口返回）", extra=log_info)
            print(f"⏰ {cookie_data['remark']} 今日已签到（接口提示）")
            self.cookie_manager._save_sign_record(cookie_data['remark'])  # 更新本地记录
            return False

        # 情况3：京豆数量为0
        if result.get("code") == "0":
            beans = int(result.get("data", {}).get("dailyAward", {}).get("beanAward", {}).get("beanCount", 0))
            if beans == 0:
                self.logger.warning(f"重复签到（京豆为0）", extra=log_info)
                print(f"⏰ {cookie_data['remark']} 今日已签到（京豆为0）")
                self.cookie_manager._save_sign_record(cookie_data['remark'])
                return False

        return True

    def sign(self, cookie_data):
        """执行签到操作（增强版）"""
        log_info = {'account': cookie_data['remark']}

        # 前置检查：本地记录校验
        if self.cookie_manager.check_today_signed(cookie_data['remark']):
            print(f"⏰ {cookie_data['remark']} 今日已签到（本地记录）")
            return False

        try:
            response = requests.get(
                "https://api.m.jd.com/client.action",
                params={
                    "functionId": "signBeanAct",
                    "body": json.dumps({
                        "fp": "-1",
                        "shshshfp": "-1",
                        "userAgent": self.headers["User-Agent"]
                    }),
                    "appid": "ld"
                },
                headers=self.headers,
                cookies=self.parse_cookie(cookie_data["cookie"]),
                timeout=15
            )
            result = response.json()
            self.logger.debug(f"API响应: {json.dumps(result)}", extra=log_info)

            # 综合状态判断
            if not self._check_response_status(result, cookie_data):
                return False

            # 处理签到成功
            if result.get("code") == "0":
                beans = int(result.get("data", {}).get("dailyAward", {}).get("beanAward", {}).get("beanCount", 0))
                self.logger.info(f"签到成功 +{beans}京豆", extra=log_info)
                print(f"✅ {cookie_data['remark']} 获得{beans}京豆")
                self.cookie_manager._save_sign_record(cookie_data['remark'])
                return True
            else:
                error_msg = result.get("errorMessage", "未知错误")
                self.logger.error(f"接口错误: {error_msg}", extra=log_info)
                print(f"❌ {cookie_data['remark']} 失败: {error_msg}")
                return False

        except requests.RequestException as e:
            self.logger.error(f"网络异常: {str(e)}", extra=log_info, exc_info=True)
            print(f"🌐 {cookie_data['remark']} 网络请求失败")
            return False
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"数据解析失败: {str(e)}", extra=log_info, exc_info=True)
            print(f"🔧 {cookie_data['remark']} 数据解析异常")
            return False


def main():
    cookie_manager = JDCookieManager()
    signer = JDSign()

    # while True:
    print("\n京东签到管理系统")
    print("1. 添加新Cookie")
    print("2. 执行签到任务")
    print("3. 查看今日日志")
    print("4. 退出系统")
    # choice = input("请选择操作：").strip()
    choice = "2".strip()
    if choice == "1":
        cookie_data = cookie_manager.get_cookie_manually()
        cookie_manager.save_cookie(cookie_data)
    elif choice == "2":
        cookies = cookie_manager.load_cookies()
        if not cookies:
            print("⚠️ 未找到有效Cookie")
            # continue
        print(f"\n开始执行 {len(cookies)} 个账号签到...")
        for cookie in cookies:
            signer.sign(cookie)
    elif choice == "3":
        try:
            with open('jd_sign.log', encoding='utf-8') as f:
                print("\n".join(f.readlines()[-20:]))
        except Exception as e:
            print(f"日志读取失败: {str(e)}")
    elif choice == "4":
        print("系统退出")
        # break
    else:
        print("⚠️ 无效的输入")

if __name__ == "__main__":
    main()
