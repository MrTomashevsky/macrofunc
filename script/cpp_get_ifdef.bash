#!/bin/bash

# $1 - filename
# $2 - macroname

n=${1%.*}
r=${1##*.}

tmp_file_name=${n}____tmp.${r}
file_name=${n}____cpp_get.${r}
cp $1 ${tmp_file_name}
echo "#ifdef "$2"
1
#else
0
#endif" >> ${tmp_file_name}
cpp -o ${file_name} ${tmp_file_name}
rm ${tmp_file_name}
tail -n 1 ${file_name}
rm ${file_name}
#
