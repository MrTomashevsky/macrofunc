##macrofunc tmp() 
    ##varline(tmp, 0)
#define MACRO1 tmp
    ##varexpr(tmp, tmp + 3) 
#define MACRO2 tmp
    ##varexpr(tmp, tmp + MACRO2)
#define MACRO3 tmp 
    ##varline(cstr, #tmp)
#define MACRO4 cstr
    ##varline(cstr, L ## #tmp)
#define MACRO5 cstr

##endmacrofunc
// ...
##integrate tmp()
/*
#define MACRO1 0
#define MACRO2 3  
#define MACRO3 6
#define MACRO4 "6"
#define MACRO5 L"6"
*/


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



##macrofunc create_functions(count)
int global[count];

    ##for(var, 0, count, 1)
void function ## var (void) { global[var]++; }
    ##endfor

void (*global_functions[count])(void) = {

    ##for(var, 0, count, 1)
    function ## var
        ##if var != count - 1
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



##macrofunc create_functions(row_of_names)
    ##foreach(var, row_of_names)
void function ## var (void) { std::cout << var << std::endl; }
    ##endforeach


void (*global_functions[__SIZE_LIST__(row_of_names)])(void) = {
    ##foreach(var, row_of_names)
    function ## var
        ##if ! __IS_END_LIST__(row_of_names, var)
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


##macrofunc is_macro(list)
    ##foreach(var, list)
        ##if ! __IS_MACRO__(row_of_names, var)
#error "is not macro: " #var
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

    ##integrate __tmp("hello", "sdsd")
    ##integrate __tmp("heh),ds", "lsdlsld")
    ##integrate __tmp("!", "lsldsld")

##endmacrofunc

##integrate hello_world()

##macrofunc varlineiables(v, t, h)
    ##error v t h
##endmacrofunc

##integrate varlineiables(8, 9, 7)
