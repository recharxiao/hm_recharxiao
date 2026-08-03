menu = """
# # # # # # # # # # # # # # # # # # # # # # # 【图书管理系统菜单】 # # # # # # # # # # # 
#       1. 添加图书  2. 修改图书  3. 删除图书  4. 查询图书  5. 列出所有图书  6. 退出系统     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##
"""
class Book:
    def __init__(self, title, author, price, stock):
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock

    def __repr__(self):
        return f"书名：{self.title} | 作者：{self.author} | 价格：{self.price} | 库存：{self.stock}"


# 教务管理系统类
class BookSystem:
    system_version = "V1.0"
    system_name = '华为鸿蒙'

    def __init__(self):
        self.book_dict = {}
    def add_book(self):
        name = input("请输入图书姓名：")
        # 校验学生姓名是否存在
        if name in self.book_dict:
            print("该图书信息已存在")
            return
        author = input("请输入图书作者：")
        price = int(input("请输入图书价格："))
        stock = int(input("请输入图书库存："))
        if 0 <= price and 0 <= stock:
            b = Book(name, author, price, stock)
            self.book_dict[name] = b
            print("图书信息添加成功 ~")
        else:
            print("输入有误!!! 所有的图书价格和库存都必须大于0")
    def del_book(self):
        name = input("请输入要删除的图书名称：")
        if name in self.book_dict:
            del self.book_dict[name]
            print("图书信息删除成功 ~")
        else:
            print("未找到该图书")
    def updata_book(self):
        name = input("请输入要修改的图书名称：")
        if name in self.book_dict:
            author = input("请输入图书作者：")
            price = int(input("请输入图书价格："))
            stock = int(input("请输入图书库存："))
            if 0 <= price and 0 <= stock:
                b = Book(name, author, price, stock)
                self.book_dict[name] = b
                print("图书信息修改成功 ~")
            else:
                print("输入有误!!! 所有的图书价格和库存都必须大于0")
        else:
            print("未找到该图书")
    def select_book(self):
        name = input("请输入要查询的图书名称：")
        if name in self.book_dict:
            print(self.book_dict[name])
        else:
            print("未找到该图书")
    def all_book(self):
        for book in self.book_dict:
            print(self.book_dict[book])
    def run(self):
        while True:
            input_str = input("欢迎使用图书管理系统 ~\t"+menu)
            match input_str:
                case "1":
                    self.add_book()
                case "2":
                    self.updata_book()
                case "3":
                    self.del_book()
                case "4":
                    self.select_book()
                case "5":
                    self.all_book()
                case "6":
                    break
                case _:
                    print("输入有误，请重新输入 ~")


if __name__ == '__main__':
    book = BookSystem()
    book.run()

