#include <SPI.h>
#include <RF22.h>
#include <RF22Router.h>

#define MY_ADDRESS 1
#define DESTINATION_ADDRESS 2
#define BAUD_RATE 9600
#define FREQUENCY 440.0

void print_measurments(int initial_time, int final_time) {
  float throughput=(float)counter*number_of_bytes*1000.0/(final_time-initial_time);

  Serial.print("Throughput=");
  Serial.print(throughput);
  Serial.println("Bytes/s");

  Serial.print("Initial time= ");  
  Serial.print(initial_time);

  Serial.print("Final time= ");  
  Serial.println(final_time);
  Serial.println("");
}

RF22Router rf22(MY_ADDRESS);  // Initiate the class to talk to my radio with MY_ADDRESS
const int sensorPin = A0;

void setup() {
  Serial.begin(BAUD_RATE);
  if (!rf22.init()) {
    Serial.println("RF22 init failed");
  }

  if (!rf22.setFrequency(FREQUENCY)) {
    Serial.println("setFrequency Fail");
  }

  // Available power modes for the transmitter in dBm: 1, 2, 5, 8, 11, 14, 17, 20
  rf22.setTxPower(RF22_TXPOW_20DBM);
  rf22.setModemConfig(RF22::GFSK_Rb125Fd125);
  rf22.addRouteTo(DESTINATION_ADDRESS, DESTINATION_ADDRESS);
  for(int pinNumber = 4; pinNumber < 6; pinNumber++) {
    pinMode(pinNumber, OUTPUT);
    digitalWrite(pinNumber, LOW);
  }

  delay(1000);
}

void loop() {
  int counter = 0;
  int initial_time = millis();

  // Mock measurements
  int sensorVal = analogRead(sensorPin);
  Serial.print("My measurement is: ");
  Serial.println(sensorVal);

  // Transform measured value into a uint8_t variable
  char data_read[RF22_ROUTER_MAX_MESSAGE_LEN];
  uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
  memset(data_read, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  sprintf(data_read, "%d", sensorVal);
  data_read[RF22_ROUTER_MAX_MESSAGE_LEN - 1] = '\0';
  memcpy(data_send, data_read, RF22_ROUTER_MAX_MESSAGE_LEN);

  int number_of_bytes = sizeof(data_send);
  Serial.print("Number of Bytes= ");
  Serial.println(number_of_bytes);

  // Sending variable data_send to DESTINATION_ADDRESS
  if (rf22.sendtoWait(data_send, sizeof(data_send), DESTINATION_ADDRESS) != RF22_ROUTER_ERROR_NONE) {
    Serial.println("Failed to sent message");
  } else {
    counter=counter+1;
    uint8_t rssi = rf22.rssiRead();
    float Pr=((float)rssi-230.0)/1.8;
    Serial.print("RSSI= ");
    Serial.print(Pr);
    Serial.println(" dBm");

    Serial.println("Message sent successfully");
  }

  int final_time=millis();
  print_measurements(initial_time, final_time)
  delay(2000);
}
