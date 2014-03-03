import ConfigParser
import optparse
import os.path
import subprocess

METRICS_CONFIG_FILENAME = 'metrics.cfg'
PATHS_CONFIG_FILENAME = 'paths.cfg'


def get_config():
    metrics = ConfigParser.SafeConfigParser()
    paths = ConfigParser.SafeConfigParser()
    # FIXME: Use smart path to these files, not just
    # hoping that CWD is the right answer.
    metrics.read(METRICS_CONFIG_FILENAME)
    paths.read(PATHS_CONFIG_FILENAME)
    return metrics, paths


def _normalize_path(normalize_me, paths):
    # First, extract the path out of the paths config.
    extracted = paths.get('paths', normalize_me)
    # Then, os.path.expanduser() it.
    return os.path.expanduser(extracted)


def run_metric(program, cwd):
    return subprocess.check_output(
        program,
        cwd=cwd,
        shell=True).strip()


def create_option_parser(metrics):
    parser = optparse.OptionParser()
    parser.add_option('--list', help='List known metrics, then exit.',
                      action='store_true')
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
    metrics, paths = get_config()

    parser = create_option_parser(metrics)

    # If the user passed '-h', parser.parse_args()
    # will take care of printing help.
    opts, args = parser.parse_args()

    if opts.list:
        return list_metrics(metrics)

    run_all_metrics(vars(parser.values), metrics, paths)


if __name__ == '__main__':
    main()
