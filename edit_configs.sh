for file in configs/*.json; do
    jq $1 $file > tmpfile && mv tmpfile $file
    # jq '.estimator_strategy |= if . == "mse" then "lse" else . end' "$file" > tmpfile && mv tmpfile "$file"
done
