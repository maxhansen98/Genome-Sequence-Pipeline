#!/bin/bash

# Überprüfen, ob das richtige Format verwendet wurde
if [ $# -ne 2 ]; then
    echo "Usage: $0 fasta_file feature_table"
    exit 1
fi

# FASTA-Datei und Feature-Tabelle als Argumente übergeben
fasta_file="$1"
feature_table="$2"

# Überprüfen, ob die FASTA-Datei existiert
if [ ! -f "$fasta_file" ]; then
    echo "FASTA file $fasta_file not found"
    exit 1
fi

# Überprüfen, ob die Feature-Tabelle existiert
if [ ! -f "$feature_table" ]; then
    echo "Feature table file $feature_table not found"
    exit 1
fi

# Ausführen der Python-Skripte und Drucken der Aminosäuresequenzen auf dem Terminal
python3 genome2orf.py --organism "$fasta_file" --features "$feature_table" |
python3 dna2mrna.py |
python3 mrna2aa.py |
awk '/^>/ {printf "%s%s\n",(NR==1)?"":"\n",$0;next} {printf "%s",$0} END {print ""}'