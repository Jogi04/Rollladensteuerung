#include <WiFi.h>
 
const char* ssid = "";
const char* password = "";

int relay_up = 12;
int relay_down = 13;
int rollladen_status = 0;
int rollladen_run_time = 10000;

WiFiServer server(80);

TaskHandle_t relay_task_down;
TaskHandle_t relay_task_up;


void relay_task_down_code(void * parameter){
  digitalWrite(relay_down, HIGH);
  rollladen_status = 1;
  delay(rollladen_run_time);
  digitalWrite(relay_down, LOW);
  vTaskDelete(relay_task_down);
}


void relay_task_up_code(void * parameter){
  digitalWrite(relay_up, HIGH);
  rollladen_status = 0;
  delay(rollladen_run_time);
  digitalWrite(relay_up, LOW);
  vTaskDelete(relay_task_up);
}


void stop_rollladen(){
  digitalWrite(relay_down, LOW);
  digitalWrite(relay_up, LOW);
}


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
        String msg = client.readString();                     // "0" = up, "1" = down, "2" = stop
        Serial.println(msg);
        
        if(msg == "0"){
          stop_rollladen();
          xTaskCreatePinnedToCore(relay_task_up_code, "relay_task_up", 10000, NULL, 0, &relay_task_up, 0);
        }
        
        else if(msg == "1"){
          stop_rollladen();
          xTaskCreatePinnedToCore(relay_task_down_code, "relay_task_down", 10000, NULL, 0, &relay_task_down, 0);
        }
        
        else if(msg == "2"){
          stop_rollladen();
        }
      }
    }
  }
}
