//Connect the Soil Moisture Sensor in Pin A0

#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "WiFi SSID";
const char* password = "WiFi Pass";

const int sensorPin = A0;

WebServer server(80);

void handleMoisture() {
  int moistureValue = analogRead(sensorPin);
  int moisturePercent = map(moistureValue, 4095, 0, 0, 100);
  server.sendHeader("Access-Control-Allow-Origin", "*"); 
  server.send(200, "text/plain", String(moisturePercent));
}

void setup() {
  Serial.begin(115200);
  pinMode(sensorPin, INPUT);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected. IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/moisture", handleMoisture);
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}