//#include <AsyncMqttClient.h>
#include <Wire.h>
#include <WiFi.h>
#include<PubSubClient.h>

// Wifi Credentials.
const char* ssid = "WBL";
const char* password = "B10s3nsors";
#define MSG_BUFFER_SIZE  (50)
WiFiClient espClient;
PubSubClient client(espClient);

// public broker for now.
const char* mqtt_server = "test.mosquitto.org";//"test.mosquitto.org"; 
char msg[MSG_BUFFER_SIZE];
int value = 0;

// Define publisher route.
const char* MQTT_PUB_VOLT0 = "neuroPort/adc1115/voltage0/Device1";
const char* MQTT_PUB_VOLT1 = "neuroPort/adc1115/voltage1/Device1";
const char* MQTT_PUB_VOLT2 = "neuroPort/adc1115/voltage2/Device1";
const char* MQTT_PUB_VOLT3 = "neuroPort/adc1115/voltage3/Device1";

void setup_wifi() {

//  delay(10);
  // We start by connecting to a WiFi network.
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
void callback(char* topic, byte* payload ,unsigned int length ) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
 for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  
  Serial.println();

}
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(100);
    }
  }
}
void setup() {      
  // initialize the serial communication:
  Serial.begin(9600);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);  
//  Serial.println(__FILE__);
//  Serial.print("ADS1X15_LIB_VERSION: ");
//  Serial.println(ADS1X15_LIB_VERSION);
  
  pinMode(14, INPUT); // Setup for leads off detection LO +
  pinMode(12, INPUT); // Setup for leads off detection LO - 
}
//
const unsigned long READ_PERIOD = 4000;  // 4000 us: 250 Hz
unsigned long prev_micros = 0;
void loop() {
  unsigned long curr_micros = micros();
  // handel reconnection.
  if(!client.connected()){
    reconnect();
  }
  client.loop();
 if(curr_micros-prev_micros>=READ_PERIOD)
 {
        Serial.print(analogRead(A0),curr_micros)
  
//      Serial.sprintf("%d,%lu \n",analogRead(A0),curr_micros);
      prev_micros = curr_micros;
      client.publish(MQTT_PUB_VOLT0, String(analogRead(A0)).c_str());
  }  
}
