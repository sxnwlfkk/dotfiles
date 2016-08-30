# I used this to parse args from a dotfile, after the cli args, but
# due to policy change (no args in dotfile), they are not needed.
# However, I don't want to delete them just yet.

def parse_dot_args(old_args, settings):
    if settings == None:
        return old_args
    else:
        parser = def_args()
        read_args = build_args_str(settings).split()
        new_args = parser.parse_args(args=read_args, namespace=old_args)
        return new_args


def build_args_str(settings_dict):
    arg_str = ''
    for key, value in settings_dict.items():
        arg_str += '--' + key + ' ' +  str(value) + ' '

    return arg_str
