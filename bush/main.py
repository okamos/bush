import sys
import traceback

from bush import option
from bush.spinner import Spinner
from bush.aws.ec2 import EC2
from bush.aws.iam import IAM


def run():
    (options, args) = option.parse_args('bush')

    output = ''
    spinner = Spinner()
    spinner.start()

    try:
        output = run_aws(options, args)
    except:
        spinner.stop()
        traceback.print_exc()
        sys.exit(2)

    spinner.stop()
    if output:
        print('\n'.join(output))

def run_aws(options, args):
    if args[0] == 'ec2':
        ec2 = EC2(options)

        if args[1] == 'ls':
            output = ec2.ls()
        elif args[1] == 'images':
            output = ec2.images()

    if args[0] == 'iam':
        iam = IAM(options)

        if args[1] == 'users':
            output = iam.list_users()

        if args[1] == 'keys':
            output = iam.list_access_keys()

    return output
