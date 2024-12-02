#include <Wire.h>
#include "LSM6DS3.h" //Install the library Seeed Arduino LSM6DS3 by Seeed
#include "Ultrasonic.h"

#define D_TOUCH 8 //D8
#define A_PIEZO 14 //A0
#define D_TILT 15
Ultrasonic D_USONIC(7); //D7 Ultrasonic Ranger
LSM6DS3 I2C_ACCELERO(I2C_MODE, 0x6A); //Capteur 6 Axis Accelerometer&Gyroscope ; On far LEFT I2C pin
                                  /*
                                  * Dans les cas où ce genre d'erreur apparaît :
                                  * LSM6DS3.cpp:89:17: error: 'class arduino::ArduinoSPI' has no member named 'setClockDivider'
                                  * SPI.setClockDivider(SPI_CLOCK_DIV4);
                                  *     ^~~~~~~~~~~~~~~
                                  * 'SPI_CLOCK_DIV4' was not declared in this scope
                                  * SPI.setClockDivider(SPI_CLOCK_DIV4);
                                  *                     ^~~~~~~~~~~~~~
                                  * etc..
                                  * Commenter des lignes 84 à 115 du fichier Arduino\libraries\Seeed_Arduino_LSM6DS3\LSM6DS3.cpp
                                  */

float acceleroXYZ[3]={};
int piezoValue = -1;
int touchValue = -1;
long USonicRangeInCentimeters = -1;
long tiltValue = -1;

const int seuil = 17; //distance en cm à définir pour considérer la distance de la feuille à souffler

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial);
  // if (I2C_ACCELERO.begin() != 0) {
  //     Serial.println("Device error");
  // } else {
  //     Serial.println("Device OK!");
  // }

  // if (0 != config_free_fall_detect()) {
  //     Serial.println("Fail to configure!");
  // } else {
  //     Serial.println("Success to Configure!");
  // }
  pinMode(D_TOUCH, INPUT);
  pinMode(A_PIEZO, INPUT);
  pinMode(D_TILT, INPUT);
  //Wire1.begin();
}

void loop() {
  //trouver_adresse_i2c(); Décommenter pour connaître l'addresse de l'accéléromètre si jamais elle change
  String sensorValues = "";
  //readAccelero(I2C_ACCELERO,false);
  if (acceleroXYZ[0]>=4.0){
    //Serial.println("Gauche");
    sensorValues+="G,";
  }else if(acceleroXYZ[0]<=-4.0){
    //Serial.println("Droite");
    sensorValues+="D,";
  }else{
    //Serial.println("Centre");
    sensorValues+="C,";
  }
  
  //readTouch(false);
  if(touchValue){
    //Serial.println("TOUCHED");
    sensorValues+="1,";
  }else{
    //Serial.println("NOT TOUCHED");
    sensorValues+="0,";
  }
  
  //readPiezo(false);
  if(piezoValue>1000){
    //Serial.println("Vibration");
    sensorValues+="1,";
  }else{
    //Serial.println("No Vibration");
    sensorValues+="0,";
  }

  readUltraSonic(false);
  if(USonicRangeInCentimeters>seuil){
    //Serial.println("On souffle");
    sensorValues+="1,";
  }else{
    //Serial.println("On souffle pas");
    sensorValues+="0,";
  }

  readTilt(false);
  if(tiltValue==1){
    //Serial.println("Vibration");
    sensorValues+="1,";
  }else{
    //Serial.println("No Vibration");
    sensorValues+="0,";
  }

  sensorValues=sensorValues.substring(0,sensorValues.length()-1); //retirer la virgule de fin
  Serial.println(sensorValues);
  
}

void readAccelero(LSM6DS3 accelero,bool afficher){
  acceleroXYZ[0] = accelero.readFloatAccelX(); //valeurs allant jusqu'à 8.0 environ, int16_t readRawAccelX valeurs allant jusqu'à environ 30k
  acceleroXYZ[1] = accelero.readFloatAccelY(); //int16_t readRawAccelY
  acceleroXYZ[2] = accelero.readFloatAccelZ(); //int16_t readRawAccelZ
  if(afficher){
    Serial.print("Valeur accelerometre : ");
    Serial.print(acceleroXYZ[0]);
    Serial.print(" ");
    Serial.print(acceleroXYZ[1]);
    Serial.print(" ");
    Serial.println(acceleroXYZ[2]);
  }
}

void readTouch(bool afficher){
  touchValue = digitalRead(D_TOUCH);
  if(afficher) {
    Serial.print("Valeur Touch : ");
    Serial.println(touchValue);
  }
}

void readPiezo(bool afficher){
  piezoValue = analogRead(A_PIEZO);
  if(afficher) {
    Serial.print("Valeur piezo : ");
    Serial.println(piezoValue);
  }
}

void readTilt(bool afficher){
  //Serial.println(analogRead(5));
  tiltValue = digitalRead(D_TILT);
  if(afficher) {
    Serial.print("Valeur tilt : ");
    Serial.println(tiltValue);
  }
}

void readUltraSonic(bool afficher){
  USonicRangeInCentimeters = D_USONIC.MeasureInCentimeters();
  if(afficher){
    Serial.print("Obstacle distance : ");
    Serial.print(USonicRangeInCentimeters);
    Serial.println("cm");
  }
}
int config_free_fall_detect(void) {
  uint8_t error = 0;
  uint8_t dataToWrite = 0;

  dataToWrite |= LSM6DS3_ACC_GYRO_BW_XL_200Hz;
  dataToWrite |= LSM6DS3_ACC_GYRO_FS_XL_2g;
  dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_416Hz;

  error += I2C_ACCELERO.writeRegister(LSM6DS3_ACC_GYRO_CTRL1_XL, dataToWrite);
  error += I2C_ACCELERO.writeRegister(LSM6DS3_ACC_GYRO_WAKE_UP_DUR, 0x00);
  error += I2C_ACCELERO.writeRegister(LSM6DS3_ACC_GYRO_FREE_FALL, 0x33);
  error += I2C_ACCELERO.writeRegister(LSM6DS3_ACC_GYRO_MD1_CFG, 0x10);
  error += I2C_ACCELERO.writeRegister(LSM6DS3_ACC_GYRO_MD2_CFG, 0x10);
  error += I2C_ACCELERO.writeRegister(LSM6DS3_ACC_GYRO_TAP_CFG1, 0x81);

  return error;
}
void trouver_adresse_i2c(void){
  byte error, address;
  int nDevices = 0;

  for (address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("Device found at address 0x");
      Serial.println(address, HEX);
      nDevices++;
    }
  }

  if (nDevices == 0) {
    Serial.println("No I2C devices found\n");
  } else {
    Serial.println("done\n");
  }
}
