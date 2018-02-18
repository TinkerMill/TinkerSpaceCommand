/*
 * To Run: g++ TimeCheck.cpp TimeCheck_example.cpp -o test.out
 *
 */
#include <ctime>
#include <iostream>
#include <string>
#include "TimeCheck.h"

using namespace std;

// Refresh rate for checking temperatures and updating PID input milliseconds, default 1000
#define TEMP_CHK_S 1

unsigned long setpoint = 1;

int main()
{

time_t timeNow = time(0);

// Create a clock to print the current temperature every second
TimeCheck printTempClock(timeNow, setpoint);

int ind = 0;

while (ind < 10)
{
  time(&timeNow);
    
  //cout << "Current Time Is: " << timeNow << "\n";

  if (printTempClock.check_trigger(timeNow)){
    cout << "Trip Time: " << timeNow << "\n";
    ind++;
  }
} // for loop

return 0;
}
