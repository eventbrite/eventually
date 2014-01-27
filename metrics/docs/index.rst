.. eb-code-metrics documentation master file, created by
   sphinx-quickstart on Mon Jan 27 12:37:45 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Generating and tracking metrics for code
========================================

This package exists to help us set and measure progress toward code
quality goals. Ideas to get your mind flowing:

* "Let's have 30% less PHP in the repository by April 2014."

* "Let's decrease the amount of non-Django database code by 50% by
  June 2014."


This package attempts to be the simplest thing possible to let you
declare a metric, find the current level of success on that metric,
commit to a specific goal by a specific date, and measure your
progress toward that.

Listing metrics and their current values
----------------------------------------

To give you a sense of how the tool works, we'll see what interacting
with the tool is like if you have already configured one metric.

To list the metrics the tool knows about::

 $ python run_metrics.py --list
 php_line_count

To actually find the current value of those metrics::

 $ python run_metrics.py
 php_line_count: 31779

This list comes from the `metrics.cfg` file. Each configuration section
specifies the name of a metric, and has the following required fields:

* `program`: The full shell command to execute.
* `cwd`: The path from which the command should be run.

The `program` should output a single number.

The `cwd` refers to a path, configured in `paths.cfg`, which is
expanded by os.path.expanduser().

The `metrics.cfg` configuration for this metric would be::

 [php_line_count]
 program = git ls-files -z -- '*.php' | xargs -0 wc -l | tail -n1 | awk '{print $1}'
 cwd = EVENTBRITECORE

and the `paths.cfg` configuration would be::

 [paths]
 EVENTBRITECORE = ~/work/eventbritecore
