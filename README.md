# Minecraft Microsoft 账户登录模块

这是一个使用 Microsoft Authentication Library (MSAL) for Python 实现的 Minecraft 微软账户登录模块。该模块允许 Minecraft 启动器通过微软账户进行身份验证，获取访问令牌，并使用这些令牌来获取 Minecraft 游戏令牌。

## 功能特性

- 使用 MSAL 库进行微软账户认证
- 支持令牌缓存，减少重复登录
- 处理令牌刷新
- 获取 Minecraft 游戏令牌
- 错误处理和日志记录

## 安装要求

- Python 3.6+
- MSAL 库

```bash
pip install msal
```

## 使用方法

```python
from mc_ms_login import MinecraftMicrosoftLogin

# 初始化登录模块
mc_login = MinecraftMicrosoftLogin(client_id="your_client_id")

# 进行登录并获取 Minecraft 令牌
result = mc_login.login()
if result["success"]:
    minecraft_token = result["minecraft_token"]
    # 使用令牌进行游戏启动或其他操作
else:
    print(f"登录失败: {result['error']}")
```

## 许可证

本项目采用 Mozilla Public License Version 2.0 许可证。详情请参阅 [LICENSE](LICENSE) 文件。