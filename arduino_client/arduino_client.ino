#include <WiFi.h>
 
const char* ssid = "<SSID>";
const char* password = "<PASSWORD>";

WiFiServer server(80);

int LED = 12;


void connect_to_wifi(){
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);;
    Serial.print("Connecting to ");
    Serial.println(ssid);
  }
 
  Serial.print("Connected to ");
  Serial.println(ssid);
}


void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  
  connect_to_wifi();
  server.begin();
}
 
void loop() {
  WiFiClient client = server.available();

  if(client){
    while(client.connected()){
      while(client.available()){
        String msg = client.readString();
        Serial.println(msg);
        static int led_state = 0;
        
        if(msg == "close"){
          digitalWrite(LED, LOW);
          led_state = 0;
        }else if(msg == "open"){
          digitalWrite(LED, HIGH);
          led_state = 1;
        }
      }
    }
  }
}
