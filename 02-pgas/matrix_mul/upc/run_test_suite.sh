/usr/local/upcxx/bin/upcxx -O matrixmul.cpp -o matrixmul


for locales in {1..8}
do
	for size in 1000 1500 2000
	do
		echo "seed: 1234  size: $size locales: $locales"
		/usr/local/upcxx/bin/upcxx-run -n $locales -N 1 matrixmul 1234 $size
	done
	echo ""	
done

