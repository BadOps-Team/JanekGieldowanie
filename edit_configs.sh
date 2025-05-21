for file in configs/config1_0.json; do
    jq $1 $file > tmpfile && mv tmpfile $file
done
