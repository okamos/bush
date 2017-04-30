from bush.aws.session import create_session


class AWSBase:
    # USAGE = ""
    # SUB_COMMANDS = []

    def __init__(self, options, resource_name):
        self.session = create_session(options)
        self.resource = self.session.resource(resource_name)
        self.name = resource_name