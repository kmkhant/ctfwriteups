#include <stdio.h>

int main() {
  char *file = '/bin/sh\0'; // 796092416
  int n = 796092416;
  printf("%s", file);
  return 0;
}
