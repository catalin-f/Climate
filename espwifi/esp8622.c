#include <PubSubClient.h>
#include <ESP8266WiFi.h>

// Replace these with your WiFi network settings
//const char* ssid = "dlink-2228"; //replace this with your WiFi network name
//const char* password = "CaRd4455"; //replace this with your WiFi network password
//const char* mqtt_server = "192.168.0.170";

const char* ssid = "Card_248_IoT"; //replace this with your WiFi network name
const char* password = "Danger!2W&"; //replace this with your WiFi network password
const char* mqtt_server = "192.168.50.247";

WiFiClient espClient;
PubSubClient client(espClient);
int HeatingPin = 0;
String switch1;
String strTopic;
String strPayload;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void callback(char* topic, byte* payload, unsigned int length) {
  payload[length] = '\0';
  strTopic = String((char*)topic);
  if(strTopic == "eu/releu")
    {
    switch1 = String((char*)payload);
    if(switch1 == "ON")
      {
        Serial.println("ON");
        digitalWrite(HeatingPin, HIGH);
      }
    else
      {
        Serial.println("OFF");
        digitalWrite(HeatingPin, LOW);
      }
    }
}
 

//
//void setup()
//{
//  delay(1000);
//  Serial.begin(115200);
// 
//  WiFi.begin(ssid, password);
//
//  Serial.println();
//  Serial.print("Connecting");
//  while (WiFi.status() != WL_CONNECTED)
//  {
//    delay(500);
//    Serial.print(".");
//  }
//
//  Serial.println("success!");
//  Serial.print("IP Address is: ");
//  Serial.println(WiFi.localIP());
//}


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
  if (client.connect("client")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.subscribe("eu/#");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
 

void setup()
{
  Serial.begin(115200);
  setup_wifi(); 
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  pinMode(HeatingPin, OUTPUT);
  digitalWrite(HeatingPin, HIGH);
}
 

void loop()
{
  if (!client.connected()) {
    reconnect();
 }
  client.loop();
}
