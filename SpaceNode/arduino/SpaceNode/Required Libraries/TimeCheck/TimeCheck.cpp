
#include "TimeCheck.h"

unsigned long timeNow, timePrevious, timeTrigger;

// Constructor
TimeCheck::TimeCheck(unsigned long _timeNow, unsigned long _timeTrigger){
  timePrevious = _timeNow;
  timeNow = _timeNow;
  timeTrigger = _timeTrigger;
}

void TimeCheck::set_trigger(unsigned long _timeTrigger){
  timeTrigger = _timeTrigger;
} 

bool TimeCheck::check_trigger(unsigned long _timeNow){
  bool triggered = false;
  timeNow = _timeNow;
  unsigned long deltaTime = timeNow - timePrevious;
  if (deltaTime >= timeTrigger ){
    timePrevious = timeNow;
    triggered = true;
  }
  else{ triggered = false; }
  
  return triggered;
}


/*
// Refresh rate for checking temperatures and updating PID input milliseconds, default 1000
#define TEMP_CHK_MS 100
// Create a clock to print the current temperature every second
TimeCheck printTempClock(millis(), TEMP_CHK_MS);
	if (printTempClock.check_trigger()){}
*/
