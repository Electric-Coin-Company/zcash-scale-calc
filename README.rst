==================
 zcash-scale-calc
==================

.. contents::

Punchline
=========

.. code:: bash

   $ zcash-scale-calc --pour-rate 100 --lifetime 500
   === zcash-scale-calc ===

   Commits per pour: 2 [COMMIT / POUR]
   Max pour rate: 100.0 [POUR / SEC]
   Network lifetime: 500 [YEAR]

   Total commits over network lifetime: 3153600000000.0 [COMMIT]
   log_2 of total commits: 41.52013682014238455718778943
   Minimal Merkle Tree height: 42


   $ zcash-scale-calc --pour-rate 5000 --lifetime 200
   === zcash-scale-calc ===

   Commits per pour: 2 [COMMIT / POUR]
   Max pour rate: 5000.0 [POUR / SEC]
   Network lifetime: 200 [YEAR]

   Total commits over network lifetime: 63072000000000.0 [COMMIT]
   log_2 of total commits: 45.84206491502974690505810887
   Minimal Merkle Tree height: 46
Installation
============

.. code:: bash

   $ git clone 'https://github.com/Electric-Coin-Company/zcash-scale-calc'
   $ pip install ./zcash-scale-calc

Usage
=====

.. code:: bash

   $ zcash-scale-calc --help
   usage: zcash-scale-calc [-h] [--pour-rate MAX_POUR_PER_SEC]
                           [--commits-per-pour COMMIT_PER_POUR]
                           [--lifetime LIFETIME_YEAR]

   zcash scale calculations.

   optional arguments:
     -h, --help            show this help message and exit
     --pour-rate MAX_POUR_PER_SEC
                           Network Pour throughput rate in pours/sec. Default:
                           5000 [POUR / SEC]
     --commits-per-pour COMMIT_PER_POUR
                           Commits tracked per pour. Default: 2 [COMMIT / POUR]
     --lifetime LIFETIME_YEAR
                           Maximum network lifetime in years. Default: 200 [YEAR]

