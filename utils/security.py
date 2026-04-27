from passlib.context import CryptContext

# 改用 pbkdf2_sha256，兼容 Python 3.13，无 72 字节限制
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# 密码加密
def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 密码验证，返回布尔值
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)