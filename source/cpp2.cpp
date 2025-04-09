
// ...
    ##var(tmp, 0)
#define MACRO1 tmp
    ##var(tmp, tmp + 3)
#define MACRO2 tmp
    ##var(tmp, tmp + MACRO2)
#define MACRO3 tmp
    ##var(cstr, #MACRO3)
#define MACRO4 cstr
    ##var(cstr, L ## #MACRO3)
#define MACRO5 cstr
##integrate tmp()
/*
#define MACRO1 0
#define MACRO2 3
#define MACRO3 6
#define MACRO4 "6"
#define MACRO5 L"6"
*/


//...
#define RAND_MACRO 100
    ##if macro_name == IO_MACRO
#define MACRO 0
    ##elif macro_name == RAND_MACRO
#define MACRO 1
    ##elif macro_name == 100
#define MACRO 2
    ##else
#define MACRO 3
    ##endif
##integrate creater(RAND_MACRO)
// #define MACRO 1


// ...
    ##error sizeof == 4
##integrate int_is_4_bytes(sizeof(int))
/*
#if sizeof(int) == 4
#error "sizeof(int) == 4"
#endif
*/

// ...
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



// ...
#define ROW 0 1 2
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


// ...
#define ROW EOF NULL stdout 400
    ##foreach(VAR, list)
        ##if ! __IS_MACRO__(row_of_names, VAR)
#error "is not macro: " #VAR
        ##endif
    ##endforeach
##integrate is_macro(list)
/*
#error "is not macro: 400"
*/





        ##error text
        ##error txt
    ##integrate __tmp("hello", "sdsd")
        ##error text
        ##error txt
    ##integrate __tmp("heh),ds", "lsdlsld")
        ##error text
        ##error txt
    ##integrate __tmp("!", "lsldsld")
##integrate hello_world()


    ##error v t h
##integrate variables(8, 9, 7)
