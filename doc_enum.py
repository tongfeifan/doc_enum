# coding=utf-8
from enum import Enum


class AutoDocedEnum(Enum):
    """
    **带描述的自赋值枚举类**
    
    用于需要同时提供枚举数值和枚举描述,又要求枚举项命名高可读性的场合, 例如常见的错误类型,错误码和错误描述, 又或是状态名称, 状态值和状态描述等应用场景, 其枚举项如下:

    +-----------+-----------------------------------+----------------+
    |  枚举项   | ClientSideError.NotFound          |                |
    +-----------+-----------------------------------+----------------+
    |  枚举值   | ClientSideError.NotFound.value    | 404            |
    +-----------+-----------------------------------+----------------+
    |  枚举描述 | ClientSideError.NotFound.__doc__  | 资源找不到     |
    +-----------+-----------------------------------+----------------+

    继承该类时可以指定如下属性:

    +-----------------------+-----------------------+-----------------+
    |  属性名称             | 作用                  | 默认值          |
    +-----------------------+-----------------------+-----------------+
    |  __initial_number__   | 枚举值的初始值        | 0               |
    +-----------------------+-----------------------+-----------------+
    |  __dict_name__        | 枚举项名称对应的键名  | 'name'          |
    +-----------------------+-----------------------+-----------------+
    |  __dict_value__       | 枚举值对应的键名      | 'value'         |
    +-----------------------+-----------------------+-----------------+
    |  __dict_doc__         | 枚举描述对应的键名    | 'doc'           |
    +-----------------------+-----------------------+-----------------+


    继承该枚举时, 只需指定 **__initial_number__** 为某个整数, 则所有枚举值会依次+1, 其间还可以混合指定 **枚举项=(枚举值, 枚举描述)** , 例子如下: 

    .. code-block:: python

        from utils import AutoDocedEnum

        class ClientSideError(AutoDocedEnum):

            __initial_number__ = 400

            BadRequest = '错误的请求'
            Unauthorized = '客户端认证失败'
            PaymentRequired = '请先支付'
            Forbidden = '请求被拒绝'
            NotFound = '资源未找到'
            MethodNotAllowed = '所请求的方法未找到'
            RequestTimeout = (409, '客户请求超时')

            
    >>> print(ClientSideError.NotFound.value)
    404
    >>> print(ClientSideError.NotFound.__doc__)
    '资源未找到'
    >>> print(ClientSideError.RequestTimeout.value)
    409
    >>> print(ClientSideError.RequestTimeout.__doc__)
    '客户请求超时'
    >>> print(ClientSideError.get_choices)
    ((400, '错误的请求'), (401, '客户端认证失败'), (402, '请先支付'), (403, '请求被拒绝'), (404, '资源未找到'), (405, '所请求的方法未找到'), (409, '客户请求超时'))


    也可以忽略 **__initial_number__** , 全部手动指定枚举值和枚举描述, 例子如下:

    .. code-block:: python

        from utils import AutoDocedEnum

        class APIStatus(AutoDocedEnum):

            __dict_value__ = 'code'
            __dict_doc__ = 'msg'

            OK = ('0000', '请求完成')
            ERRORJSON = ('1001', '数据格式并非json')
            MISSING = ('1002', '参数"{}"不存在')
            INVALID = ('1003', '参数"{}"不合法')

            
    >>> print(APIStatus.MISSING.value)
    '1002'
    >>> print(APIStatus.MISSING.__doc__.format('http_method'))
    参数"http_method"不存在
    >>> print(APIStatus.MISSING.get_dict())
    {'msg': '参数"{}"不存在', 'code': '1002', 'name': 'MISSING'}

    """

    #: 指定一系列枚举值的起始值
    __initial_number__ = 1

    #: 枚举项名称对应的键名
    __dict_name__ = 'name'

    #: 枚举值对应的键名
    __dict_value__ = 'value'

    #: 枚举描述对应的键名
    __dict_doc__ = 'doc'

    def __new__(cls, *args):
        """
        生成新枚举项时, 将其值自动加1
        """
        cls.__last_number__ = getattr(cls, "__last_number__",
                                      cls.__initial_number__ - 1) + 1
        new_obj = object.__new__(cls)
        new_obj._value_ = cls.__last_number__
        return new_obj
    
    def __init__(self, *args):
        """
        初始化枚举项时赋值注释
        """
        if len(args) > 2:
            raise TypeError('初始化参数{args}的数量不能超过2个!'.format(args=args))
        try:
            value, *doc = args
            self.__doc__ = str(doc[0]) if doc else str(value)
            if doc:
                self._value_ = value
        except Exception:
            raise TypeError('初始化参数{args}未能转换为可读字符串!'.format(
                args=args))

    @classmethod
    def get_choices(cls):
        """
        **获取选项生成器** , 可用于Django字段的choices

        .. code-block:: python

            status = models.IntegerField(choices=APIStatus.get_choices(),
                                         default=APIStatus.OK.value,
                                         verbose_name='API状态')

        """
        return tuple((item.value, item.__doc__) for item in cls)

    def get_dict(self):
        """
        **获取枚举项对应的字典**

        >>> print(ClientSideError.BadRequest.get_dict())
        {'doc': '错误的请求', 'value': 400, 'name': 'BadRequest'}

        """
        return {self.__dict_name__: self.name,
                self.__dict_value__: self.value,
                self.__dict_doc__: self.__doc__}