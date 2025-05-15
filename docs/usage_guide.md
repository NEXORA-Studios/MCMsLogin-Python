# Minecraft Microsoft 账户登录模块使用指南

## 简介

本指南详细介绍了如何配置和使用 Minecraft Microsoft 账户登录模块。该模块使用 Microsoft Authentication Library (MSAL) for Python 实现了 Minecraft 微软账户的完整登录流程。

## 前提条件

1. Python 3.6 或更高版本
2. 已安装 MSAL 和 requests 库
3. Microsoft Azure 应用注册（用于获取客户端 ID）

## 安装

1. 克隆或下载本仓库
2. 安装依赖项：

```bash
pip install -r requirements.txt
```

## 注册 Azure 应用

要使用此模块，您需要在 Microsoft Azure 门户中注册一个应用程序：

1. 访问 [Azure 门户](https://portal.azure.com/)
2. 导航至「Azure Active Directory」→「应用注册」
3. 点击「新注册」
4. 填写应用名称（例如「Minecraft Launcher」）
5. 在「支持的账户类型」中选择「任何组织目录中的账户和个人 Microsoft 账户」
6. 重定向 URI 可以设置为「http://localhost」（移动和桌面应用）
7. 点击「注册」
8. 注册完成后，记录「应用程序（客户端）ID」，这将用于初始化登录模块

## 基本用法

以下是使用该模块的基本步骤：

```python
from mc_ms_login import MinecraftMicrosoftLogin

# 初始化登录模块，替换为您的客户端 ID
mc_login = MinecraftMicrosoftLogin(client_id="your_client_id_here")

# 执行登录流程
result = mc_login.login()

# 检查登录结果
if result["success"]:
    # 登录成功
    minecraft_token = result["minecraft_token"]
    profile = result["profile"]
    
    print(f"登录成功！玩家名称：{profile['name']}")
    print(f"UUID：{profile['id']}")
    
    # 使用令牌进行游戏启动或其他操作
else:
    # 登录失败
    print(f"登录失败：{result['error']}")
    if "details" in result:
        print(f"详细信息：{result['details']}")
```

## 高级用法

### 自定义令牌缓存路径

默认情况下，令牌缓存保存在 `~/.minecraft/msal_token_cache.json`。您可以自定义缓存路径：

```python
mc_login = MinecraftMicrosoftLogin(
    client_id="your_client_id_here",
    cache_path="/path/to/your/cache.json"
)
```

### 单独使用各个认证步骤

如果需要更精细的控制，可以单独使用各个认证步骤：

```python
# 获取微软令牌
ms_result = mc_login.get_microsoft_token()
if ms_result["success"]:
    ms_token = ms_result["token"]["access_token"]
    
    # 获取 Xbox Live 令牌
    xbox_result = mc_login.get_xbox_token(ms_token)
    if xbox_result["success"]:
        xbox_token = xbox_result["token"]
        user_hash = xbox_result["user_hash"]
        
        # 获取 XSTS 令牌
        xsts_result = mc_login.get_xsts_token(xbox_token)
        if xsts_result["success"]:
            xsts_token = xsts_result["token"]
            
            # 获取 Minecraft 令牌
            mc_result = mc_login.get_minecraft_token(user_hash, xsts_token)
            if mc_result["success"]:
                mc_token = mc_result["token"]
                
                # 获取 Minecraft 个人资料
                profile_result = mc_login.get_minecraft_profile(mc_token)
```

## 常见问题

### 1. 登录时出现「此账户未拥有 Minecraft」错误

这表示您的 Microsoft 账户未购买 Minecraft Java 版。请确保使用已购买 Minecraft 的账户登录。

### 2. 登录时出现「此账户未关联 Xbox 账户」错误

您需要先在 [Xbox 网站](https://www.xbox.com/) 上创建一个 Xbox 个人资料。

### 3. 登录时出现「此账户来自不支持 Xbox Live 的国家/地区」错误

某些国家/地区不支持 Xbox Live 服务。您可能需要更改账户的区域设置。

## 集成到启动器

将此模块集成到 Minecraft 启动器时，您需要：

1. 使用 `login()` 方法获取 Minecraft 令牌
2. 使用获取的令牌构建启动参数
3. 处理令牌过期情况（通常通过检查 `expires_in` 值）

## 安全注意事项

- 客户端 ID 不是敏感信息，可以包含在代码中
- 令牌缓存文件包含敏感信息，确保适当保护
- 不要在日志中记录访问令牌
- 考虑在生产环境中加密令牌缓存文件