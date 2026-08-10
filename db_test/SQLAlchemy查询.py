from datetime import datetime  # 从datetime模块导入datetime类, 用于处理日期时间类型的数据

from sqlalchemy import create_engine, Integer, String, DateTime, select, \
    or_  # 从sqlalchemy核心模块导入: create_engine(创建引擎), Integer(整型), String(字符串型), DateTime(日期时间型)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, Session # 从sqlalchemy.orm模块导入: Mapped(类型映射注解), mapped_column(列映射), DeclarativeBase(声明式基类), Session(会话对象)

# 1. 创建SQLAlchemy引擎, 管理数据库连接、配置信息
engine = create_engine("mysql+pymysql://root:xyb3306@localhost:3306/ai-partner",  # 创建数据库引擎, 连接MySQL数据库, 指定用户名root、密码xyb3306、主机localhost、端口3306、数据库名ai-partner
                       echo=True)  # echo=True : 由连接产生的 SQL 语句, 会输出在日志中;


# 2. 声明模型父类, 定义与数据库表映射的模型类 (ORM --> 对象关系映射 : 类 ---> 表)
class Base(DeclarativeBase):  # 定义Base类, 继承自DeclarativeBase, 作为所有ORM模型的声明式基类
    pass  # 空类体, Base仅用作所有模型类的统一父类, 不需要额外属性或方法


class AiMessage(Base):  # 定义AiMessage模型类, 继承自Base, 对应数据库中的ai_message表
    __tablename__ = "ai_message"  # 指定该模型映射到的数据库表名为"ai_message"

    # 格式 --> 属性名: Mapped[对象属性类型] = mapped_column(类型(SQLALchemy中的类型), 是否为空, 是否主键, 字段注释)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 定义id字段: 整型, 主键, 自增, 注释为'主键'
    session_id: Mapped[int] = mapped_column(Integer, nullable=False)  # 定义session_id字段: 整型, 不允许为空, 表示所属会话ID
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # 定义role字段: 字符串(最大长度20), 不允许为空, 表示消息角色(user/assistant)
    content: Mapped[str] = mapped_column(String(500), nullable=False)  # 定义content字段: 字符串(最大长度500), 不允许为空, 表示消息内容
    create_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # 定义create_time字段: 日期时间类型, 不允许为空, 表示消息创建时间

    def __repr__(self):  # 定义__repr__方法, 用于打印或调试时显示对象的字符串表示
        return f"<AiMessage(id={self.id}, session_id={self.session_id}, role={self.role}, content={self.content}, create_time={self.create_time})>"  # 返回包含所有字段值的格式化字符串, 方便调试查看对象信息


# 自动创建表
# Base.metadata.create_all(engine)  # 根据所有继承Base的模型类, 在数据库中自动创建对应的表(当前已注释, 需要时取消注释即可)

if __name__ == '__main__':  # 程序入口: 仅当直接运行该脚本时执行以下代码, 被导入时不执行
    # 3. 执行操作 - 新增数据
    # 3.1 获取操作数据库的会话对象session
    session = Session(engine)  # 创建一个数据库会话对象, 绑定到上面的engine引擎(注意: 此行创建的session未被使用, 后面用了with语句重新创建)

    # 3.2 执行操作
    with  session:  # 使用上下文管理器创建会话, 自动管理会话的生命周期(退出with块时自动关闭连接)
       # 1.1查询所有数据
       #  result_list = session.execute(select(AiMessage)).all()
       #  for result in result_list:
       #      print(result[0])

       #1.2从ai_message 表中查询指定字段role,content
        # result_list = session.execute(select(AiMessage.role, AiMessage.content)).all()
        # for result in result_list:
        #     print(result[0], result[1])
        #
        # print("------------------------"*3)
        # result_list = session.execute(select(AiMessage.role, AiMessage.content)).scalars().all()
        # for result in result_list:
        #     print(result)
        #2 条件查询
        # 1.3 查询id = 1
        # result = session.execute(select(AiMessage).where(AiMessage.id == 1)).scalars().one()
        # print(result)

        # 1.3  查询消息内容中包含 "你好" 的消息
        # result_list = session.execute(select(AiMessage).where(AiMessage.content.like('%你好%'))).scalars().all()
        # for result in result_list:
        #     print(result)

        # 1.3  查询 role 为 'user' 并且 'content' 中包含 "你好" 的消息  -- 默认: and ; ---> and_ : 多个条件通过and连接
        # result_list = session.execute(select(AiMessage).where(AiMessage.role == 'user', AiMessage.content.like('%你好%'))).scalars().all()
        # for result in result_list:
        #     print(result)

        # 2.3 查询 role 为 'user' 或者 'content' 中包含 "你好" 的消息 ---> or_ : 多个条件通过or连接
        # result_list =session.execute(select(AiMessage).where(or_(AiMessage.role == 'user',AiMessage.content.like('%你好%')))).scalars().all()
        # print(result_list)

        # 3. 排序查询
        # 3.1 查询 id为6 或者 role为'user' 的消息数据, 并按照创建时间降序排序, 如果创建时间相同则按照id升序
       # result_list = session.execute(select(AiMessage)
       #                               .where(or_(AiMessage.role == 'user',AiMessage.id == 6))
       #                               .order_by(AiMessage.create_time.desc(),AiMessage.id.asc())
       #                               ).scalars().all()
       # for result in result_list:
       #     print(result)
       # 3. 分页查询
       result_list = session.execute(select(AiMessage)
                                     .where(AiMessage.session_id ==1)
                                     .offset(0).limit(5)
                                     ).scalars().all()

       for result in result_list:
            print(result)

        