from functools import total_ordering


@total_ordering
class Car:
    """汽车类"""
    chelun = '车轮'
    chelun_num = 4
    def __del__(self):
        print(f"{self.brand} {self.name} 已被销毁")
    def __init__(self, color: str, brand: str, name: str, price: int):
        self.color = color
        self.brand = brand
        self.name = name
        self.price = price

    def running(self) -> None:
        """模拟汽车行驶"""
        print(f"{self.brand} {self.name} 正在高速行驶中....")

    def total_cost(self, discount: float, rate: float = 0.1) -> float:
        """计算总花费：裸车价 * 折扣 + 税费"""
        return self.price * discount + rate * self.price

    def __eq__(self, other) -> bool:
        return self.price == other.price

    def __ge__(self, other) -> bool:
        return self.price > other.price

    def __str__(self) -> str:
        return f"颜色是{self.color}，品牌是{self.brand}，名称是{self.name}，价格是{self.price}"

if __name__ == '__main__':
    print(Car.chelun,Car.chelun_num)
# 测试
    c1 = Car("白色", "BYD", "汉", 180000)
    print(c1)

    c2 = Car("白色", "BYD", "汉", 180001)
    print(c2)

    print(c1 == c2)

    print('c1>c2的结果是：',c1 > c2)

