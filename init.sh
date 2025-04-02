array=$(pwd)
echo $(pwd)

prevpath=text_files/prevpath.txt

if [ ! -f ${prevpath} ]; then
    echo "${prevpath} new"
    echo $PATH > $prevpath
fi

#PATH=$PATH:"${array[*]}/proj"
PATH=$PATH:/home/tomatik/project/kurs_proj/proj
export $PATH

#export $PATH

