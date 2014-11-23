static int t=0x1770;
int sleep(int sec){
  t +=sec;
}

int time(){
  return t;
}

//gcc -shared -fPIC sleep.c -o sleep.so
