#!/usr/bin/env python

""" Benchmark loading an RSA key from a PEM string """

# pylint: disable=wrong-import-position,wrong-import-order
from bench.unitbench import Benchmark
from test.fixtures import rsa_priv_pem, to_bytes_2and3
from bench.reporter import Reporter
from jwcrypto.jwk import JWK

class LoadKeyBenchmark(Benchmark):
    """ Load key benchmark """

    def input(self):
        """ Name of benchmark """
        return ["Load Key"]

    def repeats(self):
        """ Iterations """
        return 10000

    def bench_RSA(self):
        """ Import key """
        JWK.from_pem(to_bytes_2and3(rsa_priv_pem))

if __name__ == "__main__":
    #pylint: disable=W0402
    import string
    string.capwords = lambda x: x
    LoadKeyBenchmark().run(reporter=Reporter())
