#include "MPU6050.h"    
#include  <Adafruit_BMP280.h>

Adafruit_BMP280 bmp; // I2C Interface

MPU6050 mpu;
int16_t ax, ay, az;
int16_t gx, gy, gz;

struct MyData {
  byte X;
  byte Y;
  byte Z;
  byte GX;
  byte GY;
  byte GZ;
};

MyData data;

//We should calculate offsets!
int offset=20050;

void setup() {
  Serial.begin(9600);
  mpu.initialize();
  
  Serial.println(F("BMP280 test"));
  
  if  (!bmp.begin()) {
  Serial.println(F("Could not find a valid BMP280 sensor,  check wiring!"));
  while (1);
  }
/* Default settings from datasheet.  */
bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                Adafruit_BMP280::STANDBY_MS_500);  /* Standby time. */
}

void loop() {
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  data.Z = map(az, -17000, 17000, 0, 255);  // Z axis data
  
  delay(10);
  Serial.print(bmp.readTemperature()); // in *C degrees
  Serial.print(":");
  //Serial.print(F("Pressure = "));
  Serial.print(bmp.readPressure()/100);  //displaying the Pressure in hPa, you can change the unit
  Serial.print(":");
  //Serial.print("Axis Z:");
  Serial.print(az-offset);
  Serial.println();
  //delay(900); 
}