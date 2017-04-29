from optparse import OptionParser, OptionGroup

import sys

from . import __version__
from bush import ec2


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

    if sys.argv[1] == 'ec2':
        parser.set_usage(ec2.usage(prog_name))
        group = OptionGroup(parser, "EC2 Options")
        # group.add_option("-c", "--column", dest="columns",
        #                  help="columns are")
        parser.add_option_group(group)

        if len(sys.argv) < 3 or not (sys.argv[2] in ec2.SUB_COMMANDS):
            parser.print_help()
            sys.exit(2)

    return parser.parse_args()
