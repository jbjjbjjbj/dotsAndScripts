for file in *.cbr; do
    mv "$file" "`basename "$file" .cbr`.pdf"
done

