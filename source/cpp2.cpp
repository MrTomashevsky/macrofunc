
// ...
#define MACRO1 0
#define MACRO2 0 + 3
#define MACRO3 0 + 3 + MACRO2
#define MACRO4 #0 + 3 + MACRO2
#define MACRO5 L#0 + 3 + MACRO#0 + 3 + MACRO2
/*
#define MACRO1 0
#define MACRO2 3
#define MACRO3 6
#define MACRO4 "6"
#define MACRO5 L"6"
*/


//...
#define RAND_MACRO 100
#define MACRO 0
#define MACRO 1
#define MACRO 2
#define MACRO 3
// #define MACRO 1


// ...
#if  sizeof == 4
   #error " sizeof == 4"
#endif
/*
#if sizeof(int) == 4
#error "sizeof(int) == 4"
#endif
*/

// ...
int global[3];
void function0 (void) { global[0]++;oid function0 (void) { global[0]++; }
void (*global_functions[3])(void) = {
functionunction0
,
};
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
int global[ROW];
void function0 (void) { global[0]++;oid function0 (void) { global[0]++; }
void (*global_functions[ROW])(void) = {
functionunction0
,
};
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
#error "is not macro: " #list
/*
#error "is not macro: 400"
*/





#if  text
   #error " text"
#endif
#if  txt
   #error " txt"
#endif
#if  text
   #error " text"
#endif
#if  txt
   #error " txt"
#endif
#if  text
   #error " text"
#endif
#if  txt
   #error " txt"
#endif
#if  text
   #error " text"
#endif
#if  txt
   #error " txt"
#endif


#if  v t h
   #error " v t h"
#endif
