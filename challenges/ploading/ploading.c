#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#define TGTTIME 6000


int main(){
  time_t starttime;
  time_t endtime;
  //lyrics 39lines
  char *lithiumflower[] = {"She's so cold and human",
                           "It's something humans do",
                           "She stays so golden solo",
                           "She's so number nine",
                           "She's incredible math",
                           "Just incredible math",
                           "And is she really human?",
                           "She's just so something new",
                           "A waking lithium flower",
                           "Just about to bloom",
                           "I smell lithium now",
                           "Smelling lithium now",
                           "How is she when she doesn't surf?",
                           "How is she when she doesn't surf?",
                           "How is she when she doesn't surf?",
                           "I wonder what she does when she wakes up?",
                           "When she wakes up",
                           "So matador",
                           "So calm",
                           "So oil on a fire",
                           "She's so good",
                           "She's so good",
                           "She's so goddess lithium flower",
                           "So sonic wave",
                           "Yeah, she's so groove, yeah",
                           "She's so groove",
                           "Yeah",
                           "Wow, where did she learn how to surf?",
                           "Wow, where did she learn how to surf?",
                           "Wow, where did she learn how to surf?",
                           "You know I've never seen the girl wipe out",
                           "How does she so perfectly surf?",
                           "How does she so perfectly surf?",
                           "How does she so perfectly surf?",
                           "I wonder what she does when she wakes up?",
                           "I wanna go surfing with her",
                           "I wanna go surfing with her",
                           "I wanna go surfing with her",
                           "I wanna go surfing with her"
  };
  
  //base time
  starttime=time(NULL);
  //printf("Start time = %d\n",(int)starttime);

  //do shit
  int i;
  for (i=0; i<6000; i++){
    //i%39
    //printf("%d\n",i%39);
    printf("- %50s\n",lithiumflower[i%39]);
    sleep(1);
    //timecheck
    endtime=time(NULL);
    //printf("End time = %d\n", (int)endtime);
    int dff = endtime - starttime;
    //    printf("Differnce is %d\n",dff);
    if((endtime - starttime) >= TGTTIME){
      //print flag
      printf("flag{%s}", lithiumflower[8]);
    }
  }

  //check time
  //  gettimeofday(&tv, NULL);
  //endtime=tv.tv_sec;
  //printf("End time = %ld\n",endtime);
  //int difference = endtime - starttime;
  //printf("Difference is %d\n",difference);

}
