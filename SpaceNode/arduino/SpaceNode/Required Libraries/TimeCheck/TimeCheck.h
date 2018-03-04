
/*
 TimeCheck.h - Library for Checking the Current time and comparing it to a 
 setpoint. Can trip an "if statement" or call a callback.

 Created by: Steve Lammers, 2/18/2018

  End user provides a 
    - Timer Setpoint 
*/

#ifndef TIMECHECK
#define TIMECHECK

//#include "Arduino.h"

class TimeCheck{
  private:
	  unsigned long timeNow, timePrevious, timeTrigger;

	public:
  // Constructor 
	TimeCheck(unsigned long _timeNow, unsigned long _timeTrigger);

  // Deconstructor
  //~TimeCheck();
	
  void set_trigger(unsigned long _timeTrigger);

	bool check_trigger(unsigned long _timeNow);

}; // class TimeCheck



#endif //TIMECHECK
