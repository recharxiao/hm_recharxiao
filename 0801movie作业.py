'''
# ================================================================================
# 作业题 2：电影信息管理系统
# ================================================================================
"""
【需求说明】

1. 业务背景
   使用面向对象思想，开发一个电影信息管理系统，可对电影信息进行
   添加、修改、删除、精确查询、查询所有、查询评分最高等操作。

2. 涉及到的类
   2.1 Movie（电影类）
       - 实例属性：电影名(name)、导演(director)、主演(actor)、票价(price)、评分(score)
       - 方法：
           * __init__：初始化方法
           * __repr__：返回电影的字符串表示，格式为：
             "电影名: xxx | 导演: xxx | 主演: xxx | 票价: xxx | 评分: xxx"

   2.2 MovieSystem（电影信息管理系统类）
       - 类属性：system_name（系统名称）、system_version（系统版本号）
       - 实例属性：movie_dict（用于存放所有电影对象的字典）   【 提示: 字典类型 {"电影名1": movie对象, "电影名2": movie对象} 】
       - 方法：
           * __init__：初始化方法，创建一个空的 movie_dict
           * add_movie：添加电影
           * update_movie：修改电影
           * delete_movie：删除电影
           * query_movie：精确查询指定电影
           * list_movies：展示所有电影
           * top_rated_movie：查询评分最高的电影（若有并列，一并输出）
           * run：显示菜单并循环接收用户操作

3. 业务规则
   3.1 添加电影时：
       - 依次输入电影名、导演、主演、票价、评分
       - 电影名不能重复（已存在则提示并返回）
       - 票价必须大于 0，评分必须在 0-10 之间，否则提示并返回
   3.2 修改电影时：
       - 输入要修改的电影名
       - 若不存在则提示"未找到该电影"
       - 找到后依次输入新的导演、主演、票价、评分，并更新
   3.3 删除电影时：
       - 输入要删除的电影名
       - 若不存在则提示"未找到该电影"
   3.4 查询电影时：
       - 输入电影名进行精确查询
   3.5 查询评分最高电影时：
       - 遍历 movie_dict 找到评分最高的电影
       - 若有并列最高分，则一并输出

4. 菜单
       1. 添加电影   2. 修改电影   3. 删除电影
       4. 查询指定电影  5. 查询所有电影
       6. 查询评分最高电影  7. 退出系统
'''

menu = """
# # # # # # # # # # # # # # # # # # # # # # # 【电影信息管理系统菜单】 # # # # # # # # # # # # # # # # #
#  1. 添加电影   2. 修改电影   3. 删除电影   4. 查询指定电影   5. 查询所有电影   6. 查询评分最高电影   7. 退出系统  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""


# 电影类
class Movie:
    def __init__(self, name, director, actor, price, score):
        self.name = name
        self.director = director
        self.actor = actor
        self.price = price
        self.score = score

    def __repr__(self):
        return f"电影名: {self.name} | 导演: {self.director} | 主演: {self.actor} | 票价: {self.price} | 评分: {self.score}"


# 电影信息管理系统类
class MovieSystem:
    system_name = "电影信息管理系统"
    system_version = "V1.0"

    def __init__(self):
        self.movie_dict = {}

    def add_movie(self):
        name = input("请输入电影名：")
        if name in self.movie_dict:
            print("该电影已存在，请勿重复添加 ~")
            return
        director = input("请输入导演：")
        actor = input("请输入主演：")
        try:
            price = float(input("请输入票价："))
            score = float(input("请输入评分："))
        except ValueError:
            print("输入有误!!! 票价和评分必须为数字")
            return
        if price <= 0 or not (0 <= score <= 10):
            print("输入有误!!! 票价必须大于 0，评分必须在 0-10 之间")
            return
        self.movie_dict[name] = Movie(name, director, actor, price, score)
        print("电影信息添加成功 ~")

    def update_movie(self):
        name = input("请输入要修改的电影名：")
        if name not in self.movie_dict:
            print("未找到该电影")
            return
        director = input("请输入新的导演：")
        actor = input("请输入新的主演：")
        try:
            price = float(input("请输入新的票价："))
            score = float(input("请输入新的评分："))
        except ValueError:
            print("输入有误!!! 票价和评分必须为数字")
            return
        if price <= 0 or not (0 <= score <= 10):
            print("输入有误!!! 票价必须大于 0，评分必须在 0-10 之间")
            return
        movie = self.movie_dict[name]
        movie.director = director
        movie.actor = actor
        movie.price = price
        movie.score = score
        print("电影信息修改成功 ~")

    def delete_movie(self):
        name = input("请输入要删除的电影名：")
        if name in self.movie_dict:
            del self.movie_dict[name]
            print("电影信息删除成功 ~")
        else:
            print("未找到该电影")

    def query_movie(self):
        name = input("请输入要查询的电影名：")
        if name in self.movie_dict:
            print(self.movie_dict[name])
        else:
            print("未找到该电影")

    def list_movies(self):
        if not self.movie_dict:
            print("系统中暂无电影 ~")
            return
        for movie in self.movie_dict.values():
            print(movie)

    def top_rated_movie(self):
        if not self.movie_dict:
            print("系统中暂无电影 ~")
            return
        max_score = max(movie.score for movie in self.movie_dict.values())
        top_movies = [movie for movie in self.movie_dict.values() if movie.score == max_score]
        print(f"评分最高的电影（最高分：{max_score}）：")
        for movie in top_movies:
            print(movie)

    def run(self):
        while True:
            choice = input("欢迎使用" + self.system_name + " ~\t" + menu)
            match choice:
                case "1":
                    self.add_movie()
                case "2":
                    self.update_movie()
                case "3":
                    self.delete_movie()
                case "4":
                    self.query_movie()
                case "5":
                    self.list_movies()
                case "6":
                    self.top_rated_movie()
                case "7":
                    print("感谢使用，再见 ~")
                    break
                case _:
                    print("输入有误，请重新输入 ~")


if __name__ == '__main__':
    ms = MovieSystem()
    # 插入测试数据
    test_movies = [
        Movie("流浪地球", "郭帆", "吴京", 45.0, 8.9),
        Movie("哪吒之魔童降世", "饺子", "吕艳婷", 42.0, 9.5),
        Movie("你好，李焕英", "贾玲", "贾玲", 39.9, 8.8),
        Movie("战狼2", "吴京", "吴京", 49.9, 9.0),
        Movie("长津湖", "陈凯歌", "吴京", 50.0, 9.0),  # 与战狼2并列最高评分
    ]
    for movie in test_movies:
        ms.movie_dict[movie.name] = movie
    ms.run()
