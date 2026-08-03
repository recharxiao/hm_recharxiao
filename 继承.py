"""
继承: 描述的是两个类之间的关系, 子类继承父类, 就可以获取到父类中的属性和方法 (非私有)
重写: 是指子类继承父类后，如果父类中的方法不满足需求，可以在子类中重新定义父类中已有的方法（方法名相同），从而用子类的实现替换父类的实现。
"""
class Car:
    def __init__(self, brand, model, color, owner):
        self.brand = brand          # 品牌(公有属性)
        self.model = model          # 型号(公有属性)
        self.color = color          # 颜色(公有属性)
        self.__owner = owner        # 拥有者(私有属性)

    def start(self): # 启动
        print(f'{self.brand} {self.model} 正在启动...')

    def run(self): # 行驶
        print(f'{self.__owner} : {self.brand} {self.model} 正在行驶...')

    def stop(self): # 停止
        print(f'{self.brand} {self.model} 停止行驶...')

    def get_owner(self):
        return self.__owner[0:1] + "**"

    def charge(self):
        print(f'{self.brand} {self.model} 正在补充燃料...')

# 燃油车
class FuelCar(Car):
    def charge(self):
        # 方式一: super().方法名()
        # super().charge()

        # 方式二: 类名.方法名(self)
        Car.charge(self)
        print(f'{self.brand} {self.model} 正在加油...')

# 电车
class ElectricCar(Car):
    def charge(self):
        Car.charge(self)
        print(f'{self.brand} {self.model} 正在充电...')


if __name__ == '__main__':
    c1 = FuelCar("BMW", "X5", "黑色", "张三")
    c2 = ElectricCar("比亚迪", "秦L", "白色", "阎庆林")
    c1.charge()
    c2.run()
    c2.stop()
    c2.charge()