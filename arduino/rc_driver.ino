#include <AFMotor.h>
AF_DCMotor motor1(1, MOTOR12_64KHZ);
AF_DCMotor motor2(2, MOTOR12_64KHZ);

//Function Declaration

void Left();
void Right();
void Forward(); 
void Backward();


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
    switch (buff)
    {
      case 'l':
      {
        Left();
      }
      case 'r':
      {
        Right();
      }
      case 'f':
      {
        Forward();
      }
      case 'b':
      {
        Backward();
      }
    }
    
  }
}

void Left()
{
   
   
    int val=Serial.parseInt();
    motor2.setSpeed(val);
    motor2.run(FORWARD);  //left
    Serial.println("check Left");
    delay(1000);
    Stop2();
    Serial.println("check motor2 Stopped");
    
   
}

   void Right()
{
   
   
    int val=Serial.parseInt();
    motor2.setSpeed(val);
    motor2.run(BACKWARD);  //right
    
    Serial.println("check right");  
    delay(1000);
    Stop2();
    Serial.println("check motor2 Stopped");
      
}

void Forward()
{
   
   
    int val=Serial.parseInt();
    motor1.setSpeed(val);
    motor1.run(FORWARD);  // forward
     Serial.println("check Forrward");    
 delay(1000);
  Stop1();
  Serial.println(" check motor2 Stopped");
   
}

void Backward()
{
   
   
    int val=Serial.parseInt();
    motor1.setSpeed(val);
    motor1.run(BACKWARD);  //backward
     Serial.println("check Backward");    
    delay(1000);
    Stop1();
  Serial.println("check motor1 Stopped");
}

void Stop1()
{
  motor1.run(RELEASE);
  Serial.println("motor1 Stopped");
  while(1)
    {
      if(Serial.available()>0)
      {
        Readdata();    
      }
    }
   
}

void Stop2()
{
  motor2.run(RELEASE);
  Serial.println("motor2 Stopped");
  while(1)
    {
      if(Serial.available()>0)
      {
        Readdata();    
      }
    }
   
}
