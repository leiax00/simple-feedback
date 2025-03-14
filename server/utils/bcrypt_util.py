import bcrypt

def hash_password(password: str) -> str:
    """加密密码"""
    salt = bcrypt.gensalt(rounds=10)  # rounds=10 和 Spring Security 默认的 work factor 一致
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def verify_password(password: str, hashed_password: str) -> bool:
    """验证密码"""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


if __name__ == '__main__':
    plain_password = "admin@2025"
    pwd = hash_password(plain_password)
    pwd1 = hash_password(plain_password)

    print("哈希后的密码:", pwd)
    print("哈希后的密码1:", pwd1)
    print("密码匹配:", verify_password("admin@2025", '$2b$10$Dul694SFQROmjySbVqDRne9uYx4a/24A.w.vKHp5ihHR5V3lO.vHe'))  # True
    print("密码匹配:", verify_password("admin@2025", pwd1))  # True
    print("密码错误:", verify_password("wrong_password", pwd))  # False