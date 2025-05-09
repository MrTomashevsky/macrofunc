/*##macrofunc tmp() 
    ##var(tmp, 0)
#define MACRO1 tmp
    ##var(tmp, tmp + 3) 
#define MACRO2 tmp
    ##var(tmp, tmp + MACRO2)
#define MACRO3 tmp 

    ##var(cstr, #tmp)
#define MACRO4 cstr
    ##var(cstr, L ## #tmp)
#define MACRO5 cstr

##endmacrofunc
// ...
##integrate tmp()

*/

#include <algorithm>

/*
#define MACRO1 0
#define MACRO2 3
#define MACRO3 6
#define MACRO4 "6"
#define MACRO5 L"6"
*/
/*
##macrofunc creater(macro_name)
    ##if macro_name == IO_MACRO
#define MACRO 0
    ##elif macro_name == RAND_MACRO
#define MACRO 1
    ##elif macro_name == 100
#define MACRO 2
    ##else
#define MACRO 3
    ##endif
##endmacrofunc
//...
#define RAND_MACRO 100
##integrate creater(RAND_MACRO)
// #define MACRO 1


##macrofunc int_is_4_bytes(sizeof)
    ##error sizeof == 4
##endmacrofunc
// ...
##integrate int_is_4_bytes(sizeof(int)) 
/*
#if sizeof(int) == 4
#error "sizeof(int) == 4"
#endif
*/

/*
##macrofunc create_functions(count)
int global[count];

    ##for(VAR, 0, count, 1)
void function ## VAR (void) { global[VAR]++; }
    ##endfor

void (*global_functions[count])(void) = {

    ##for(VAR, 0, count, 1)
    function ## VAR
        ##if VAR != count - 1
    ,
        ##endif
    ##endfor

};
##endmacrofunc
// ...
##integrate create_functions(3)
/*
int global[3];
void function0(void) { global[0]++; }
void function1(void) { global[1]++; }
void function2(void) { global[2]++; }
void (*global_functions[count])(void) = {
function0,
function1,
function2
};
*/


/*
##macrofunc create_functions(row_of_names)
    ##foreach(VAR, row_of_names)
void function ## VAR (void) { std::cout << VAR << std::endl; }
    ##endforeach

void (*global_functions[__SIZE_LIST__])(void) = {
    ##foreach(VAR, row_of_names)
    function ## VAR
        ##if ! __IS_END_LIST__(row_of_names, VAR)
    ,
        ##endif
    ##endforeach

};
##endmacrofunc
// ...
#define ROW 0 1 2
##integrate create_functions(ROW)
/*
void function0(void) { std::cout << 0 << std::endl; }
void function1(void) { std::cout << 1 << std::endl; }
void function2(void) { std::cout << 2 << std::endl; }
void (*global_functions[3])(void) = {
function0,
function1,
function2
};
*/

/*
##macrofunc is_macro(list)
    ##foreach(VAR, list)
        ##if ! __IS_MACRO__(VAR)
#error "is not macro: " #VAR
        ##endif
    ##endforeach
##endmacrofunc
// ...
#define ROW EOF NULL stdout 400
##integrate is_macro(list)
/*
#error "is not macro: 400"
*/




##macrofunc hello_world()


    ##macrofunc __tmp(text, txt)
        ##error text
        ##error txt
    ##endmacrofunc

    ##integrate __tmp(hello, ff)

##endmacrofunc

##integrate hello_world()

##macrofunc variables(v)
    ##error v
##endmacrofunc

##integrate variables(df)
