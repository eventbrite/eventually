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


def create_option_parser():
    parser = optparse.OptionParser()
    parser.add_option('--list', help='List known metrics, then exit.',
                      action='store_true')
    return parser


def run_all_metrics(metrics, paths):
    for section_title in metrics.sections():
        program = metrics.get(section_title, 'program')
        cwd = _normalize_path(
            metrics.get(section_title, 'cwd'), paths)
        print section_title + ':', run_metric(program, cwd)


def list_metrics(metrics):
    for section_title in metrics.sections():
        print section_title


def main():
    parser = create_option_parser()

    # If the user passed '-h', parser.parse_args()
    # will take care of printing help.
    opts, args = parser.parse_args()

    # Do the required setup.
    metrics, paths = get_config()

    if opts.list:
        return list_metrics(metrics)

    run_all_metrics(metrics, paths)


if __name__ == '__main__':
    main()
