
cd ../reseek_log
grep lapsed \
	fast.21.log \
	fast._new.log \
	fast._newdb.log \
	sensitive.21.log \
	sensitive._new.log \
	sensitive._newdb.log \
	verysensitive.21.log \
	verysensitive._newdb.log \
	| sed "-es/:Elapsed time/ /" \
	| columns.py

echo

cd ../analysis
grep SEPQ \
	reseek21_fast.sf2.txt \
	reseek_new_fast.sf2.txt \
	reseek_newdb_fast.sf2.txt \
	| sed "-es/reseek//" \
	| sed "-es/_new/new/" \
	| sed "-es/\.txt//" \
	| sed "-es/ /\t/g" \
	| tr ':' '\t' \
	| columns.py
echo

grep SEPQ \
	reseek21_sensitive.sf2.txt \
	reseek_new_sensitive.sf2.txt \
	reseek_newdb_sensitive.sf2.txt \
	| sed "-es/reseek//" \
	| sed "-es/_new/new/" \
	| sed "-es/\.txt//" \
	| sed "-es/ /\t/g" \
	| tr ':' '\t' \
	| columns.py
echo

grep SEPQ \
	reseek21_verysensitive.sf2.txt \
	reseek_new_verysensitive.sf2.txt \
	reseek_newdb_verysensitive.sf2.txt \
	| sed "-es/reseek//" \
	| sed "-es/_new/new/" \
	| sed "-es/\.txt//" \
	| sed "-es/ /\t/g" \
	| tr ':' '\t' \
	| columns.py
echo
