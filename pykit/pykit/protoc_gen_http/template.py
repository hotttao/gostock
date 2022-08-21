# from google.protobuf import descriptor_pb2


class MethodDetail:
    def __init__(self, name: str, original_name: str, num: int, request: str, reply: str,
                 path: str, method: str, has_vars: bool, has_body: bool, body: str,
                 response_body: str):
        """_summary_

            Args:
                name (str): _description_
                original_name (str): The parsed original name
                num (int): _description_
                request (str): _description_
                reply (str): _description_
                path (str): _description_
                method (str): _description_
                has_vars (bool): _description_
                has_body (bool): _description_
                body (str): _description_
                response_body (str): _description_

            Returns:
                _type_: _description_
        """
        self.name = name
        self.original_name = original_name
        self.num = num
        self.request = request
        self.reply = reply
        self.path = path
        self.method = method
        self.has_vars = has_vars
        self.has_body = has_body
        self.body = body
        self.response_body = response_body


class ServiceDetail:
    def __init__(self, service_type: str, service_name: str,
                 metadata: str, methods: MethodDetail = None):
        """_summary_

        Args:
            service_type (str): Greeter
            service_name (str): helloworld.Greeter
            metadata (str): api/helloworld/helloworld.proto
            methods (MethodDesc):
        """
        self.service_type = service_type
        self.service_name = service_name
        self.metadata = metadata
        self.methods = methods or []

    def execute(self) -> str:
        method_sets = {}
        for m in self.methods:
            method_sets[m.name] = m
        # 加载模板，生成代码
        return ''
