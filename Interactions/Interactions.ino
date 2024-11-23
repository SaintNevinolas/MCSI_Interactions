#include <Wire.h>
#include "LSM6DS3.h"

#define D_TOUCH 8 //D8
#define A_PIEZO 14 //A0
LSM6DS3 I2C_ACCELERO(I2C_MODE, 0x6A); //Capteur 6 Axis Accelerometer&Gyroscope
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

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial);
  if (I2C_ACCELERO.begin() != 0) {
      Serial.println("Device error");
  } else {
      Serial.println("Device OK!");
  }

  if (0 != config_free_fall_detect()) {
      Serial.println("Fail to configure!");
  } else {
      Serial.println("Success to Configure!");
  }
  pinMode(D_TOUCH, INPUT);
  pinMode(A_PIEZO, INPUT);
  //pinMode(D_TILT, INPUT);
  //Wire1.begin();
}

void loop() {
  //trouver_adresse_i2c(); Décommenter pour connaître l'addresse de l'accéléromètre si jamais elle change

  
  readAccelero(I2C_ACCELERO,false);
  if (acceleroXYZ[0]>=4.0){
    Serial.println("Gauche");
  }else if(acceleroXYZ[0]<=-4.0){
    Serial.println("Droite");
  }else{
    Serial.println("Centre");
  }
  Serial.print("TOUCH Value : ");
  Serial.println(digitalRead(D_TOUCH));
  
  Serial.print("PIZEO Value : ");
  Serial.println(analogRead(A_PIEZO));
  delay(100);
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
