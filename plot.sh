#!/bin/bash

INPUT=${1:-out}
TRAINING_DIR="training_runs"

# Collect list of input files
if [ "$INPUT" == "all" ]; then
    echo "Plotting all files in $TRAINING_DIR..."
    files=$(find "$TRAINING_DIR" -type f -regex '.*/[0-9][^/]*$' | sort -n)
else
    files="$INPUT"
fi

# Get all unique metrics across all files
metrics=$(cat $files | grep -oP '^\w+(?=:)' | sort -u)

for metric in $metrics; do
    echo "Processing $metric..."

    if [ "$metric" == "SPS" ]; then
        gnuplot -persist <<EOF
set terminal svg size 3840,2160 font 'Verdana,24' background rgb "white"
set output "${metric}.svg"
set title "${metric} over Steps"
set xlabel "Step"
set ylabel "${metric}"
plot $(for f in $files; do
    echo -n "\"< grep ^SPS: $f | awk '{print NR, \$2}'\" with lines linewidth 3 title \"$f\", "
done | sed 's/, $//')
EOF
    else
        # Check if any file has data for this metric
        has_data=false
        for f in $files; do
            if grep -q "^$metric" "$f"; then
                has_data=true
                break
            fi
        done

        if [ "$has_data" = false ]; then
            echo "Skipping $metric (no data)"
            continue
        fi

        gnuplot -persist <<EOF
set terminal svg size 3840,2160 font 'Verdana,24' background rgb "white"
set output "${metric}.svg"
set title "${metric} over Steps"
set xlabel "Step"
set ylabel "${metric}"
plot $(for f in $files; do
    echo -n "\"< grep ^$metric $f | awk '{print \$3, \$2}'\" with lines linewidth 3 title \"$f\", "
done | sed 's/, $//')
EOF
    fi
done

