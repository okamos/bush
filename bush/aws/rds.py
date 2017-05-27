from bush import color
from bush.aws.base import AWSBase


class RDS(AWSBase):
    USAGE = """%prog rds <Command> [options]

Commands
    * ls
    """

    SUB_COMMANDS = ['ls']

    def __init__(self, options):
        super().__init__(options, 'rds')

    def __get_instances_internal(self):
        filter_name = ''
        filter_values = ''
        options = self.options

        if options.db_instance_id:
            filter_name = 'db-instance-id'
            filter_values = options.db_instance_id.split(',')
        else:
            return self.client.describe_db_instances()

        f = {'Name': filter_name, 'Values': filter_values}
        return self.client.describe_db_instances(Filters=[f])

    def __get_instances(self):
        instances = self.__get_instances_internal()['DBInstances']
        self.instances = []
        for instance in instances:
            row = {}
            row['id'] = instance['DBInstanceIdentifier']
            row['instance_type'] = instance['DBInstanceClass']
            row['engine'] = instance['Engine']
            row['username'] = instance['MasterUsername']
            row['db_name'] = instance['DBName']
            endpoint = instance['Endpoint']
            row['endpoint'] = endpoint['Address']
            row['port'] = str(endpoint['Port'])
            row['multi_az'] = str(instance['MultiAZ'])
            row['state'] = instance['DBInstanceStatus']

            self.instances.append(row)

    def __get_state(self, state):
        if state == 'available':
            return color.green(state)
        if state == 'deleting' or state == 'failed' or state == 'storage-full':
            return color.red(state)
        if state == 'creating' or state == 'modirying' or state == 'rebooting':
            return color.yellow(state)
        else:
            return state

    def ls(self):
        columns = [
            'id',
            'instance_type',
            'engine',
            'username',
            'db_name',
            'endpoint',
            'port',
            'multi_az',
            'state'
        ]

        self.__get_instances()

        formats = []
        for i, column in enumerate(columns):
            max_len = len(column)
            for instance in self.instances:
                val = instance[column] or ''
                if len(val) > max_len:
                    max_len = len(val)

            formats.append('{%s:<%s}' % (i, max_len + 1))

        list_format = ''.join(formats)
        header = list_format.format(*columns)

        page = []
        page.append(header)
        page.append('-' * (len(header) - 1))

        for instance in self.instances:
            row = []
            for key in instance:
                if key == 'state':
                    row.append(self.__get_state(instance[key]))
                else:
                    row.append(instance[key])

            page.append(list_format.format(*row))

        return page
