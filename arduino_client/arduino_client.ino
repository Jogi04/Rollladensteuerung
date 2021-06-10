#include <WiFi.h>

int LED = 12;

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  
   WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
    delay(1000);
  }
  
  digitalWrite(LED, HIGH);
}

void loop() {
  delay(1000);
  Serial.println(WiFi.localIP());
}
