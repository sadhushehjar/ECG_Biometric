//#include <BLEDevice.h>
//#include <BLEServer.h>
//#include <BLEUtils.h>
//#include <BLE2902.h>
//BLEServer* pServer = NULL;
//BLECharacteristic* pCharacteristic = NULL;
//bool deviceConnected = false;
//bool oldDeviceConnected = false;
//uint32_t value = 0;
//
//// See the following for generating UUIDs:
//// https://www.uuidgenerator.net/
//// TODO CHANGE THESE
//#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
//#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
//
//class MyServerCallbacks: public BLEServerCallbacks {
//    void onConnect(BLEServer* pServer) {
//      deviceConnected = true;
//      BLEDevice::startAdvertising();
//    };
//
//    void onDisconnect(BLEServer* pServer) {
//      deviceConnected = false;
//    }
//};


void setup() {      
  // initialize the serial communication:
  Serial.begin(9600);
    // Create the BLE Device
  //BLEDevice::init("ESP32");
    // Create the BLE Server
//  pServer = BLEDevice::createServer();
//  pServer->setCallbacks(new MyServerCallbacks());
//
//    // Create the BLE Service
//  BLEService *pService = pServer->createService(SERVICE_UUID);

//  // Create a BLE Characteristic
//  pCharacteristic = pService->createCharacteristic(
//                      CHARACTERISTIC_UUID,
//                      BLECharacteristic::PROPERTY_READ   |
//                      BLECharacteristic::PROPERTY_WRITE  |
//                      BLECharacteristic::PROPERTY_NOTIFY |
//                      BLECharacteristic::PROPERTY_INDICATE
//                    );
//    // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
//  // Create a BLE Descriptor
//  pCharacteristic->addDescriptor(new BLE2902());

//  // Start the service
//  pService->start();
//
//  // Start advertising
//  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
//  pAdvertising->addServiceUUID(SERVICE_UUID);
//  pAdvertising->setScanResponse(false);
//  pAdvertising->setMinPreferred(0x0);  // set value to 0x00 to not advertise this parameter
//  BLEDevice::startAdvertising();
//  Serial.println("Waiting a client connection to notify...");
//  
  pinMode(14, INPUT); // Setup for leads off detection LO +
  pinMode(12, INPUT); // Setup for leads off detection LO - 
}
//
const unsigned long READ_PERIOD = 4000;  // 4000 us: 250 Hz


//void loop() { 
// // notify changed value
//    if (deviceConnected) {
//        pCharacteristic->setValue((uint8_t*)&value, 4);
//        pCharacteristic->notify();
////        value++;
//        delay(10); // bluetooth stack will go into congestion, if too many packets are sent, in 6 hours test i was able to go as low as 3ms
//    }
//    // disconnecting
//    if (!deviceConnected && oldDeviceConnected) {
//        delay(500); // give the bluetooth stack the chance to get things ready
//        pServer->startAdvertising(); // restart advertising
//        Serial.println("start advertising");
//        oldDeviceConnected = deviceConnected;
//    }
//    // connecting
//    if (deviceConnected && !oldDeviceConnected) {
//        // do stuff here on connecting
//        oldDeviceConnected = deviceConnected;
//    }
//    
//    static unsigned long lastRead;
//    if (micros() - lastRead >= READ_PERIOD) {
//        lastRead += READ_PERIOD;
//        if (digitalRead(10) == 1 || digitalRead(11) == 1){
//            Serial.println('!');
//        }
//        else{
//            static unsigned long t = millis();
//           // Serial.println(t);
//            Serial.println(analogRead(A0) * (3.3/1024));
//        }
//    }
//}
unsigned long prev_micros = 0;
void loop() {
  unsigned long curr_micros = micros();
 if(curr_micros-prev_micros>=READ_PERIOD)
 {
      Serial.printf("%d,%lu \n",analogRead(A0),curr_micros);
      prev_micros = curr_micros;
  }  
}
