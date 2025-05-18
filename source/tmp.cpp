##macrofunc inter(ROW)

##varexpr(LEN, __SIZE_LIST__(ROW))
const int iota##LEN  [LEN] = {
##foreach(VAR, ROW)
    VAR,
##endforeach
};
##endmacrofunc

// ##integrate inter(10 324)


##macrofunc ma(COUNT)
#define HELLO \
##if COUNT == 1
true
##elif COUNT ==2
##else
false
##endif
##if COUNT == 1
true
##elif COUNT ==2
##else
false
##endif
##endmacrofunc

##integrate ma(1)

##integrate ma(2)