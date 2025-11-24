
person = {
    "name": "Alice",
    "age": 25,
    "is_student": False
}

# 访问值（通过键）
print(person["name"])  # 输出：Alice
print(person.get("age"))  # 输出：25（get方法更安全，键不存在时返回None）

# 修改值
person["age"] = 26

# 添加键值对
person["gender"] = "female"

# 删除键值对
del person["is_student"]
person.pop("gender")  # 弹出并返回值

