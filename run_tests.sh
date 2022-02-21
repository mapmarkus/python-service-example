# $* passes arguments to this script to pytest it overrides the previous
# arguments set here
#
# Interesting options:
#
#  -k EXPRESSION            Only run tests which match the given substring
#                           expression
#
#  -x, --exitfirst          Exit instantly on first error or failed test.
#  --maxfail=num            Exit after first num failures or errors.#
#  --lf, --last-failed      Rerun only the tests that failed in the last run
#  --ff, --failed-first     Run all tests but run the last failuers first
#  --nf, --new-first        Run tests from new files first, then all the rest
#                           by time
#  --lfnf={all,none}, --last-failed-no-failures={all,none}
#                           Which tests to run with NO previously knonw
#                           failures
#  --sw, --stepwise         Exit on test failure and continue from last failing
#                           test next time
#
#               Reporting
#
#  --duration=N             show N slowest setup/test durations (N=0 for all)
#  -v, --verbose            show more details
#  -vv,                     even more verbose
#  -q, --quite              show less details
#  -r chars                 report using chars instead of colored dots
#  --show-capture={no,stdout,stderr,log,all}
#                           Controls how captured stdout/stderr/log is shown on
#                           failed tests. Default is 'all'
#
#              Collection
#
# --pyargs                  Try to interpret arguments as python packages
#                           (like -s in unittest?)
# --ignore=path
# --ignore-glob=path        Ignore path or glob path
#
#              Warnings
#
# -W PYTHONGWARNINGS        Show python warning (this can be set to "error" to
#                           force test errors if a warning is found)
SERVICE_DB_NAME=test SERVICE_TEST_MODE=True pytest -Wignore -v ${*:-tests}
