#! /usr/bin/env python2

import sys
import argparse
from decimal import Decimal, ROUND_UP
from dimana import Units


COMMIT = Units('COMMIT')
SEC = Units('SEC')
MIN = Units('MIN')
HOUR = Units('HOUR')
DAY = Units('DAY')
YEAR = Units('YEAR')
BRANCH = Units('BRANCH')


# Invariants:
# This ignores leap-days/seconds:
SEC_PER_YEAR = (
    (SEC('60') / MIN.one)
    * (MIN('60') / HOUR.one)
    * (HOUR('24') / DAY.one)
    * (DAY('365') / YEAR.one)
    )

# Variable Defaults:
DEFAULT_MAX_COMMITMENTS_PER_SEC = COMMIT('10000') / SEC.one
# This is chosen to be 25% over bitcoin's estimate of Visa's daily peak
# rate as of ~2015
# ref: https://en.bitcoin.it/wiki/Scalability#Scalability_targets

DEFAULT_MAX_LIFETIME_YEAR = YEAR('200')
DEFAULT_BRANCH_FACTOR = BRANCH('2')


# The output result:
REPORT_TMPL = '''\
=== zcash-scale-calc ===

Max commitment rate: {commitments_per_sec}
Network lifetime: {lifetime_year}

Total commits over network lifetime: {total_commits}
log_{branch_factor} of total commits: {log_total_commits}
Minimal Merkle Tree height: {min_merkle_tree_height}
'''


def main(args=sys.argv[1:]):
    """
    zcash capacity calculations.
    """
    opts = parse_args(args)

    total_commits = (
        opts.MAX_COMMITMENTS_PER_SEC *
        opts.LIFETIME_YEAR *
        SEC_PER_YEAR
    )

    log_tc = total_commits.amount.ln() / opts.BRANCH_FACTOR.amount.ln()
    log_tc_ceil = log_tc.quantize(Decimal('1'), rounding=ROUND_UP)

    print REPORT_TMPL.format(
        commitments_per_sec=opts.MAX_COMMITMENTS_PER_SEC,
        lifetime_year=opts.LIFETIME_YEAR,
        total_commits=total_commits,
        branch_factor=opts.BRANCH_FACTOR,
        log_total_commits=log_tc,
        min_merkle_tree_height=log_tc_ceil,
    )


def parse_args(args):
    p = argparse.ArgumentParser(description=main.__doc__)

    def add_argument(*args, **kw):
        if 'default' in kw and 'help' in kw:
            defval = kw['default']
            kw['help'] += ' Default: {}'.format(defval)

        p.add_argument(*args, **kw)

    add_argument(
        '--output-rate',
        dest='MAX_COMMITMENTS_PER_SEC',
        type=(COMMIT/SEC),
        default=DEFAULT_MAX_COMMITMENTS_PER_SEC,
        help='Network Note Commitment throughput rate in notes/sec.',
    )

    add_argument(
        '--lifetime',
        dest='LIFETIME_YEAR',
        type=YEAR,
        default=DEFAULT_MAX_LIFETIME_YEAR,
        help='Maximum network lifetime in years.',
    )

    add_argument(
        '--branch-factor',
        dest='BRANCH_FACTOR',
        type=BRANCH,
        default=DEFAULT_BRANCH_FACTOR,
        help='Branching factor of Merkle tree.',
    )

    return p.parse_args(args)


if __name__ == '__main__':
    main()
