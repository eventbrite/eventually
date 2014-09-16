import ConfigParser
import optparse
import os.path
import subprocess

METRICS_CONFIG_FILENAME = 'eventually.conf'
PATHS_CONFIG_FILENAME = 'paths.conf'


def get_config(base_dir):
    metrics = ConfigParser.SafeConfigParser()
    paths = ConfigParser.SafeConfigParser()
    base_dir = os.path.abspath(base_dir) + os.path.sep
    metrics.read(os.path.join(base_dir, METRICS_CONFIG_FILENAME))
    paths.read(os.path.join(base_dir, PATHS_CONFIG_FILENAME))
    return metrics, paths


def _normalize_path(normalize_me, paths):
    # First, extract the path out of the paths config.
    extracted = paths.get('paths', normalize_me)
    # Then, os.path.expanduser() it.
    return os.path.expanduser(extracted)


def run_metric(program, cwd):
    p = subprocess.Popen(program, cwd=cwd, stdout=subprocess.PIPE, shell=True)
    output, _ = p.communicate()
    output = output or ''
    return output.strip()


def create_option_parser(metrics):
    parser = optparse.OptionParser()
    parser.add_option('--list', help='List known metrics, then exit.',
                      action='store_true')
    parser.add_option(
        '-d',
        '--dir',
        help='Directory from which to read configuration [default: %default]',
        type='string',
        default='./')
    for section_title in metrics.sections():
        parser.add_option('--' + section_title,
                          help='Just run %s' % (section_title,),
                          action='store_true',
                          default=None)
    return parser


def run_all_metrics(cli_options, metrics, paths):
    # Find out if the user asked to run a particular one
    run_just_these = []
    for section_title in metrics.sections():
        if cli_options.get(section_title):
            run_just_these.append(section_title)

    # Either run the specific ones we were asked about, or else run
    # all of them.
    if run_just_these:
        run_these = run_just_these
    else:
        run_these = metrics.sections()

    # Then run them
    for section_title in run_these:
        program = metrics.get(section_title, 'program')
        cwd = _normalize_path(
            metrics.get(section_title, 'cwd'), paths)
        value = run_metric(program, cwd)
        # If the section has targets, print that too.
        if (metrics.has_option(section_title, 'target_value') and
            metrics.has_option(section_title, 'target_date') and
            metrics.has_option(section_title, 'start_date') and
            metrics.has_option(section_title, 'start_value')):
            print section_title + ':', value,  '(was:', metrics.get(
                section_title, 'start_value'), 'on', metrics.get(
                section_title, 'start_date') + ')'
            print section_title, '(target_value):', metrics.get(
                    section_title, 'target_value')
            print section_title, '(target_date):', metrics.get(
                section_title, 'target_date')
        else:
            print section_title + ':', value


def list_metrics(metrics):
    for section_title in metrics.sections():
        print section_title


def main():
    # Do the required setup.
    metrics, paths = get_config(base_dir='.')

    parser = create_option_parser(metrics)

    # If the user passed '-h', parser.parse_args()
    # will take care of printing help.
    opts, args = parser.parse_args()

    # Re-do configuration getting, now that we have a base
    # directory.
    metrics, paths = get_config(vars(parser.values)['dir'])

    if opts.list:
        return list_metrics(metrics)

    run_all_metrics(vars(parser.values), metrics, paths)


if __name__ == '__main__':
    main()
