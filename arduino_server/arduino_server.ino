#include <WiFi.h>
 
const char* ssid = "";
const char* password = "";

int relay_up = 12;
int relay_down = 13;
int rollladen_status = 0;
int rollladen_run_time = 10000;

WiFiServer server(80);


void connect_to_wifi(){
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }

  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  pinMode(relay_up, OUTPUT);
  pinMode(relay_down, OUTPUT);
  digitalWrite(relay_up, LOW);
  digitalWrite(relay_down, LOW);
  
  connect_to_wifi();
  server.begin();
}
 
void loop() {
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print("Connecting to ");
    Serial.println(ssid);
  }

  WiFiClient client = server.available();

  if(client){
    while(client.connected()){
      while(client.available()){
        String msg = client.readString();                     // "0" = down, "1" = up, "2" = stop
        Serial.println(msg);
        
        if(msg == "0"){
          digitalWrite(relay_up, HIGH);
          rollladen_status = 0;
          unsigned long time_now = millis();
          
          while (millis() < time_now + rollladen_run_time){
            msg = client.readString();
            if(msg == "2"){
              rollladen_status = 2;
              break;
            }
            else if(msg == "1"){
              digitalWrite(relay_up, LOW);
              digitalWrite(relay_down, HIGH);
              break;
            }
          }
          
          digitalWrite(relay_up, LOW);
        }
        
        else if(msg == "1"){
          digitalWrite(relay_down, HIGH);
          rollladen_status = 1;
          unsigned long time_now = millis();
          
          while (millis() < time_now + rollladen_run_time){
            msg = client.readString();
            if(msg == "2"){
              rollladen_status = 2;
              break;
            }
            else if(msg == "0"){
              digitalWrite(relay_down, LOW);
              digitalWrite(relay_up, HIGH);
              break;
            }
          }
          
          digitalWrite(relay_down, LOW);
        }
        
        else if(msg == "2"){
          digitalWrite(relay_up, LOW);
          digitalWrite(relay_down, LOW);
          rollladen_status = 2;
        }
      }
    }
  }
}
