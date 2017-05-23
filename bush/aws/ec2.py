import re
from bush import color
from bush.aws.base import AWSBase


class EC2(AWSBase):
    USAGE = """%prog ec2 <Command> [options]

Commands
    * ls
    * images
    * start
    * stop
    * remove
    """
    SUB_COMMANDS = ['ls', 'images', 'start', 'stop', 'remove']

    COLUMNS_HELP = """select columns, comma separated.
availability_zone,
image_id,
instance_id,
instance_type,
key_name,
launch_time,
private_dns_name,
private_ip_address,
public_dns_name,
public_ip_address,
security_groups,
state,
tag_Name
    """
    TAG_RE = re.compile(r'^tag_(.+)')

    def __init__(self, options):
        super().__init__(options, 'ec2')

    def __get_instances(self):
        filter_name = ''
        filter_values = ''
        options = self.options

        if options.instance_id:
            filter_name = 'instance-id'
            filter_values = options.instance_id.split(',')
        elif options.tag_name:
            filter_name = 'tag:Name'
            filter_values = options.tag_name.split(',')
        elif options.filter_name and options.filter_values:
            filter_name = options.filter_name
            filter_values = options.filter_values.split(',')
        else:
            self.instances = self.resource.instances.all()
            return

        f = {'Name': filter_name, 'Values': filter_values}
        self.instances = self.resource.instances.filter(Filters=[f])

    def __get_max_len(self, attr):
        max_len = len(attr)
        for instance in self.instances:
            try:
                val = getattr(instance, attr)
            except:
                val = ''
            if not type(val) is str:
                val = ''

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

    def __get_max_len_from_security_groups(self):
        max_len = 15  # <security_groups>
        for instance in self.instances:
            val = self.__get_security_group_names(instance.security_groups)

            if max_len < len(val):
                max_len = len(val)

        return max_len

    def __get_tag_value(self, tags, key):
        if tags is None:
            return ''

        for tag in tags:
            if tag['Key'] == key:
                return tag['Value']

        return ''

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

    def __get_state_with_image(self, image):
        state = image.state
        if state == 'available':
            return color.green(state)
        elif state == 'pending':
            return color.yellow(state)
        elif state == 'failed':
            return color.red(state)
        else:
            return state

    def __get_security_group_names(self, groups):
        names = []
        if groups:
            for g in groups:
                names.append(g['GroupName'])

        return ', '.join(names)

    def __get_list_format(self, headers):
        formats = []
        for i, header in enumerate(headers):
            tag_key = EC2.TAG_RE.match(header)
            if tag_key:
                len = self.__get_max_len_from_tag(tag_key.groups()[0], header)
            elif header == 'state':
                len = self.__get_max_len_from_state()
            elif header == 'availability_zone':
                len = 17  # <availability_zone>
            elif header == 'launch_time':
                len = 19  # YYYY/mm/dd HH:MM:SS
            elif header == 'security_groups':
                len = self.__get_max_len_from_security_groups()
            else:
                len = self.__get_max_len(header)
            formats.append('{%s:<%s}' % (i, len + 1))

        return ''.join(formats)

    def __is_non_filter(self):
        options = self.options
        iid = options.instance_id
        name = options.tag_name
        fil = options.filter_name and options.filter_values

        if iid or name or fil:
            return False
        return True

    def ls(self):
        default_columns = [
            'instance_id',
            'instance_type',
            'tag_Name',
            'public_ip_address',
            'private_ip_address',
            'state'
        ]

        other_columns = [
            'availability_zone',
            'image_id',
            'key_name',
            'launch_time',
            'private_dns_name',
            'public_dns_name',
            'security_groups',
        ]

        all_columns = default_columns + other_columns
        if self.options.columns:
            columns = []
            # unique
            for c in self.options.columns.split(','):
                if c not in columns:
                    columns.append(c)
        else:
            columns = default_columns

        headers = [h for h in columns if h in all_columns]

        self.__get_instances()

        i_info = []
        for instance in self.instances:
            line = {}
            for h in headers:
                tag_key = EC2.TAG_RE.match(h)
                if tag_key:
                    val = self.__get_tag_value(instance.tags,
                                               tag_key.groups()[0])
                elif h == 'availability_zone':
                    val = instance.placement['AvailabilityZone']
                elif h == 'launch_time':
                    if instance.launch_time:
                        time_format = '%Y/%m/%d %H:%M:%S'
                        val = instance.launch_time.strftime(time_format)
                elif h == 'security_groups':
                    val = self.__get_security_group_names(
                            instance.security_groups)
                elif h == 'state':
                    val = self.__get_state(instance)
                else:
                    val = getattr(instance, h) or ''
                line[h] = val or '-'

            i_info.append(line)

        list_format = self.__get_list_format(headers)
        header = list_format.format(*headers)

        order_by = self.options.order_by
        if order_by and order_by in headers:
            i_info = sorted(i_info, key=lambda x: x[order_by])
            if self.options.order == 'desc':
                i_info.reverse()

        page = []
        page.append(header)
        page.append('-' * (len(header) - 1))

        for line in i_info:
            l = []
            for k in line:
                l.append(line[k])
            page.append(list_format.format(*l))

        return page

    def images(self):
        columns = [
            'image_id',
            'name',
            'description',
            'creation_date',
            'state'
        ]

        if self.options.image_id:
            image_ids = self.options.image_id.split(',')
            images = self.resource.images.filter(ImageIds=image_ids)
        else:
            owners = ['self']
            images = self.resource.images.filter(Owners=owners)

        i_info = []
        for image in images:
            line = {}
            for column in columns:
                if column == 'state':
                    val = self.__get_state_with_image(image)
                else:
                    val = getattr(image, column)
                line[column] = val or '-'

            i_info.append(line)

        formats = []
        for i, column in enumerate(columns):
            l = len(column)
            for image in images:
                val = getattr(image, column) or ''
                if len(val) > l:
                    l = len(val)

            formats.append('{%s:<%s}' % (i, l + 1))
        list_format = ''.join(formats)
        header = list_format.format(*columns)

        i_info = sorted(i_info, key=lambda x: x['name'])

        page = []
        page.append(header)
        page.append('-' * (len(header) - 1))

        for line in i_info:
            l = []
            for k in line:
                l.append(line[k])
            page.append(list_format.format(*l))

        return page

    def start_instances(self):
        if self.__is_non_filter():
            return ['Filter id or name required.']

        self.options.columns = 'instance_id,tag_Name,state'
        self.__get_instances()

        instance_ids = []
        will_starts = []
        for instance in self.instances:
            will_start = {}
            state = instance.state['Code']
            if state == 80:
                instance_ids.append(instance.instance_id)
                will_start['instance_id'] = instance.instance_id
                will_start['tag_Name'] = self.__get_tag_value(
                    instance.tags, 'Name'
                )
                will_starts.append(will_start)

        if len(instance_ids) == 0:
            return ['Not found stopped instances']

        sorted_instances = sorted(
            will_starts, key=lambda x: x['instance_id']
        )

        startings = self.client.start_instances(
            InstanceIds=instance_ids
            )['StartingInstances']
        sorted_startings = sorted(startings, key=lambda x: x['InstanceId'])

        formats = []
        for i, column in enumerate(['instance_id', 'tag_Name']):
            max_len = len(max(w[column] for w in will_starts))
            formats.append('{%s:<%s}' % (i, max_len + 1))

        headers = ['instance_id', 'tag_Name']
        list_format = ''.join(formats)
        header = list_format.format(*headers)
        page = [header, '-' * (len(header) - 1)]

        for i, starting in enumerate(sorted_startings):
            if starting['CurrentState']['Code'] == 0:
                page.append(list_format.format(
                    sorted_instances[i]['instance_id'],
                    sorted_instances[i]['tag_Name']
                ))

        return page

    def stop_instances(self):
        if self.__is_non_filter():
            return ['Filter id or name required.']

        self.options.columns = 'instance_id,tag_Name,state'
        self.__get_instances()

        instance_ids = []
        will_stops = []
        for instance in self.instances:
            will_stop = {}
            state = instance.state['Code']
            if state == 16:
                instance_ids.append(instance.instance_id)
                will_stop['instance_id'] = instance.instance_id
                will_stop['tag_Name'] = self.__get_tag_value(
                    instance.tags, 'Name'
                )
                will_stops.append(will_stop)

        if len(instance_ids) == 0:
            return ['Not found running instances']

        sorted_instances = sorted(will_stops, key=lambda x: x['instance_id'])

        stoppings = self.client.stop_instances(
            InstanceIds=instance_ids
            )['StoppingInstances']
        sorted_stoppings = sorted(stoppings, key=lambda x: x['InstanceId'])

        formats = []
        for i, column in enumerate(['instance_id', 'tag_Name']):
            max_len = len(max(w[column] for w in will_stops))
            formats.append('{%s:<%s}' % (i, max_len + 1))

        headers = ['instance_id', 'tag_Name']
        list_format = ''.join(formats)
        header = list_format.format(*headers)
        page = [header, '-' * (len(header) - 1)]

        for i, stopping in enumerate(sorted_stoppings):
            if stopping['CurrentState']['Code'] == 64:
                page.append(list_format.format(
                    sorted_instances[i]['instance_id'],
                    sorted_instances[i]['tag_Name']
                ))

        return page

    def terminate_instances(self):
        if self.__is_non_filter():
            return ['Filter id or name required.']

        self.options.columns = 'instance_id,tag_Name,state'
        self.__get_instances()

        instance_ids = []
        will_terminates = []
        for instance in self.instances:
            will_terminate = {}
            state = instance.state['Code']
            if state == 16 or state == 80:
                instance_ids.append(instance.instance_id)
                will_terminate['instance_id'] = instance.instance_id
                will_terminate['tag_Name'] = self.__get_tag_value(
                    instance.tags, 'Name'
                )
                will_terminates.append(will_terminate)

        if len(instance_ids) == 0:
            return ['Not found running or stopped instances']

        sorted_instances = sorted(
            will_terminates, key=lambda x: x['instance_id']
        )

        terminating = self.client.terminate_instances(
            InstanceIds=instance_ids
            )['TerminatingInstances']
        sorted_terminating = sorted(terminating, key=lambda x: x['InstanceId'])

        formats = []
        for i, column in enumerate(['instance_id', 'tag_Name']):
            max_len = len(max(w[column] for w in will_terminates))
            formats.append('{%s:<%s}' % (i, max_len + 1))

        headers = ['instance_id', 'tag_Name']
        list_format = ''.join(formats)
        header = list_format.format(*headers)
        page = [header, '-' * (len(header) - 1)]

        for i, stopping in enumerate(sorted_terminating):
            page.append(list_format.format(
                sorted_instances[i]['instance_id'],
                sorted_instances[i]['tag_Name']
            ))

        return page
