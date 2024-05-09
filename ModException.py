class XBLAuthingException(Exception):
    def __init__(self, message='XBL Authentication failed.'):
        self.message = message
        super().__init__(self.message)

class XSTSAuthingException(Exception):
    def __init__(self, message='XSTS Authentication failed.'):
        self.message = message
        super().__init__(self.message)

class MinecraftAuthingException(Exception):
    def __init__(self, message='Minecraft Authentication failed.'):
        self.message = message
        super().__init__(self.message)

class MinecraftCheckLicenseException(Exception):
    def __init__(self, message='Minecraft License Checking failed.'):
        self.message = message
        super().__init__(self.message)
        
class MinecraftGetProfileException(Exception):
    def __init__(self, message='Minecraft Profile Getting failed.'):
        self.message = message
        super().__init__(self.message)

class VerifyUhsException(Exception):
    def __init__(self, message='Verify UHS failed.'):
        self.message = message
        super().__init__(self.message)