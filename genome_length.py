#!/usr/bin/python3
import argparse
from urllib.request import urlopen
import regex as re


# Herunterladen des Genome Reports von Aufgaben-URL
def download_report():
    # Using requests-library, https://pypi.org/project/requests/
    url = "ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/prokaryotes.txt"
    genome_report = urlopen(url)
    return genome_report.read().decode('utf-8')


def get_genome_info(genome_report, regex_list):
    genome_info = []
    lines = genome_report.split('\n')
    for line in lines:
        if line.startswith('#'):
            continue

        # Organism-Zeile
        columns = line.split("\t")
        organism_name = columns[7]

        # Umwandlung in Mb
        genome_length = float(columns[5]) / 1000000

        for regex in regex_list:
            if re.search(regex, organism_name, re.IGNORECASE):
                genome_info.append((organism_name, genome_length))
                break
    return genome_info


def main():
    genome_report = download_report()

    # Argument-Parsing
    parser = argparse.ArgumentParser(
        description="Search for fully sequenced genomes based on organism names and regex patterns.")
    parser.add_argument("--organism", nargs="+", help="Given Regex patterns", required=True)
    args = parser.parse_args()

    regex_list = args.organism
    genome_info = get_genome_info(genome_report, regex_list)

    for organism, length in genome_info:
        print(f"{organism}\t{length:.3f} Mb")


if __name__ == '__main__':
    main()


