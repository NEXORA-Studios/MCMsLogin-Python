# -*- coding: utf-8 -*-
"""
Minecraft Microsoft 账户登录模块测试

用于测试 MinecraftMicrosoftLogin 类的功能
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# 添加父目录到 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mc_ms_login import MinecraftMicrosoftLogin


class TestMinecraftMicrosoftLogin(unittest.TestCase):
    """测试 MinecraftMicrosoftLogin 类"""
    
    def setUp(self):
        """测试前的设置"""
        self.client_id = "test_client_id"
        self.test_cache_path = "test_token_cache.json"
        
        # 创建测试实例
        self.mc_login = MinecraftMicrosoftLogin(
            client_id=self.client_id,
            cache_path=self.test_cache_path
        )
    
    def tearDown(self):
        """测试后的清理"""
        # 删除测试缓存文件（如果存在）
        if os.path.exists(self.test_cache_path):
            os.remove(self.test_cache_path)
    
    @patch('msal.PublicClientApplication.get_accounts')
    @patch('msal.PublicClientApplication.acquire_token_silent')
    def test_get_microsoft_token_from_cache(self, mock_acquire_token, mock_get_accounts):
        """测试从缓存获取微软令牌"""
        # 模拟账户和令牌
        mock_get_accounts.return_value = [{'username': 'test@example.com'}]
        mock_acquire_token.return_value = {"access_token": "test_token"}
        
        # 调用方法
        result = self.mc_login.get_microsoft_token()
        
        # 验证结果
        self.assertTrue(result["success"])
        self.assertEqual(result["token"]["access_token"], "test_token")
        
        # 验证方法调用
        mock_get_accounts.assert_called_once()
        mock_acquire_token.assert_called_once()
    
    @patch('requests.post')
    def test_get_xbox_token(self, mock_post):
        """测试获取 Xbox Live 令牌"""
        # 模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Token": "test_xbox_token",
            "DisplayClaims": {"xui": [{"uhs": "test_user_hash"}]}
        }
        mock_post.return_value = mock_response
        
        # 调用方法
        result = self.mc_login.get_xbox_token("test_ms_token")
        
        # 验证结果
        self.assertTrue(result["success"])
        self.assertEqual(result["token"], "test_xbox_token")
        self.assertEqual(result["user_hash"], "test_user_hash")
        
        # 验证请求
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_get_xsts_token(self, mock_post):
        """测试获取 XSTS 令牌"""
        # 模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Token": "test_xsts_token",
            "DisplayClaims": {"xui": [{"uhs": "test_user_hash"}]}
        }
        mock_post.return_value = mock_response
        
        # 调用方法
        result = self.mc_login.get_xsts_token("test_xbox_token")
        
        # 验证结果
        self.assertTrue(result["success"])
        self.assertEqual(result["token"], "test_xsts_token")
        
        # 验证请求
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_get_minecraft_token(self, mock_post):
        """测试获取 Minecraft 令牌"""
        # 模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "test_mc_token",
            "expires_in": 86400
        }
        mock_post.return_value = mock_response
        
        # 调用方法
        result = self.mc_login.get_minecraft_token("test_user_hash", "test_xsts_token")
        
        # 验证结果
        self.assertTrue(result["success"])
        self.assertEqual(result["token"], "test_mc_token")
        self.assertEqual(result["expires_in"], 86400)
        
        # 验证请求
        mock_post.assert_called_once()
    
    @patch('requests.get')
    def test_get_minecraft_profile(self, mock_get):
        """测试获取 Minecraft 个人资料"""
        # 模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "test_uuid",
            "name": "TestPlayer"
        }
        mock_get.return_value = mock_response
        
        # 调用方法
        result = self.mc_login.get_minecraft_profile("test_mc_token")
        
        # 验证结果
        self.assertTrue(result["success"])
        self.assertEqual(result["profile"]["id"], "test_uuid")
        self.assertEqual(result["profile"]["name"], "TestPlayer")
        
        # 验证请求
        mock_get.assert_called_once()


if __name__ == "__main__":
    unittest.main()