class Car:
    wheel = 4       # 汽车的轮胎数量
    tax_rate = 0.1  # 购置税

    def __init__(self, c_brand, c_name, c_owner, c_price): # self 表示基于该类创建出来的当前对象
        self.brand = c_brand
        self.name = c_name
        self.price = c_price
        self.owner = c_owner    # 私有属性

    def running(self):
        print(f"{self.owner} 驾驶 {self.brand} 的 {self.name} 汽车, 正在在高速行驶")

    def stop(self):
        print(f"{self.owner} 驾驶 {self.brand} 的 {self.name} 汽车, 遇到红灯, 停下来了")

    def __control_fuel(self):
        print(f'{self.owner}正在猛踩油门')
    def control_fuel(self):
        self.__control_fuel()
if __name__ == '__main__':
    c1 = Car('BMW', 'X7', '王林', 800000)
    c1.control_fuel()