import botocore

from bush import color
from bush.aws.base import AWSBase


class IAM(AWSBase):
    USAGE = """
{} iam <Command> [options]

Commands
    * users
    * keys
    """

    SUB_COMMANDS = ['users', 'keys']

    def __init__(self, options):
        super().__init__(options, 'iam')

    def __get_users(self):
        users = self.client.list_users(MaxItems=1000)['Users']
        self.users = []
        for user in users:
            info = {}
            info['id'] = user['UserId']
            info['name'] = user['UserName']
            time_format = '%Y/%m/%d %H:%M:%S'
            info['creation_date'] = user['CreateDate'].strftime(time_format)
            info['Arn'] = user['Arn']
            self.users.append(info)

    def __get_access_keys(self, user_name=None):
        try:
            if user_name is not None:
                res = self.client.list_access_keys(
                    UserName=user_name,
                    MaxItems=1000
                )
            else:
                res = self.client.list_access_keys(
                    MaxItems=1000
                )
        except botocore.errorfactory.NoSuchEntityException:
            return []

        metadata = res.get('AccessKeyMetadata')
        if metadata is None:
            return []

        keys = []
        for key in metadata:
            data = {}
            data['id'] = key['AccessKeyId']
            data['user_name'] = key['UserName']
            time_format = '%Y/%m/%d %H:%M:%S'
            data['creation_date'] = key['CreateDate'].strftime(time_format)
            data['state'] = key['Status']
            keys.append(data)

        return keys

    def __correct_access_keys(self, user_names):
        if user_names == '':
            return self.__get_access_keys()

        keys = []
        self.__get_users()

        if self.__include_only_wild_card(user_names):
            for user in self.users:
                keys.extend(self.__get_access_keys(user['name']))
        else:
            for user_name in user_names:
                for user in self.users:
                    if user_name in user['name']:
                        keys.extend(self.__get_access_keys(user['name']))

        return keys

    def __include_only_wild_card(self, arr):
        try:
            arr.index('*')
            return True
        except:
            return False

    def __get_state(self, state):
        if state == 'Active':
            return color.green(state)
        elif state == 'Inactive':
            return color.red(state)
        else:
            return state

    def list_users(self):
        columns = [
            'id',
            'name',
            'creation_date',
            'Arn'
        ]

        self.__get_users()

        formats = []
        for i, column in enumerate(columns):
            max_len = len(column)
            for user in self.users:
                if len(user[column]) > max_len:
                    max_len = len(user[column])

            formats.append('{%s:<%s}' % (i, max_len + 1))

        list_format = ''.join(formats)
        header = list_format.format(*columns)

        users = sorted(self.users, key=lambda x: x['name'])

        page = []
        page.append(header)
        page.append('-' * (len(header) - 1))

        for user in users:
            info = []
            for key in user:
                info.append(user[key])
            page.append(list_format.format(*info))

        return page

    def list_access_keys(self):
        columns = [
            'id',
            'user_name',
            'creation_date',
            'state'
        ]

        options = self.options
        user_names = ''
        if (options.user_name):
            user_names = options.user_name.split(',')

        keys = self.__correct_access_keys(user_names)

        formats = []
        for i, column in enumerate(columns):
            max_len = len(column)
            for key in keys:
                if len(key[column]) > max_len:
                    max_len = len(key[column])

            formats.append('{%s:<%s}' % (i, max_len + 1))

        list_format = ''.join(formats)
        header = list_format.format(*columns)

        keys = sorted(keys, key=lambda x: x['user_name'])

        page = []
        page.append(header)
        page.append('-' * (len(header) - 1))

        for key in keys:
            info = []
            for k in key:
                if k == 'state':
                    info.append(self.__get_state(key[k]))
                else:
                    info.append(key[k])

            page.append(list_format.format(*info))

        return page
