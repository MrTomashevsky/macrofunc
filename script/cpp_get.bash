#!/bin/bash

# $1 - filename
# $2 - macroname

n=${1%.*}
r=${1##*.}

tmp_file_name=${n}____tmp.${r}
file_name=${n}____cpp_get.${r}
cp $1 ${tmp_file_name}
echo -e "\n\n"$2 >> ${tmp_file_name}
cpp -o ${file_name} ${tmp_file_name}
rm ${tmp_file_name}
tail -n $# ${file_name}
rm ${file_name}
#
