from bush.aws.session import create_session


class AWSBase:
    # USAGE = ''
    # SUB_COMMANDS = []

    def __init__(self, options, resource_name):
        self.name = resource_name
        self.options = options
        self.session = create_session(options)

    @property
    def resource(self):
        if not hasattr(self, '__resource'):
            self.__set_resource()
        return self.__resource

    @property
    def client(self):
        if not hasattr(self, '__client'):
            self.__set_client()
        return self.__client

    def __set_resource(self):
        self.__resource = self.session.resource(self.name)

    def __set_client(self):
        self.__client = self.session.client(self.name)
