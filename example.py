# -*- coding: utf-8 -*-
"""
Minecraft Microsoft 账户登录示例

展示如何使用 MinecraftMicrosoftLogin 类进行 Minecraft 微软账户登录
"""

import sys
from mc_ms_login import MinecraftMicrosoftLogin

# 替换为你的应用程序客户端 ID
# 你需要在 Azure 门户中注册一个应用程序来获取客户端 ID
# https://portal.azure.com/ -> Azure Active Directory -> 应用注册
CLIENT_ID = ""

def main():
    """主函数，演示登录流程"""
    print("Minecraft Microsoft 账户登录示例")
    print("-" * 40)
    
    # 初始化登录模块
    mc_login = MinecraftMicrosoftLogin(client_id=CLIENT_ID)
    
    # 执行登录流程
    print("开始登录流程...")
    print("请按照提示在浏览器中完成 Microsoft 账户登录")
    print("-" * 40)
    
    result = mc_login.login()
    
    if result["success"]:
        # 登录成功，显示用户信息
        profile = result["profile"]
        print(f"登录成功！欢迎，{profile['name']}")
        print(f"UUID: {profile['id']}")
        print(f"令牌有效期: {result['expires_in']} 秒")
        
        # 在实际应用中，你可以使用 result["minecraft_token"] 进行游戏启动等操作
        print("\n你现在可以使用此令牌启动游戏或执行其他操作")
    else:
        # 登录失败，显示错误信息
        print(f"登录失败: {result['error']}")
        if "details" in result:
            print(f"详细信息: {result['details']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())