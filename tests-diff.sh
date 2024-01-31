TEST_DIR="/test"

OUTPUT_FILE="my-stats"

# Clear the output file if it already exists
> "$OUTPUT_FILE"

# Loop through each .lir file in the directory
for file in "$TEST_DIR"/*.lir; do

    json_file="${file%.lir}.lir.json" OUTPUT_FILE
    ./run-stats.sh "$file" "$json_file" >> "$OUTPUT_FILE"
    stats_file="${file%.lir}.stats"
    diff -wp "$OUTPUT_FILE" "$stats_file"
    
done