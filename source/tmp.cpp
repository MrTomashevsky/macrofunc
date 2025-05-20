

##macrofunc function_change_global_value_g(COUNT)

    ##for(COUNTER, 0, COUNT, 1)
    void __function_change_global_value_g##COUNTER##__() { g[COUNTER]++; }
    ##endfor


    void (*__function_change_global_value_g_array_[COUNT])(void) = {
    ##for(COUNTER, 0, COUNT, 1)
        __function_change_global_value_g ## COUNTER ## __ 
        ##if COUNTER != COUNT - 1
            ,
        ##endif
    ##endfor
    };


##endmacrofunc

#define HAHA 5

##integrate function_change_global_value_g(HAHA)
