import argparse
import pstats

parser = argparse.ArgumentParser()
parser.add_argument('path')
parser.add_argument('-n')
args = parser.parse_args()

p = pstats.Stats(args.path)
p.strip_dirs().sort_stats(pstats.SortKey.CUMULATIVE).print_stats(int(args.n))