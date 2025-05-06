#define MACRO 9
int global[3];
void function0 (void) { global[0]++; }
void (*global_functions[3])(void) = {
function0
,
};
#define ROW 0 1 2
void functionROW (void) { std::cout << ROW << std::endl; }
void (*global_functions[__SIZE_LIST__])(void) = {
functionROW
,
};
#define ROW EOF NULL stdout 400
#error "is not macro: ""list"
#if text
   #error "text"
#endif
#if txt
   #error "txt"
#endif
#if text
   #error "text"
#endif
#if txt
   #error "txt"
#endif
#if text
   #error "text"
#endif
#if txt
   #error "txt"
#endif
#if text
   #error "text"
#endif
#if txt
   #error "txt"
#endif
#if v t h
   #error "v t h"
#endif
