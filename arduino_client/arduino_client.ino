#include <WiFi.h>
 
const char* ssid = "FritzBox";
const char* password = "8753946793318200";

WiFiServer server(80);

int LED = 12;

IPAddress local_IP(192, 168, 178, 184);
IPAddress gateway(192, 168, 178, 1);
IPAddress subnet(255, 255, 255, 0);


void connect_to_wifi(){
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("STA Failed to configure");
  }
  
  WiFi.mode(WIFI_MODE_STA);
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print("Connecting to ");
    Serial.println(ssid);
  }
 
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.println(WiFi.localIP());
}


void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  
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
        String msg = client.readString();
        static int led_state = 0;
        
        if(msg == "open"){
          digitalWrite(LED, LOW);
          led_state = 0;
        }else if(msg == "close"){
          digitalWrite(LED, HIGH);
          led_state = 1;
        }
      }
    }
  }
}
