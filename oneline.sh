#/bin/sh
for i in {1..15}; do
	rootpath=$(cd `dirname $0`; pwd); 
	python $rootpath/oneline.py;
done
