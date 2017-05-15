from bush.aws.base import AWSBase


class IAM(AWSBase):
    USAGE = """
%s iam <Command> [options]

Commands
    * users
    """[1:-1]

    SUB_COMMANDS = ["users"]

    def __init__(self, options):
        super().__init__(options, "iam")

    def __get_users(self):
        users = self.client.list_users(MaxItems=1000)['Users']
        self.users = []
        for user in users:
            info = {}
            info["id"] = user["UserId"]
            info["name"] = user["UserName"]
            time_format = "%Y/%m/%d %H:%M:%S"
            info["creation_date"] = user["CreateDate"].strftime(time_format)
            info["Arn"] = user["Arn"]
            self.users.append(info)

    def list_users(self):
        columns = [
            "id",
            "name",
            "creation_date",
            "Arn"
        ]

        self.__get_users()

        formats = []
        for i, column in enumerate(columns):
            max_len = 4
            for user in self.users:
                if (len(user[column]) > max_len):
                    max_len = len(user[column])

            formats.append("{%s:<%s}" % (i, max_len + 1))

        list_format = "".join(formats)
        header = list_format.format(*columns)

        users = sorted(self.users, key=lambda x: x['name'])

        page = []
        page.append(header)
        page.append("-" * (len(header)))

        for user in users:
            info = []
            for key in user:
                info.append(user[key])
            page.append(list_format.format(*info))

        return page
