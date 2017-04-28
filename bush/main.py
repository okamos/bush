import option
from session import create_session


(options, args) = option.parse_args("Bush")
session = create_session(options)
