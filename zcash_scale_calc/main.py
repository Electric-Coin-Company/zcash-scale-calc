#! /usr/bin/env python2

import sys
import argparse
from decimal import Decimal, ROUND_UP
from dimana import Dimana


# dimana units types:
class Units (object):
    def __init__(self):
        units = [
            'COMMIT',
            'POUR',
            'SEC',
            'MIN',
            'HOUR',
            'DAY',
            'YEAR',
        ]

        for unit in units:
            setattr(self, unit, Dimana.get_dimension(unit))

U = Units()

# Invariants:
# This ignores leap-days/seconds:
SEC_PER_YEAR = (
    (U.SEC('60') / U.MIN.one)
    * (U.MIN('60') / U.HOUR.one)
    * (U.HOUR('24') / U.DAY.one)
    * (U.DAY('365') / U.YEAR.one)
    )

# Variable Defaults:
DEFAULT_MAX_POUR_PER_SEC = U.POUR('5000') / U.SEC.one
# This is chosen to be 25% over bitcoin's estimate of Visa's daily peak
# rate as of ~2015
# ref: https://en.bitcoin.it/wiki/Scalability#Scalability_targets

DEFAULT_MAX_LIFETIME_YEAR = U.YEAR('200')

DEFAULT_COMMIT_PER_POUR = U.COMMIT('2') / U.POUR.one


# The output result:
REPORT_TMPL = '''\
=== zcash-scale-calc ===

Commits per pour: {commit_per_pour}
Max pour rate: {pour_per_sec}
Network lifetime: {lifetime_year}

Total commits over network lifetime: {total_commits}
log_2 of total commits: {log2_total_commits}
Minimal Merkle Tree height: {min_merkle_tree_height}
'''


def main(args = sys.argv[1:]):
    """
    zcash scale calculations.
    """
    opts = parse_args(args)

    total_commits = (
        opts.COMMIT_PER_POUR *
        opts.MAX_POUR_PER_SEC *
        opts.LIFETIME_YEAR *
        SEC_PER_YEAR
    )

    log2_tc = total_commits.value.ln() / Decimal('2').ln()
    log2_tc_ceil = log2_tc.quantize(Decimal('1'), rounding=ROUND_UP)

    print REPORT_TMPL.format(
        commit_per_pour = opts.COMMIT_PER_POUR,
        pour_per_sec = opts.MAX_POUR_PER_SEC,
        lifetime_year = opts.LIFETIME_YEAR,
        total_commits = total_commits,
        log2_total_commits = log2_tc,
        min_merkle_tree_height = log2_tc_ceil,
    )


def parse_args(args):
    p = argparse.ArgumentParser(description=main.__doc__)

    def add_argument(*args, **kw):
        if 'default' in kw and 'help' in kw:
            defval = kw['default']
            kw['help'] += ' Default: {!r}'.format(defval)

        p.add_argument(*args, **kw)

    # This should be dimana functionality:
    def make_unit_parser(unitone):
        def parse(arg):
            return Dimana(arg) * unitone
        parse.__doc__ = 'A {} value.'.format(unitone.dimstr)

        return parse

    add_argument(
        '--pour-rate',
        dest='MAX_POUR_PER_SEC',
        type=make_unit_parser(U.POUR.one/U.SEC.one),
        default=DEFAULT_MAX_POUR_PER_SEC,
        help='Network Pour throughput rate in pours/sec.',
    )

    add_argument(
        '--commits-per-pour',
        dest='COMMIT_PER_POUR',
        type=make_unit_parser(U.COMMIT.one/U.POUR.one),
        default=DEFAULT_COMMIT_PER_POUR,
        help='Commits tracked per pour.',
    )

    add_argument(
        '--lifetime',
        dest='LIFETIME_YEAR',
        default=DEFAULT_MAX_LIFETIME_YEAR,
        help='Maximum network lifetime in years.',
    )

    return p.parse_args(args)


if __name__ == '__main__':
    main()
