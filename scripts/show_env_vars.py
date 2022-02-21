import sys
from typing import Union

from pydantic import BaseSettings

from app.settings import settings


def env_vars(conf):
    d = dict()
    for k, v in conf.__fields__.items():
        ins = getattr(conf, k)
        if isinstance(ins, BaseSettings):
            d.update(env_vars(ins))
        else:
            d[conf.__config__.env_prefix + k.upper()] = dict(
                current=ins, field=v)

    return d


def vars_to_stdout(with_color=True):
    d = env_vars(settings)
    tab = len(sorted(d.keys(), key=lambda s: len(s), reverse=True)[0])
    value_col = 'Value'

    if with_color:
        reset = '\033[0m'
        fg_color = '\033[38;5;228m'
    else:
        reset = ''
        fg_color = ''

    print('{var_name: <{tab}}  {value_col}'.format(
        var_name='Name', tab=tab, value_col=value_col))
    print('=' * (tab + len(value_col) + 3 + 15))

    for name, value in env_vars(settings).items():
        schema = value['field']
        field_type = schema.type_
        is_optional = hasattr(field_type, '__origin__') and\
            field_type.__origin__ == Union and\
            isinstance(None, field_type.__args__[1])

        print(f'{fg_color}{name: <{tab}}{reset}  {value["current"]}')

        if schema.default is not Ellipsis:
            print(f' > Default: {schema.default}')
        elif is_optional:
            print(' > Default: None')

        print('')


def vars_to_markdown():
    json = settings.schema()

    lines = []

    def row(values):
        lines.append('| ' + ' | '.join(values) + ' |')

    for _, defn in json['definitions'].items():
        lines.append('## ' + defn['title'])
        lines.append(defn['description'] + '\n')

        row(['Name', 'Description', 'Default'])
        row(['----']*3)

        for _, prop in defn['properties'].items():
            if prop.get('hidden') is True:
                continue

            var_name = list(prop['env_names'])[0].upper()

            if prop.get('note') is not None:
                var_name = f'{var_name} <sup>({prop.get("note")})</sup>'

            row([
                var_name,
                str(prop.get('description', '')),
                str(prop.get('default', ''))
            ])

        lines.append('')

    print('\n'.join(lines))


if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        print("\n"
              "Show global variables used by the application, with their"
              "default values and current values.\n"
              "\n"
              "Options:\n"
              "\t-h, --help\tThis help.\n"
              "\t--markdown\tPrint in markdown format.\n"
              "\t--no-color\tPrint without using ansi colors.\n"
              )
        sys.exit(0)

    if '--markdown' in sys.argv:
        print('# ENV Variables\n')
        vars_to_markdown()
    else:
        vars_to_stdout('--no-color' not in sys.argv)
