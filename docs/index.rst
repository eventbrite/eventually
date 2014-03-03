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
 my_metric

To actually find the current value of those metrics::

 $ python run_metrics.py
 my_metric: 31779

This list comes from the `metrics.cfg` file. Each configuration section
specifies the name of a metric, and has the following required fields:

* `program`: The full shell command to execute.
* `cwd`: The path from which the command should be run.

The `program` should output a single number.

The `cwd` refers to a path, configured in `paths.cfg`, which is
expanded by os.path.expanduser().

The `metrics.cfg` configuration for this metric would be::

 [my_metric]
 program = git ls-files -z -- '*.php' | xargs -0 wc -l | tail -n1 | awk '{print $1}'
 cwd = EVENTBRITECORE

and the `paths.cfg` configuration would be::

 [paths]
 EVENTBRITECORE = ~/work/eventbritecore


Setting goals
=============

To set a quantitative code quality goal, you need these things:

* An idea for a *measurable attribute of the code*, and a command you
  can use to measure it. For example: the idea might be, "Have less
  old-style database handling code," and the way to measure it will
  be to use `git ls-files` to list the files in a particular directory,
  and `wc -l` to count the number of lines in them.

* A *current value* of that metric. You need this so you can measure
  progress.

* A *target value* of that metric. This is what you commit to getting to.

* A *target date* of that metric. This is when you will achieve the
  target date.

To use this tool to help you, put your measureable attribute and command in
`metrics.cfg` as described in the previous section.

Once you have added the metric, use the following process to enable goal tracking.

Calculate the start_value
-------------------------

If your metric is called `my_metric`, and you have already configured
it in `metrics.cfg`, then run this command to calculate just the value
of that metric::

 $ python run_metrics.py --my_metric

You will see a message like::

 my_metric: 31779

Add that to `metrics.cfg` as `start_value` within your `[my_metric]`
section.

Also add a `start_date`, which should be today's date in ISO date format,
for example, `2014-01-27`.

Set a target value and date
---------------------------

Now we'll set the goal. Simply edit the `metrics.cfg` file to add these
keys to your `[my_metric]` section:

* `target_value`: integer, e.g. 12003;

* `target_date`: ISO format date of when you want to reach that value.

Check your progress
-------------------

Now whenever you run the tool, when it prints the value of that metric, it
will also print the target value. For example::

 $ python run_metrics.py --my_metric
 my_metric: 31779
 my_metric (target_value): 20000
 my_metric (target_date): 2014-03-31

Handling success
----------------

Once you reach success on a goal, we recommend:

* Emailing your teammates with the output of the tool, and then

* Deleting the metric from your metrics.cfg file, since you no longer need it.


Known deficiencies
==================

Here are the things this tool does not do yet:

* Store the results over time. For example, if you and the team
  want to remove 2000 lines of code in the next 3 months, it could
  be motivating to see a graph of how this has progressed. However,
  this does not do that.

* Let you check just subsets of the code. This could be useful for a
  version of the tool that integrates with developers' workflow, so
  that if some of the checks are expensive, they can be run on just
  the files that a developer has modified.

* Let you identify which people need to make the changes that the tool
  suggests. One way to do this will be via `git blame -w`, if the
  metrics can be provided on a line-by-line basis.

* Let you identify which groups within the team are responsible for
  making sure the changes happen. It can be nice to move up the
  management hierarchy so that we can say, "Bob's engineering
  department needs to stop adding new code that uses old-style
  database calls," rather than just "These particular engineers in
  Bob's team need to fix things."

* Silencing warnings. This (for now) is best-handled by the scripts
  that we call-out to.
