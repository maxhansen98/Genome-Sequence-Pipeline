#!/usr/bin/python3
import argparse
import sys

# *
# Wenn Zeit, TO-DOS
# fasta & sys je in Funktion schreiben, gleichen Code draußen lassen und ggf. print locus Tag anpassen

RNA2DNA = {"UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
           "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
           "UAU": "Y", "UAC": "Y", "UAA": "STOP", "UAG": "STOP",
           "UGU": "C", "UGC": "C", "UGA": "STOP", "UGG": "W",
           "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
           "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
           "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
           "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
           "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
           "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
           "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
           "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
           "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
           "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
           "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
           "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G", }


def translate_mrna_to_aa(mrna_sequence: str):
    sequence = ""
    for i in range(0, len(mrna_sequence), 3):
        codon = mrna_sequence[i:i + 3]
        if codon in RNA2DNA:
            amino_acid = RNA2DNA[codon]
            if amino_acid == "STOP":
                break
            else:
                sequence += amino_acid
        else:
            sequence += "X"  # Error-AA, similar as in some literature (e.g. BLOSUM matrixes)
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
                    mrna_sequence = line.strip()
                    sequence = translate_mrna_to_aa(mrna_sequence)
                    print(sequence)
    else:
        fasta_content = sys.stdin.read().splitlines()
        sequence = ""
        locus_tag = ""
        for line in fasta_content:
            if line.startswith('>'):
                if sequence != '':
                    # Translation and output for each new sequence
                    aa_sequence = translate_mrna_to_aa(sequence)
                    print(f'>{locus_tag}')
                    print(aa_sequence)
                    sequence = ""
                locus_tag = line.strip().lstrip(">")
            else:
                sequence += line.strip()
        aa_sequence = translate_mrna_to_aa(sequence)
        print(f">{locus_tag}")
        print(aa_sequence)


if __name__ == "__main__":
    main()
