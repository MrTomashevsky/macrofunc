#!/bin/bash

# $1 - filename
# $2 - macroname

# trap 'echo "# $BASH_COMMAND";read' DEBUG

printf "%s%s%s\n" \" $1 \"
cat $1

n=${1%.*}
r=${1##*.}

tmp_file_name=${n}____tmp.${r}
file_name=${n}____cpp_get.${r}

touch ${tmp_file_name}
touch ${file_name}

sleep 1.25

cp $1 ${tmp_file_name}
echo "#ifdef "$2"
1
#else
0
#endif" >> ${tmp_file_name}

cat $1


cpp -o ${file_name} ${tmp_file_name} > /dev/null 2>&1
# printer
tail -n 1 ${file_name}

rm ${tmp_file_name}
rm ${file_name}
