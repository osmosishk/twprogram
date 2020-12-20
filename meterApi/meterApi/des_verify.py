from pyDes import des, CBC, PAD_PKCS5
import binascii
 
# 密鑰
KEY='mHAxsLYz'
def des_encrypt(s):
    """
    DES 加密
    :param s: 原始字串
    :return: 加密後字串，16進制
    """
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)
 
 
def des_descrypt(s):
    """
    DES 解密
    :param s: 加密後的字串，16進制
    :return:  解密後的字串
    """
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de