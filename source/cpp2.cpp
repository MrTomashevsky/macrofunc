
// ...
has been integrated
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
has been integrated
##integrate creater(RAND_MACRO)
// #define MACRO 1


// ...
has been integrated
##integrate int_is_4_bytes(sizeof(int))
/*
#if sizeof(int) == 4
#error "sizeof(int) == 4"
#endif
*/

// ...
has been integrated
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
has been integrated
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
has been integrated
##integrate is_macro(list)
/*
#error "is not macro: 400"
*/







has been integrated
    ##integrate __tmp("hello", "sdsd")
has been integrated
    ##integrate __tmp("heh),ds", "lsdlsld")
has been integrated
    ##integrate __tmp("!", "lsldsld")

