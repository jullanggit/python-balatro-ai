#!/bin/bash

INPUT=${1:-out}  # default to 'out' if no argument given

# Get all metric names (lines starting with a word and a colon)
metrics=$(grep -oP '^\w+(?=:)' "$INPUT" | sort -u)

for metric in $metrics; do
    # Create a temp data file for gnuplot: "<step> <value>"
    grep "^$metric" "$INPUT" | awk '{print $3, $2}' > "$metric.dat"

    # Skip if data is empty
    if [ ! -s "$metric.dat" ]; then
        echo "No data for $metric, skipping..."
        continue
    fi

    # Generate PNG plot using gnuplot
    gnuplot <<EOF
set terminal pngcairo size 800,400
set output "${metric}.png"
set title "${metric} over Steps"
set xlabel "Step"
set ylabel "${metric}"
set datafile separator whitespace
plot "${metric}.dat" with linespoints title "${metric}"
EOF

    echo "Saved plot: ${metric}.png"
done
