from distro import like
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import create_engine, Integer, String, Date, DateTime, select, update, delete, and_, between, desc
from datetime import date, datetime

# 1. 创建引擎 - 管理数据库连接信息
engine = create_engine("mysql+pymysql://root:xyb3306@localhost:3306/0809", echo=True)  # 输出生成的SQL


# 2. 映射类与表的关系, 类中的属性与表中字段的关系 --> 所有映射类都需要继承Base
class Base(DeclarativeBase):
    pass


class Emp(Base):
    __tablename__ = "emp"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键")
    name: Mapped[str] = mapped_column(String(10), nullable=False, comment="姓名")
    gender: Mapped[int] = mapped_column(Integer, nullable=False, comment="性别, 1:男, 2:女")
    job: Mapped[int] = mapped_column(Integer, nullable=True,comment="职位, 1:班主任, 2:讲师, 3:学工主管, 4:教研主管, 5:咨询师")
    salary: Mapped[int] = mapped_column(Integer, nullable=False, comment="薪资")
    entry_date: Mapped[date] = mapped_column(Date, nullable=True, comment="入职日期")
    create_time: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="更新时间")

    def __repr__(self):
        return (f"(id:{self.id}, 姓名:{self.name}, 性别:{self.gender}, 职位:{self.job}, 工资:{self.salary}, "
                f"入职日期:{self.entry_date}, 创建日期:{self.create_time}, 更新日期:{self.update_time}\n)")


if __name__ == '__main__':
    with (Session(engine) as session):
#  1. 查询所有姓"李"的员工记录
#         result = session.execute(select(Emp).where(Emp.name.like("李%"))).scalars().all()
#         print(result)
#  2. 查询薪资高于20000的男性员工信息
#         result = session.execute(select(Emp).where(and_(Emp.salary >20000,Emp.gender == 1))).scalars().all()
#         print(result)

#  3. 查询同时满足 性别为女 且 职位是班主任 的员工
#         result = session.execute(select(Emp).where(and_(Emp.job == 2,Emp.gender == 2))).scalars().all()
#         print(result)

#  4. 查询薪资在5000-8000之间的咨询师（job=5）姓名 和 薪资, 并且按照薪资倒序排序
#         result = session.execute(select(Emp.name,Emp.salary)
#                                  .where(and_(Emp.job == 5,Emp.salary.between(5000,8000)))
#                                  .order_by(desc(Emp.salary))
#                                  ).all()
#         print(result)

#  5. 显示所有 女性 员工的信息，按薪资从高到低排序, 如果薪资相同再按入门日期升序排序
#         result = session.execute(select(Emp).where(Emp.gender == 2).order_by(desc(Emp.salary),Emp.entry_date)).scalars().all()
#         print(result)

#  6. 查询 2010-01-01 年之后入职 并且 性别为女 并且 姓名为两个字的 员工姓名, 薪资, 职位
#         result = session.execute(select(Emp.name,Emp.salary,Emp.job)
#                                  .where(and_(Emp.entry_date > '2010-01-01',Emp.gender == 2,Emp.name.like("__")))
#                                  ).all()
#         print(result)


#  7. 查询所有姓名为两个字, 并且薪资在 10000 到 20000 之间 的信息 , 并根据入职时间降序排序
#         result = session.execute(select(Emp).where(and_(Emp.name.like("__"),Emp.salary.between(10000,20000)))
#                                  .order_by(desc(Emp.entry_date))).scalars().all()
#         print(result)

#  8. 查询性别为女 , 职位为班主任的员工信息, 并且根据入职时间升序排序, 入职时间相同, 再按照薪资降序排序
#         result = session.execute(select(Emp).where(and_(Emp.gender == 2,Emp.job == 1))
#                                   .order_by(Emp.entry_date,desc(Emp.salary))).scalars().all()
#         print(result)

#  9. 查询所有姓名为三个字, 并且入职时间在 '2010-01-01' 到 '2020-01-01' 之间入职 的信息 , 并根据入职时间降序排序
#         result = session.execute(select(Emp).where(and_(Emp.name.like("___"),Emp.entry_date.between('2010-01-01','2020-01-01')))
#                                   .order_by(desc(Emp.entry_date))).scalars().all()
#         print(result)

#  10. 往表中插入2条数据 , 数据内容自己指定
#         session.add(Emp(name = '张无忌',gender = 1,job=3,salary=6000,entry_date = '2026-06-16 16:30:39',
#                         create_time='2026-06-17 16:30:39',update_time=datetime.now()))
#         session.add(Emp(name='周芷若', gender=1, job=3, salary=6000, entry_date='2026-06-16 16:30:39',
#                         create_time='2026-06-17 16:30:39', update_time=datetime.now()))
#         session.commit()

#  11. 修改id为 2,3,4,5,6 员工的数据, 将其职位调整为 '讲师', 入职时间调整为2026-01-01, 更新时间设置为当前时间 ;
#         session.execute(update(Emp).where(Emp.id.in_([2,3,4,5,6])).values(job=2,entry_date='2026-01-01',update_time=datetime.now()))
#         session.commit()

#  12. 删除id为 30, 31, 32, 33的员工信息
        session.execute(delete(Emp).where(Emp.id.in_([30,31,32,33])))
        session.commit()