class Recharxiao:
    """人设信息类"""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.sex = "男"
        self.height = 170
        self.weight = 60
        self.birthday = "1990-01-01"
        self.hobby = ["打篮球", "看电影", "看书"]
        self.favorite_food = ["火锅", "麻辣烫", "烧烤"]
        self.favorite_color = ["红色", "黄色", "蓝色"]
        self.favorite_book = ["三体", "三体2", "三体3"]

    def __str__(self) -> str:
        """面向用户的友好展示"""
        return f"{self.name}的年龄是{self.age}"

    def __repr__(self) -> str:
        """面向开发者的展示，遵循惯例返回可重建对象的表达式"""
        return f"Recharxiao(name={self.name!r}, age={self.age})"

    def show_birthday(self) -> str:
        """展示生日信息"""
        return f"{self.name}的生日是{self.birthday}"


if __name__ == "__main__":
    recharger = Recharxiao("recharger", 30)
    print(recharger.__dict__)
    print(recharger.show_birthday())
    print(repr(recharger))
    print(str(recharger))
