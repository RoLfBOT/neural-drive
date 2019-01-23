#include <AFMotor.h>
AF_DCMotor motor1(1, MOTOR12_64KHZ);
AF_DCMotor motor2(2, MOTOR12_64KHZ);

void setup() {
  Serial.begin(9600);
}


void loop() 
{
    Readdata(); 
}

void Readdata()
{
  if(Serial.available()>0)
  {
    char buff=Serial.read();
    int val=Serial.parseInt();
    switch (buff)
    {
      case 'l':
      {
        turnMotor(motor2,false,val);
        break;
      }
      case 'r':
      {
        turnMotor(motor2,true,val);
        break;
      }
      case 'f':
      {
        turnMotor(motor1,false,val);
        break;
      }
      case 'b':
      {
        turnMotor(motor1,true,val);
        break;
      }
    }
    
  }
}

void turnMotor(AF_DCMotor motor,bool backward,int val){
  motor.setSpeed(val);
  if(backward){
    motor.run(BACKWARD);
  }else{
    motor.run(FORWARD);
  }
}
