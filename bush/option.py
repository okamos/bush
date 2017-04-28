from optparse import OptionParser

import __init__

def parse_args(prog_name):
    usage = "%s arg1 [options]" % prog_name
    version = "%s %s" % (prog_name, __init__.__version__)

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

    return parser.parse_args()
