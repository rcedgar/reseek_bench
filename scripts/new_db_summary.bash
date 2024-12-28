
cd ../reseek_log
grep lapsed \
	fast.21.log \
	fast._new_db.log \
	sensitive.21.log \
	sensitive._new_db.log \
	| sed "-es/:Elapsed time/ /" \
	| columns.py

echo

cd ../analysis
grep SEPQ \
	reseek21_fast.sf2.txt \
	reseek_new_db_fast.sf2.txt \
	reseek21_sensitive.sf2.txt \
	reseek_new_db_sensitive.sf2.txt \
	| sed "-es/reseek//" \
	| sed "-es/_new_db/new_db/" \
	| sed "-es/\.txt//" \
	| sed "-es/ /\t/g" \
	| tr ':' '\t' \
	| columns.py
