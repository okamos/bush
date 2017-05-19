import sys
import traceback

from bush.lack_args_error import LackArgsError

from bush import option
from bush.spinner import Spinner
from bush.aws.ec2 import EC2
from bush.aws.iam import IAM


def run():
    parser = option.build_parser()
    (options, args) = parser.parse_args()

    output = ''
    spinner = Spinner()
    spinner.start()

    try:
        output = run_aws(options, args)
    except LackArgsError:
        spinner.stop()
        parser.print_help()
        sys.exit(2)
    except:
        spinner.stop()
        traceback.print_exc()
        sys.exit(2)

    spinner.stop()
    if output:
        print('\n'.join(output))


def run_aws(options, args):
    output = ''
    args_len = len(args)

    if args_len < 2:
        raise LackArgsError()

    if args[0] == 'ec2':
        ec2 = EC2(options)

        if args[1] == 'ls':
            output = ec2.ls()
        elif args[1] == 'images':
            output = ec2.images()
    elif args[0] == 'iam':
        iam = IAM(options)

        if args[1] == 'users':
            output = iam.list_users()
        elif args[1] == 'keys':
            output = iam.list_access_keys()

    return output
