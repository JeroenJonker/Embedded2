/*
 *  This sketch sets up the ESP8266 as a Socket Server.
 *  The esp has a IR-led connected on GPIO2.
 */

#include <ESP8266WiFi.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>

#define IR_LED 2  // ESP8266 GPIO pin set to GPIO2

IRsend irsend(2);  // Set the GPIO to be used to sending the message.

const char* ssid = "Domotica";
const char* password = "domotica";

WiFiServer server(12478);

void setup() {
  irsend.begin();
  Serial.begin(115200);
  delay(10);

  
  // Connect to WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
  // Start the server
  server.begin();
  Serial.println("Server started");

  // Print the IP address
  Serial.println(WiFi.localIP());
}

void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
  
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
  
  String req = client.readStringUntil('\r');
  Serial.println(req);
  for (int x = 0; x < 20; x++)
  {
    irsend.sendNEC(req.toInt(), 32);
    delay(10);
  }
  client.flush();

  Serial.println("Client disonnected");
}

