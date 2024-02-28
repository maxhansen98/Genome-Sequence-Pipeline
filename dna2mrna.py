#!/usr/bin/python3
import argparse
import sys

# *
# Wenn Zeit, TO-DOS
# fasta & sys je in Funktion schreiben, gleichen Code draußen lassen und ggf. print locus Tag anpassen

DNA2MRNA = {
    'C': 'C',
    'G': 'G',
    'A': 'A',
    'T': 'U'
}


def translate_dna_to_mrna(dna_sequence: str):
    sequence = ''
    for i in range(0, len(dna_sequence)):
        dna_base = dna_sequence[i]
        if dna_base in DNA2MRNA:
            mrna_base = DNA2MRNA[dna_base]
        else:
            mrna_base = 'X'
        sequence += mrna_base
    return sequence


def main():
    parser = argparse.ArgumentParser(description='Translate mRNA seq to amino acid seq')
    parser.add_argument('--fasta', type=str, help='Input FASTA file')
    args = parser.parse_args()

    # Get FASTA-file ready or import the sys-Input (in this case, on the Abgabeserver the fasta-flag is '-')
    if args.fasta and args.fasta != '-':
        with open(args.fasta, 'r') as fasta_file:
            lines = fasta_file.readlines()
            for line in lines:
                if line.startswith(">"):
                    locus_tag = line.strip().lstrip(">")
                    print(f">{locus_tag}")
                else:
                    dna_sequence = line.strip()
                    sequence = translate_dna_to_mrna(dna_sequence)
                    print(sequence)
    else:
        fasta_content = sys.stdin.read().splitlines()
        sequence = ''
        locus_tag = ''
        for line in fasta_content:
            if line.startswith('>'):
                if sequence != '':
                    # Translation and output for each new sequence
                    mrna_sequence = translate_dna_to_mrna(sequence)
                    print(f'>{locus_tag}')
                    print(mrna_sequence)
                    sequence = ''
                locus_tag = line.strip().lstrip('>')
            else:
                sequence += line.strip()
        mrna_sequence = translate_dna_to_mrna(sequence)
        print(f'>{locus_tag}')
        print(mrna_sequence)


if __name__ == '__main__':
    main()
