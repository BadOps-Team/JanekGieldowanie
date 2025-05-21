for file in configs/*.json; do
    jq 'del(.ga.max_age)' $file > tmpfile && mv tmpfile $file
done
