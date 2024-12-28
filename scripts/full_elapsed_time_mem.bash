grep lapsed \
  ../foldseek_search_full/*time* \
  ../reseek_search_full/*time* \
  | sed "-es/(.*)://" \
  | columns.py

echo

grep "Maximum resident" \
  ../foldseek_search_full/*time* \
  ../reseek_search_full/*time* \
  | sed "-es/(.*)://" \
  | columns.py
