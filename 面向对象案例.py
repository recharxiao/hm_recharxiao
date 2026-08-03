"""
采用面向对象的编程思想，完成教务管理系统的开发。教务管理系统可以管理在校学生的成绩信息，通过控制台菜单与用户交互，具体的功能如下：
    1. 添加学生成绩：根据输入的学生姓名、语文成绩、数学成绩、英语成绩，记录在系统中
        1.1 输入学生姓名、语文成绩、数学成绩、英语成绩
        1.2 检查学生姓名是否已存在, 如果学生不存在, 再添加 (存在则, 不添加)
        1.3 验证成绩范围（0-100分）
        1.4 创建学生对象并添加到系统
    2. 修改学生成绩：根据输入的学生姓名，修改对应的学生成绩
        2.1 输入要修改的学生姓名
        2.2 根据姓名查找该学生, 显示该生当前成绩信息
        2.3 输入新的语文、数学、英语成绩
        2.4 更新学生成绩数据
    3. 删除学生成绩：根据输入的学生姓名，删除对应的学生成绩
    4. 查询指定学生成绩：根据输入的学生姓名，查找对应的学生成绩，并输出
        4.1 输出格式为: "姓名：张三 | 语文：85 | 数学：90 | 英语：88 | 总分：263"
    5. 展示全部学生成绩：展示出系统中所有学生的成绩
"""


# 学生类
class Student:
    def __init__(self, s_name, s_chinese, s_math, s_english):
        self.name = s_name
        self.chinese = s_chinese
        self.math = s_math
        self.english = s_english

    def __repr__(self):
        return f"姓名：{self.name} | 语文：{self.chinese} | 数学：{self.math} | 英语：{self.english} | 总分：{self.chinese + self.math + self.english}"


# 教务管理系统类
class EduManagement:
    version = "V1.0"

    # 定义实例属性 --> {"王林": stu对象, "张三": stu对象}
    def __init__(self):
        self.student_dict = {}

    # 添加学生成绩
    def add_stu(self):
        name = input("请输入学生姓名：")
        # 校验学生姓名是否存在
        if name in self.student_dict:
            print("该学生信息已存在")
            return

        # 录入学生成绩
        chinese = int(input("请输入学生语文成绩："))
        math = int(input("请输入学生数学成绩："))
        english = int(input("请输入学生英语成绩："))

        # 判断成绩有效性
        if 0 <= chinese <= 100 and 0 <= math <= 100 and 0 <= english <= 100:
            s = Student(name, chinese, math, english)
            self.student_dict[name] = s
            print("学生信息添加成功 ~")
        else:
            print("输入有误!!! 所有的学生成绩都必须在0-100之间")

    # 修改学生成绩
    def update_stu(self):
        name = input("请输入学生姓名：")

        # 校验学生姓名是否存在
        if name not in self.student_dict:
            print("该学生信息不存在")
            return

        # 获取到要修改的学生信息
        stu = self.student_dict[name]
        print("要修改的学生原始信息如下: ")
        print(stu)

        # 录入学生成绩
        chinese = int(input("请输入学生修改后的语文成绩："))
        math = int(input("请输入学生修改后的数学成绩："))
        english = int(input("请输入学生修改后的英语成绩："))

        # 判断成绩有效性
        if 0 <= chinese <= 100 and 0 <= math <= 100 and 0 <= english <= 100:
            stu.chinese = chinese
            stu.math = math
            stu.english = english
            print("学生信息修改成功 ~")
        else:
            print("输入有误!!! 所有的学生成绩都必须在0-100之间")

    # 删除学生成绩
    def del_stu(self):
        name = input("请输入要删除的学生姓名：")
        # 校验学生姓名是否存在
        if name not in self.student_dict:
            print("该学生信息不存在")
            return

        # 删除
        del self.student_dict[name]
        print("删除学生信息成功~")

    # 查询指定学生成绩
    def query_stu(self):
        name = input("请输入要查询的学生姓名：")
        # 校验学生姓名是否存在
        if name not in self.student_dict:
            print("该学生信息不存在")
            return

        print(self.student_dict[name])

    # 展示全部学生成绩
    def query_all_stu(self):
        print("全部学生信息如下: ")
        for s in self.student_dict.values():
            print(s)

    # 运行系统方法
    def run(self):
        print("######## 欢迎您访问教务管理系统 ########")

        while True:
            print()
            print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
            print("# 1.添加学生   2.修改学生   3.删除学生   4.查询指定学生   5.查询所有学生   6.退出系统   #")
            print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
            print()

            choice = input("请选择要执行的操作, 输入1-6: ")
            match choice:
                case "1":  # 添加学生
                    self.add_stu()
                case "2":  # 修改学生
                    self.update_stu()
                case "3":  # 删除学生
                    self.del_stu()
                case "4":  # 查询指定学生
                    self.query_stu()
                case "5":  # 查询所有学生
                    self.query_all_stu()
                case "6":  # 退出系统
                    print("Bye ~")
                    break
                case _:  # 其他情况
                    print("输入错误, 请选择1-6之间的菜单功能!")


# 运行测试
if __name__ == '__main__':
    edu = EduManagement()
    edu.run()