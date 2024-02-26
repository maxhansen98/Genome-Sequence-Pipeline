#!/usr/bin/python3
import argparse


def extract_orfs(genome_file, feature_table):

    return


def main():
    parser = argparse.ArgumentParser(description='Extract ORFs from genome sequence and convert to mRNA')
    parser.add_argument('--organism', type=str, help='Genome sequence file')
    parser.add_argument('--features', type=str, help='Feature table file')
    args = parser.parse_args()

    extract_orfs(args.organism, args.features)


if __name__ == "__main__":
    main()
