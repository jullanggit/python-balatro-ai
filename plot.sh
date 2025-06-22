#!/bin/bash

INPUT=${1:-out}
metrics=$(grep -oP '^\w+(?=:)' "$INPUT" | sort -u)

for metric in $metrics; do
    echo "Processing $metric..."

    if [ "$metric" == "SPS" ]; then
        # Count occurrences to use as x-axis (assuming 1:1 per line)
        gnuplot -persist <<EOF
set terminal pngcairo size 800,400
set output "${metric}.png"
set title "${metric} over Steps"
set xlabel "Update"
set ylabel "${metric}"
plot "< grep '^SPS:' '$INPUT' | awk '{print NR, \$2}'" with linespoints title "${metric}"
EOF
    else
        # Skip empty data
        data=$(grep "^$metric" "$INPUT" | awk '{if (NF >= 3) print $3, $2}')
        if [ -z "$data" ]; then
            echo "Skipping $metric (no data)"
            continue
        fi

        # Normal case with <step> <value>
        gnuplot -persist <<EOF
set terminal pngcairo size 800,400
set output "${metric}.png"
set title "${metric} over Steps"
set xlabel "Step"
set ylabel "${metric}"
plot "< grep '^$metric' '$INPUT' | awk '{print \$3, \$2}'" with linespoints title "${metric}"
EOF
    fi
done

