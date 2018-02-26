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
LEVEL = Units('LEVEL')


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
    opts.cmdfunc(opts)


def depth_from_lifetime(opts):
    """Calculate tree depth given target lifetime."""

    total_commits = (
        opts.MAX_COMMITMENTS_PER_SEC *
        opts.LIFETIME_YEAR *
        SEC_PER_YEAR
    )

    print_report(opts, total_commits, opts.LIFETIME_YEAR)


def lifetime_from_depth(opts):
    """Calculate lifetime given tree depth."""

    total_commits = COMMIT(2 ** opts.DEPTH.amount)
    lifetime = total_commits / (opts.MAX_COMMITMENTS_PER_SEC * SEC_PER_YEAR)

    print_report(opts, total_commits, lifetime)


def print_report(opts, total_commits, lifetime):
    log_tc = total_commits.amount.ln() / opts.BRANCH_FACTOR.amount.ln()
    log_tc_ceil = log_tc.quantize(Decimal('1'), rounding=ROUND_UP)

    print REPORT_TMPL.format(
        commitments_per_sec=opts.MAX_COMMITMENTS_PER_SEC,
        lifetime_year=pretty_disp(lifetime),
        total_commits=total_commits,
        branch_factor=opts.BRANCH_FACTOR,
        log_total_commits='{:.2f}'.format(log_tc),
        min_merkle_tree_height=log_tc_ceil,
    )


def parse_args(args):
    def add_argument(parser, *args, **kw):
        if 'default' in kw and 'help' in kw:
            defval = kw['default']
            kw['help'] += ' Default: {}'.format(defval)

        parser.add_argument(*args, **kw)

    p = argparse.ArgumentParser(description=main.__doc__)

    add_argument(
        p,
        '--output-rate',
        dest='MAX_COMMITMENTS_PER_SEC',
        type=(COMMIT/SEC),
        default=DEFAULT_MAX_COMMITMENTS_PER_SEC,
        help='Network Note Commitment throughput rate in notes/sec.',
    )

    add_argument(
        p,
        '--branch-factor',
        dest='BRANCH_FACTOR',
        type=BRANCH,
        default=DEFAULT_BRANCH_FACTOR,
        help='Branching factor of Merkle tree.',
    )

    subp = p.add_subparsers()

    dflp = subp.add_parser(
        'depth-from-lifetime',
        help=depth_from_lifetime.__doc__,
    )
    dflp.set_defaults(cmdfunc=depth_from_lifetime)

    add_argument(
        dflp,
        '--lifetime',
        dest='LIFETIME_YEAR',
        type=YEAR,
        required=True,
        help='Maximum network lifetime in years.',
    )

    lfdp = subp.add_parser(
        'lifetime-from-depth',
        help=lifetime_from_depth.__doc__,
    )
    lfdp.set_defaults(cmdfunc=lifetime_from_depth)

    add_argument(
        lfdp,
        '--depth',
        dest='DEPTH',
        type=LEVEL,
        required=True,
        help='Commitment tree depth.',
    )

    return p.parse_args(args)


def pretty_disp(value, precision=2):
    """A string repr of a value with only precision digits after decimal."""
    return '{:.2f} {}'.format(value.amount, value.units)


if __name__ == '__main__':
    main()
