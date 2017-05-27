from optparse import OptionParser, OptionGroup

import sys

from . import __version__
from bush.aws.ec2 import EC2
from bush.aws.iam import IAM
from bush.aws.rds import RDS


def build_parser():
    usage = """%prog <Resource> [options]

Resources
    * ec2
    * iam
    * rds
    """

    parser = OptionParser(usage=usage, version='%prog {}'.format(__version__))
    parser.add_option('-p', '--profile',
                      action='store', type='string', dest='profile',
                      help='Use a specific profile from your credential file')
    parser.add_option('-r', '--region',
                      action='store', type='string', dest='region',
                      help='Use a specific region')
    parser.add_option('--access_key_id',
                      action='store', type='string', dest='access_key',
                      help='Use a specific AWS_ACCESS_KEY_ID')
    parser.add_option('--secret_key',
                      action='store', type='string', dest='secret_key',
                      help='Use a specific AWS_SECRET_ACCESS_KEY')
    parser.add_option('--dry-run', type='string', dest='dry_run',
                      help='')

    argv_len = len(sys.argv)

    if argv_len >= 2 and sys.argv[1] == 'ec2':
        parser.set_usage(EC2.USAGE)
        group = OptionGroup(parser, 'EC2 Options')
        group.add_option('--id', dest='instance_id',
                         help='filter instance ids, comma separated')
        group.add_option('-n', '--name', dest='tag_name',
                         help='filter Name tag, comma separated')
        group.add_option('--filter_name', dest='filter_name',
                         help='Use a specific filter name')
        group.add_option('--filter_values', dest='filter_values',
                         help='filter values, comma separated')
        parser.add_option_group(group)

        if argv_len >= 3:
            if sys.argv[2] == 'ls':
                group.add_option('-c', '--columns', dest='columns',
                                 help=EC2.COLUMNS_HELP)
                group.add_option('-o', '--order', dest='order',
                                 help='list order, asc or desc')
                group.add_option('--order_by', dest='order_by',
                                 help='order by column')

            if sys.argv[2] == 'images':
                group.add_option('-i', '--image_id', dest='image_id',
                                 help='filter image ids, comma separated')

    if argv_len >= 2 and sys.argv[1] == 'iam':
        parser.set_usage(IAM.USAGE)
        group = OptionGroup(parser, 'IAM Options')
        parser.add_option_group(group)

        if argv_len >= 3 and sys.argv[2] == 'keys':
            group.add_option('-n', '--name', dest='user_name',
                             help='filter user names, comma separated, or *')

    if argv_len >= 2 and sys.argv[1] == 'rds':
        parser.set_usage(RDS.USAGE)
        group = OptionGroup(parser, 'RDS Options')
        parser.add_option_group(group)

        if argv_len >= 3 and sys.argv[2] == 'ls':
            group.add_option('--id', dest='db_instance_id',
                             help='filter instance ids, comma separated, or *')

    return parser
