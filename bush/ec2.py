from bush.session import create_session

import re
from bush import color


SUB_COMMANDS = ["ls"]
TAG_RE = re.compile(r"^tag_(.+)")


def usage(prog_name):
    return """
%s ec2 <Command> [options]

Commands
    * list
    """[1:-1] % prog_name


def get_resource(options):
    session = create_session(options)
    return session.resource("ec2")


def get_max_len(instances, attr):
    l = len(attr)
    for i in instances:
        try:
            val = getattr(i, attr)
        except:
            val = ""
        if not type(val) is str:
            val = ""

        if l < len(val):
            l = len(val)

    return l


def get_max_tag_len(instances, key, header):
    l = len(header)
    for i in instances:
        val = get_tag_value(i.tags, key)
        if l < len(val):
            l = len(val)

    return l


def get_max_state_len(instances):
    l = 5  # <state>
    for i in instances:
        val = i.state['Name']
        if l < len(val):
            l = len(val)

    return l


def get_tag_value(tags, key):
    if tags is None:
        return ""

    for tag in tags:
        if tag['Key'] == key:
            return tag['Value']

    return ""


def get_state(instance):
    code = instance.state['Code']
    state = instance.state['Name']
    if code == 16:
        return color.green(state)
    elif code == 48 or code == 80:
        return color.red(state)
    elif code == 0 or code == 32 or code == 64:
        return color.yellow(state)
    else:
        return state


def get_list_format(instances, headers):
    formats = []
    for i, h in enumerate(headers):
        tag_key = TAG_RE.match(h)
        if tag_key:
            len = get_max_tag_len(instances, tag_key.groups()[0], h)
        elif h == "state":
            len = get_max_state_len(instances)
        else:
            len = get_max_len(instances, h)
        formats.append("{%s:<%s}" % (i, len + 1))

    return "".join(formats)


def list(options):
    ec2 = get_resource(options)
    instances = ec2.instances.all()
    headers = [
        "instance_id",
        "instance_type",
        "tag_Name",
        "public_ip_address",
        "private_ip_address",
        "state"
    ]
    ret = []
    for i in instances:
        line = {}
        for h in headers:
            tag_key = TAG_RE.match(h)
            if tag_key:
                val = get_tag_value(i.tags, tag_key.groups()[0])
            elif h == "state":
                val = get_state(i)
            else:
                val = getattr(i, h) or ""
            line[h] = val or "-"

        ret.append(line)

    list_format = get_list_format(instances, headers)
    header = list_format.format(*headers)
    print(header)
    print("-" * len(header))
    sorted_list = sorted(ret, key=lambda x: x['tag_Name'])
    for line in sorted_list:
        l = []
        for k in line:
            l.append(line[k])
        print(list_format.format(*l))
