#include <SPI.h>
#include <RF22.h>
#include <RF22Router.h>

#define TRANSMITTER 1
#define RECEIVER 2

#define BAUD_RATE 9600
#define FREQUENCY 440.0

RF22Router rf22(RECEIVER);
int received_data=0;
uint8_t rssi;
float pwr=-90;

void setup() {

  Serial.begin(BAUD_RATE);
  if (!rf22.init()) {
    Serial.println("RF22 init failed!");
  }

  if (!rf22.setFrequency(FREQUENCY)) {
    Serial.println("setFrequency failed!");
  }

  // available power modes for the transmitter in dBm: 1, 2, 5, 8, 11, 14, 17, 20
  rf22.setTxPower(RF22_TXPOW_20DBM);
  rf22.setModemConfig(RF22::GFSK_Rb125Fd125);// The modulation should be the same as that of the transmitter. Otherwise no communication will take place

  // define the routes for this network
  rf22.addRouteTo(TRANSMITTER, TRANSMITTER);
  for (int pinNumber=4; pinNumber<6; pinNumber++) {
    pinMode(pinNumber,OUTPUT);
    digitalWrite(pinNumber, LOW);
  }

  delay(100); 
}

void loop() {

  uint8_t buf[RF22_ROUTER_MAX_MESSAGE_LEN];
  char incoming[RF22_ROUTER_MAX_MESSAGE_LEN];
  memset(buf, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  memset(incoming, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);

  uint8_t len = sizeof(buf); 
  uint8_t from;
  //digitalWrite(5, LOW);
  if (rf22.recvfromAck(buf, &len, &from)) {
    // digitalWrite(5, HIGH);

    rssi = rf22.rssiRead();
    pwr= ((float)rssi - 230.0) / 1.8;
    //Serial.print("RSSI= ");
    //Serial.println(pwr);
    //Serial.println(" dBm");

    buf[RF22_ROUTER_MAX_MESSAGE_LEN - 1] = '\0';
    memcpy(incoming, buf, RF22_ROUTER_MAX_MESSAGE_LEN);
    //Serial.print("got request from : ");
    //Serial.println(from, DEC);
    
    received_data = atoi((char*)incoming);
    Serial.println(received_data);
  }
}
