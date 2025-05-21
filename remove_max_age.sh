for file in configs/*.json; do
    jq 'del(.ga.max_age)' $file > $file
done