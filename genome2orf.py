#!/usr/bin/python3
import argparse
MATCHING_BASES = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}


def fasta_reader(fasta_file):
    seqs = {}
    current_header = ''
    current_seq = ''
    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_header:  # Skip the first line (current_header still empty)
                    seqs[current_header] = current_seq
                current_header = line.split(maxsplit=1)[0].lstrip('>')  # Split at the first space and remove '>'
                current_seq = ''
                print(current_header)
            else:
                current_seq += line
        if current_header:  # Last call before returning
            seqs[current_header] = current_seq
    return seqs


def extract_orfs(genome_file, feature_table):
    genome_sequences = fasta_reader(genome_file)
    orfs = []

    with open(feature_table, 'r') as f:
        for line in f:
            columns = line.strip().split('\t')
            if columns[0] == 'CDS':
                locus_tag = columns[16]
                start = int(columns[7]) - 1
                end = int(columns[8])
                strand = columns[9]
                seq_name = columns[6]

                if seq_name in genome_sequences:
                    seq = genome_sequences[seq_name][start:end]
                    if strand == '-':
                        seq = rev_complement(seq)

                    # Append ORFs while keeping the correct order
                    orfs.append((locus_tag, seq))
    return orfs


def rev_complement(seq):
    reversed_seq = reversed(seq)
    complement = ''
    for base in reversed_seq:
        if base in MATCHING_BASES:
            complement += MATCHING_BASES[base]
        else:
            complement += base
    return complement


def main():
    parser = argparse.ArgumentParser(description='Extract ORFs from genome sequence and convert to mRNA')
    parser.add_argument('--organism', type=str, help='Genome sequence file')
    parser.add_argument('--features', type=str, help='Feature table file')
    args = parser.parse_args()

    orfs = extract_orfs(args.organism, args.features)
    for locus_tag, seq in orfs:
        print(f">{locus_tag}")
        print(seq)


if __name__ == "__main__":
    main()
