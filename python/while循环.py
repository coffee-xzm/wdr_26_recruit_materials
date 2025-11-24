
password = "123456"
input_pwd = ""

while input_pwd != password:
    input_pwd = input("请输入密码: ")
    if input_pwd != password:
        print("密码错误，请重新输入")

print("密码正确，登录成功")

