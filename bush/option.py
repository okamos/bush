from optparse import OptionParser, OptionGroup

import sys

from . import __version__
from bush.aws.ec2 import EC2


def parse_args(prog_name):
    RESOURCES = ['ec2']
    usage = """
%s <Resource> [options]

Resources
    * ec2
    """[1:-1] % prog_name

    version = "%s %s" % (prog_name, __version__)

    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-p", "--profile",
                      action="store", type="string", dest="profile",
                      help="Use a specific profile from your credential file")
    parser.add_option("-r", "--region",
                      action="store", type="string", dest="region",
                      help="Use a specific region")
    parser.add_option("--access_key_id",
                      action="store", type="string", dest="access_key",
                      help="Use a specific AWS_ACCESS_KEY_ID")
    parser.add_option("--secret_key",
                      action="store", type="string", dest="secret_key",
                      help="Use a specific AWS_SECRET_ACCESS_KEY")

    if len(sys.argv) < 2 or not (sys.argv[1] in RESOURCES):
        parser.print_help()
        sys.exit(2)

    if sys.argv[1] == "ec2":
        parser.set_usage(EC2.USAGE % prog_name)
        group = OptionGroup(parser, "EC2 Options")
        group.add_option("--id", dest="instance_id",
                         help="filter instance ids, comma separated")
        group.add_option("--name", dest="tag_name",
                         help="filter tag_Name, comma separated")
        parser.add_option_group(group)

        if len(sys.argv) < 3 or not (sys.argv[2] in EC2.SUB_COMMANDS):
            parser.print_help()
            sys.exit(2)

        if sys.argv[2] == "ls":
            group.add_option("-c", "--columns", dest="columns",
                             help=EC2.COLUMNS_HELP)
            group.add_option("-o", "--order", dest="order",
                             help="list order, asc or desc")
            group.add_option("--order_by", dest="order_by",
                             help="order by column")

    return parser.parse_args()
