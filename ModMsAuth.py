from traceback import print_exc
from requests import post, get

from ModLogging import ModLogging, LoggingType as LT
from ModException import *

global_header = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

class Auth:
    @staticmethod
    def Auth_XBL(url:str):
        r'''
        进行 XBL 验证
        
        参数
        ---------
        url (str): 包含 Code 的 Uri 字符串, 以 https://login.live.com/oauth20_desktop.srf?code= 开头
        
        返回 (验证成功时)
        ------------------------
        xbl_token (str): XBL 令牌
        uhs (str)
        '''
        
        code = url.split('=')[1]
        session = post('https://user.auth.xboxlive.com/user/authenticate', headers = global_header, json = {
            'Properties': {
                'AuthMethod': 'RPS',
                'SiteName': 'user.auth.xboxlive.com',
                'RpsTicket': code
            },
            'RelyingParty': 'http://auth.xboxlive.com',
            'TokenType': 'JWT'
        })
        
        if session.ok:
            resp = session.json()
            xbl_token, uhs = resp['Token'], resp['DisplayClaims']['xui'][0]['uhs']
            return xbl_token, uhs
        else:
            raise XBLAuthingException()

    @staticmethod
    def Auth_XSTS(xbl_token:str):
        r'''
        进行 XSTS 验证
        
        参数
        ---------
        xbl_token (str): 拿到的 XBL 令牌
        
        返回 (验证成功时)
        ------------------------
        xsts_token (str): XSTS 令牌
        uhs (str)
        '''
        session = post('https://xsts.auth.xboxlive.com/xsts/authorize', headers = global_header, json = {
            'Properties': {
                'SandboxId': 'RETAIL',
                'UserTokens': [
                    xbl_token
                ]
            },
            'RelyingParty': 'rp://api.minecraftservices.com/',
            'TokenType': 'JWT'
        })
        
        if session.ok:
            resp = session.json()
            xsts_token, uhs = resp['Token'], resp['DisplayClaims']['xui'][0]['uhs']
            return xsts_token, uhs
        else:
            raise XSTSAuthingException()

    @staticmethod
    def GetMinecraftToken(uhs:str, xsts_token:str):
        r'''
        拿到 Minecraft 访问令牌
        
        参数
        ---------
        uhs (str)
        xsts_token (str): 拿到的 XSTS 令牌
        
        返回 (验证成功时)
        ------------------------
        access_token (str): 账户访问令牌
        '''
        
        session = post('https://api.minecraftservices.com/authentication/login_with_xbox', headers = global_header, json = {
            'identityToken': f'XBL3.0 x={uhs};{xsts_token}'
        })
        
        if session.ok:
            resp = session.json()
            access_token = resp['access_token']
            return access_token
        else:
            raise MinecraftAuthingException()

    @staticmethod
    def CheckLicense(token:str):
        r'''
        确认是否拥有 Minecraft 游戏
        
        参数
        ---------
        token (str): 拿到的 Minecraft 账户访问令牌
        
        返回 (验证成功时)
        ------------------------
        haveJE (bool): 是否持有 Minecraft JE
        haveBE (bool): 是否持有 Minecraft BE 
        '''
        
        session = post('https://api.minecraftservices.com/entitlements/mcstore', headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        })
        
        if session.ok:
            try:
                haveJE, haveBE = False, False
                resp = session.json()
                items = resp['items']
                for item in items:
                    if item['name'] == 'game_minecraft':
                        haveJE = True
                    elif item['name'] == 'game_minecraft_bedrock':
                        haveBE = True
            except: pass
            finally: return haveJE, haveBE
        else: raise MinecraftCheckLicenseException()
    
    @staticmethod
    def GetProfile(token:str):
        r'''
        确认是否拥有 Minecraft 游戏
        
        参数
        ---------
        token (str): 拿到的 Minecraft 账户访问令牌
        
        返回 (验证成功时)
        ------------------------
        mcid (str): 账号的 MC UUID
        mcname (str): 账号的 MC 用户名 
        '''

        session = get('https://api.minecraftservices.com/minecraft/profile', headers = {
            'Authorization': f'Bearer {token}'
        })
        
        if session.ok:
            resp:dict = session.json()
            if 'path' in resp.keys(): return None, None
            mcid, mcname = resp['id'], resp['name']
            return mcid, mcname
        else: raise MinecraftGetProfileException()

def LoginMS(code_uri:str):
    r'''
    登录方法
    
    参数
    ---------
    code_uri (str): 包含 Code 的 Uri 字符串, 以 https://login.live.com/oauth20_desktop.srf?code= 开头
    
    返回 (登录成功时)
    ------------------------
    haveJE (bool): 是否持有 Minecraft JE
    haveBE (bool): 是否持有 Minecraft BE 
    mcid (str): 账号的 MC UUID
    mcname (str): 账号的 MC 用户名 
    
    返回 (登录失败时)
    ------------------------
    
    '''
    modAuth = Auth()
    modLog = ModLogging('MSAuth')
    
    try:
        # 微软登录验证 第一步
        modLog.write('微软登录 #1 开始', LT.INFO)
        xbl_token, uhs1 = modAuth.Auth_XBL(code_uri)
        modLog.write('微软登录 #1 完成', LT.INFO)
        # 微软登录验证 第二步
        modLog.write('微软登录 #2 开始', LT.INFO)
        xsts_token, uhs2 = modAuth.Auth_XSTS(xbl_token)
        modLog.write('微软登录 #2 结束', LT.INFO)
        # 验证
        if uhs1 != uhs2: raise VerifyUhsException()
        # 微软登录验证 第三步
        modLog.write('微软登录 #3 开始', LT.INFO)
        access_token = modAuth.GetMinecraftToken(uhs1, xsts_token)
        modLog.write('微软登录 #3 结束', LT.INFO)
        # 微软登录验证 第四步
        modLog.write('微软登录 #4 开始', LT.INFO)
        (haveJE, haveBE), (mcid, mcname) = modAuth.CheckLicense(access_token), modAuth.GetProfile(access_token)
        modLog.write('微软登录 #4 结束', LT.INFO)
        # 结束
        modLog.write(f'微软登录成功，用户 {mcname} 已登录', LT.INFO)
        return haveJE, haveBE, mcid, mcname
    except Exception as ex:
        modLog.write('微软登录失败', LT.ERROR)
        err = type(ex).__name__
        traceback = print_exc()
        return err, ex, traceback