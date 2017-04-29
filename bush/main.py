import option
import ec2


(options, args) = option.parse_args("bush")

if args[0] == 'ec2':
    if args[1] == 'ls':
        ec2.list(options)
