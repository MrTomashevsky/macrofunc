##macrofunc inter(ROW)

##varexpr(LEN, __SIZE_LIST__(ROW))
const int iota##LEN  [LEN] = {
##foreach(VAR, ROW)
    VAR,
##endforeach
};
##endmacrofunc

##integrate inter(10 324)