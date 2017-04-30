import re
from bush import color
from bush.aws.base import AWSBase

class EC2(AWSBase):
    USAGE = """
%s ec2 <Command> [options]

Commands
    * list
    """[1:-1]
    SUB_COMMANDS = ["ls"]
    TAG_RE = re.compile(r"^tag_(.+)")

    def __init__(self, options):
        super().__init__(options, "ec2")

    def __get_instances(self):
        # TODO: filter instances
        self.instances = self.resource.instances.all()

    def __get_max_len(self, attr):
        max_len = len(attr)
        for instance in self.instances:
            try:
                val = getattr(instance, attr)
            except:
                val = ""
            if not type(val) is str:
                val = ""

            if max_len < len(val):
                max_len = len(val)

        return max_len

    def __get_max_len_from_tag(self, key, header):
        max_len = len(header)
        for instance in self.instances:
            val = self.__get_tag_value(instance.tags, key)

            if max_len < len(val):
                max_len = len(val)

        return max_len

    def __get_max_len_from_state(self):
        max_len = 5  # <state>
        for instance in self.instances:
            val = instance.state['Name']

            if max_len < len(val):
                max_len = len(val)

        return max_len

    def __get_tag_value(self, tags, key):
        if tags is None:
            return ""

        for tag in tags:
            if tag['Key'] == key:
                return tag['Value']

        return ""

    def __get_state(self, instance):
        code = instance.state['Code']
        state = instance.state['Name']
        # ref http://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_InstanceState.html
        if code == 16:
            return color.green(state)
        elif code == 48 or code == 80:
            return color.red(state)
        elif code == 0 or code == 32 or code == 64:
            return color.yellow(state)
        else:
            return state

    def __get_list_format(self, headers):
        formats = []
        for i, header in enumerate(headers):
            tag_key = EC2.TAG_RE.match(header)
            if tag_key:
                len = self.__get_max_len_from_tag(tag_key.groups()[0], header)
            elif header == "state":
                len = self.__get_max_len_from_state()
            else:
                len = self.__get_max_len(header)
            formats.append("{%s:<%s}" % (i, len + 1))

        return "".join(formats)

    def ls(self):
        # TODO: choose columns
        headers = [
            "instance_id",
            "instance_type",
            "tag_Name",
            "public_ip_address",
            "private_ip_address",
            "state"
        ]
        order_column = 'tag_Name'

        self.__get_instances()

        i_info = []
        for instance in self.instances:
            line = {}
            for h in headers:
                tag_key = EC2.TAG_RE.match(h)
                if tag_key:
                    val = self.__get_tag_value(instance.tags,
                                               tag_key.groups()[0])
                elif h == "state":
                    val = self.__get_state(instance)
                else:
                    val = getattr(instance, h) or ""
                line[h] = val or "-"

            i_info.append(line)

        list_format = self.__get_list_format(headers)
        header = list_format.format(*headers)
        print(header)
        print("-" * len(header))
        sorted_list = sorted(i_info, key=lambda x: x[order_column])
        for line in sorted_list:
            l = []
            for k in line:
                l.append(line[k])
            print(list_format.format(*l))
