from bush import option
from bush.aws.ec2 import EC2
from bush.aws.iam import IAM


def run():
    (options, args) = option.parse_args("bush")

    if args[0] == 'ec2':
        ec2 = EC2(options)

        if args[1] == 'ls':
            ec2.ls()
        elif args[1] == "images":
            ec2.images()

    if args[0] == 'iam':
        iam = IAM(options)

        if args[1] == 'users':
            iam.list_users()
