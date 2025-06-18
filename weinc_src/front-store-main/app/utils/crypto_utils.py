import base64
import binascii
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad


class AES128:
    """
    암호화 모듈 (AES 128)
    """
    def __init__(self, key, iv):
        self.BS = AES.block_size
        # 암호화 키중 16자리만 잘라서 쓴다.
        self.encrypt_key = key[:16]
        self.iv = iv
        self.pad = lambda s: bytes(s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS), 'utf-8')
        self.unpad = lambda s: s[0:-ord(s[-1:])]

    def encrypt(self, raw):
        raw = self.pad(raw)
        cipher = AES.new(self.encrypt_key, AES.MODE_CBC, self.iv)

        return b64encode(cipher.encrypt(raw)).decode("utf-8")

    def decrypt(self, enc, encoding):
        enc = b64decode(enc)
        cipher = AES.new(self.encrypt_key, AES.MODE_CBC, self.iv)

        return self.unpad(cipher.decrypt(enc)).decode(encoding)

class AES256:
    """
    암호화 모듈 (AES 256) [key,iv 길이 32글자]
    """
    def __init__(self, key, iv):
        self.bs = 32
        self.key = binascii.unhexlify(AES256.str_to_bytes(key))
        self.iv = binascii.unhexlify(AES256.str_to_bytes(iv))

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * AES256.str_to_bytes(chr(self.bs - len(s) % self.bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    def encrypt(self, raw):
        raw = self._pad(AES256.str_to_bytes(raw))
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return binascii.hexlify(cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        enc = binascii.unhexlify(AES256.str_to_bytes(enc))
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self._unpad(cipher.decrypt(enc)).decode('utf-8')


class AES256ECB:
    """
    암호화 모듈 (AES 256 / ECB) [key 길이 32글자]
    """
    def __init__(self, key):
        self.key = key.encode()

    def encrypt_ecb(self, data):
        cipher = AES.new(self.key, AES.MODE_ECB)  # ECB 모드
        padded_data = pad(data.encode(), AES.block_size)  # PKCS5Padding 적용
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode()  # Base64로 인코딩하여 반환

    # AES-256 ECB 복호화
    def decrypt_ecb(self, encrypted_data):
        cipher = AES.new(self.key, AES.MODE_ECB)  # ECB 모드
        decrypted = cipher.decrypt(base64.b64decode(encrypted_data))
        return unpad(decrypted, AES.block_size).decode()  # PKCS5Padding 제거 후 반환


class RSACipher:
    """
    RSA 암호화 모듈\n
    개인키(비번X) 생성 [openssl genrsa -out private_key.pem 1024]\n
    개인키(비번) 생성 [openssl genrsa -des3 -out enc_private_key.pem 1024]\n
    개인키(기존 키에 비번) 생성 [openssl rsa -des3 -in private_key.pem -out enc_private_key.pem]\n
    공개키 생성(개인 키에 비번이 있다면 입력) [openssl rsa -in private_key.pem -out public_key.pem -pubout]
    """
    @staticmethod
    def encrypt(raw, public_key):
        """
        암호화
        :param raw: 평문
        :param public_key:공개키
        :return:
        """
        key = RSA.importKey(public_key)
        cipher = PKCS1_OAEP.new(key)
        encrypted = cipher.encrypt(raw.encode('utf-8'))
        return b64encode(encrypted).decode('utf-8')

    @staticmethod
    def decrypt(enc: str, private_key: str, pw: str = ''):
        """
        복호화
        :param enc:암호문
        :param private_key:개인키
        :param pw:개인키 암호
        :return:
        """
        key = RSA.importKey(private_key, passphrase=pw)
        cipher = PKCS1_OAEP.new(key)
        return cipher.decrypt(b64decode(enc)).decode('utf-8')
