#!/bin/bash
# Gruppe 3

# Überprüfen, ob das richtige Format verwendet wurde
if [ $# -ne 1 ]; then
    echo "Usage: $0 directory"
    exit 1
fi

# Verzeichnis, das als Argument übergeben wurde
directory="$1"

# Schleife über alle .genome.fa-Dateien im angegebenen Verzeichnis
for genome_file in "$directory"/*.genome.fa; do
    # Überprüfen, ob .genome.fa-Datei existiert
    if [ ! -f "$genome_file" ]; then
        echo "No genome files found in $directory"
        exit 1
    fi

    # Extrahieren des Basiskerns der Datei
    base_name=$(basename "$genome_file" .genome.fa)

    # Überprüfen, ob die entsprechende .featuretable.tsv-Datei vorhanden ist
    feature_table="$directory/$base_name.featuretable.tsv"
    if [ ! -f "$feature_table" ]; then
        echo "Feature table file $feature_table not found"
        exit 1
    fi

    # Ausführen der Python-Skripte und Speichern der Ausgabe in temporären Dateien
    temp_dna_file=$(mktemp)
    temp_rna_file=$(mktemp)
    temp_aa_file=$(mktemp)

    python3 genome2orf.py --organism "$genome_file" --features "$feature_table" > "$temp_dna_file"
    python3 dna2mrna.py < "$temp_dna_file" > "$temp_rna_file"
    python3 mrna2aa.py < "$temp_rna_file" > "$temp_aa_file"

    # Speichern der Ausgabe
    mv "$temp_dna_file" "$directory/dnaSequence_$base_name.fasta"
    mv "$temp_rna_file" "$directory/rnaSequence_$base_name.fasta"
    mv "$temp_aa_file" "$directory/aaSequence_$base_name.fasta"

    echo "$base_name: DNA, RNA and AA-Files saved"
done