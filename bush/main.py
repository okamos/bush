from bush import option
from bush.spinner import Spinner
from bush.aws.ec2 import EC2
from bush.aws.iam import IAM


def run():
    (options, args) = option.parse_args("bush")

    output = ''
    spinner = Spinner()
    spinner.start()

    if args[0] == 'ec2':
        ec2 = EC2(options)

        if args[1] == 'ls':
            output = ec2.ls()
        elif args[1] == "images":
            output = ec2.images()

    if args[0] == 'iam':
        iam = IAM(options)

        if args[1] == 'users':
            output = iam.list_users()

        if args[1] == 'keys':
            output = iam.list_access_keys()

    spinner.stop()
    if output:
        print("\n".join(output))
