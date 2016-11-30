for f in *.rar
do
	unrar e -ep "$f"
	convert *.jpg "$f.pdf"
	convert *.JPG "$f.pdf"
	rm *.jpg
	rm *.JPG
done
