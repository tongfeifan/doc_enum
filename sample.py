# coding=utf-8


from membership.utils import AutoDocedEnum


class HTTPError(Exception):
    """
    **HTTP异常**
    """
    def __init__(self, status, msg):
        self.status = status
        self.msg = msg
        super().__init__(self, self.status, self.msg)

        
class ErrorStatus(AutoDocedEnum):
    """
    **API返回状态**, 详细状态请点击上方的 *[source]* 查看

    追加新状态的格式如下:

    .. code-block:: python

        STATUS_NAME = ('status_code', 'status_msg')
        BAD_REQUEST = ('400', '错误的客户请求')
    """

    __dict_name__ = 'error'
    __dict_value__ = 'code'
    __dict_doc__ = 'msg'

    Unauthorized = ('10000', '认证未通过, 未知错误')
    MissingAPPID = ('10001', '认证未通过, 缺少appid')
    InvalidAPPID = ('10002', '认证未通过, appid不合法')
    MissingSign = ('10003', '认证未通过, 缺少sign')
    InvalidSign = ('10004', '认证未通过, sign不合法')
    Forbidden = ('10005', '未授权操作该资源')
    MissingTimestamp = ('10006', '认证未通过, 缺少timestamp')
    InvalidTimestamp = ('10007', '认证未通过, timestamp不合法')
    TimestampTimeout = ('10008', '认证未通过, 时间戳超时')

    BadRequest = ('20000', '数据格式错误, 未知错误')
    InvalidJSON = ('20001', '数据格式错误, body数据不符合json标准')
    MissingArguments = ('20002', '数据格式错误, 缺少{}参数')
    InvalidArguments = ('20003', '数据格式错误, 参数{}不合法')
    InvalidURI = ('20004', '数据格式错误, URI中{}不合法')
    WrongArguments = ('20005', '数据格式错误, 存在多余的参数{}')

    InterfaceError = ('30000', '接口错误, 未知错误')
    VendorInterfaceError = ('30001', '接口错误, 无法调用商超接口')
    EcommerceInterfaceError = ('30002', '接口错误, 无法调用渠道接口')
    InterfaceResultError = ('30003', '接口错误, 返回结果异常, 结果信息为:{}')

    BusinessError = ('40000', '业务错误, 未知错误')
    Existed = ('40001', '业务错误, 资源已存在')
    NotFound = ('40004', '业务错误, 资源不存在')
    RelationError = ('40005', '业务错误, 相关资源{}不可使用')

    InternalError = ('50000', '内部服务错误, 未知错误')
    DatabaseConnError = ('50001', '数据库错误, 无法连接数据库')
    TransactionError = ('50002', '数据库错误, 事务处理异常')
    DataReadingError = ('50003', '数据库错误, 数据读取异常')

    def get_msg(self, param=None):
        """
        **得到字典形式表达的报错消息**

        .. code-block:: python

            {
                "status": "1004",
                "msg": "products ['10001', '10002'] not found"
            }

        常用场景如下:

        .. code-block:: python

           param = ["10001", "10002"]
           return JsonResponse(APIStatus.ProductNotFound.get_msg(param))
        """
        dct = self.get_dict()
        if param:
            key = self.__dict_doc__
            dct[key] = dct[key].format(param)
        return dct

    def get_exception(self, status, param=None):
        """
        返回对应的异常
        """
        msg = self.get_msg(param)
        return HTTPError(status, msg)