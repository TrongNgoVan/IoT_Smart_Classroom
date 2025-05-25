// #include <WiFi.h>
// #include <ESP32Servo.h>
// #include <WebServer.h>

// #define POWER_PIN 32  // Pin for rain sensor power
// #define A0_PIN 26     // Pin for rain sensor signal

// Servo myservo;

// int pos = 0; // Servo position
// bool hasRun = false; // Biến kiểm soát để đảm bảo chỉ chạy một lần

// // WiFi credentials
// const char* ssid = "Ngọ Văn Trọng";
// const char* password = "13082003";

// // WebServer
// WebServer server(80);

// // Function to connect to Wi-Fi
// void setupWiFi() {
//   delay(10);
//   Serial.println("Connecting to WiFi...");
//   WiFi.begin(ssid, password);
//   while (WiFi.status() != WL_CONNECTED) {
//     delay(1000);
//     Serial.print(".");
//   }
//   Serial.println("\nConnected to WiFi");
//   Serial.print("ESP32 IP Address: ");
//   Serial.println(WiFi.localIP());
// }

// // Handle root URL (index page)
// void handleRoot() {
 
// String page = "<html><head><title>Control Window</title></head><body>";
//   page += "<p><a href='/open'>Open</a></p>";
//   page += "<p><a href='/close'>Close</a></p>";
  
//   page += "</body></html>";
//   server.send(200, "text/html", page);
// }

// // Handle open door request
// void handleOpen() {
//   openDoor();
//   server.send(200, "text/plain", "Open");
// }

// // Handle close door request
// void handleClose() {
//   closeDoor();
//   server.send(200, "text/plain", "Close");
// }

// // Open door function (move servo to open position)
// void openDoor() {
//   Serial.println("Opening door...");
//   for (pos = 0; pos <= 90; pos += 2) {
//     myservo.write(pos);
//     delay(15);
//   }
//   Serial.println("Door opened!");
// }

// // Close door function (move servo to close position)
// void closeDoor() {
//   Serial.println("Closing door...");
//   for (pos = 90; pos >= 0; pos -= 2) {
//     myservo.write(pos);
//     delay(15);
//   }
//   Serial.println("Door closed!");
// }

// void setup() {
//   myservo.attach(4);  // Attach the servo motor to pin 4
//   myservo.write(0);   // Set the initial position of the servo
//   pinMode(POWER_PIN, OUTPUT);  // Rain sensor power pin
//   Serial.begin(9600);  // Start serial communication

//   setupWiFi();
//   server.on("/", HTTP_GET, handleRoot);
//   server.on("/open", HTTP_GET, handleOpen);
//   server.on("/close", HTTP_GET, handleClose);

//   server.begin();  // Start web server
// }

// // Loop function
// void loop() {
//   server.handleClient();

//     // Bật cảm biến mưa và đọc giá trị
//   digitalWrite(POWER_PIN, HIGH); // Cấp nguồn cho cảm biến mưa
//   delay(100);                     // Chờ ổn định
//   int rain_value = analogRead(A0_PIN); // Đọc giá trị mưa
//   digitalWrite(POWER_PIN, LOW);  // Tắt nguồn cảm biến để tiết kiệm năng lượng
//   Serial.println(rain_value);    // In giá trị ra Serial Monitor để debug

//   // Kiểm tra giá trị mưa
//   if (!hasRun && rain_value <= 3600) { 
//     // Mở cửa: Quay servo đến 90 độ
//     for (pos = 0; pos <= 90; pos += 2) { // goes from 0 degrees to 180 degrees
//       // in steps of 1 degree
//       myservo.write(pos);              // tell servo to go to position in variable 'pos'
//       delay(15);                       // waits 15ms for the servo to reach the position
//        Serial.println("Cửa đã mở");  
//     }
//     delay(2000); 
//     for (pos = 90; pos >= 0; pos -= 2) { // goes from 180 degrees to 0 degrees
//       myservo.write(pos);              // tell servo to go to position in variable 'pos'
//       delay(15);                       // waits 15ms for the servo to reach the position
//        Serial.println("Cửa đã đóng"); 
//     }        

//     hasRun = true;              // Đánh dấu là đã thực hiện xong
//   }

//   delay(500); // Dừng một chút trước khi lặp lại
// }

#include <ESP32Servo.h>

#define POWER_PIN 32  // Chân cấp nguồn cho cảm biến mưa
#define A0_PIN 26     // Chân đọc tín hiệu từ cảm biến mưa

Servo myservo;       // Tạo đối tượng servo
int pos = 90;         // Biến lưu vị trí servo (mở cửa ở 90 độ)
bool isDoorOpen = true; // Biến trạng thái cửa (true: mở, false: đóng)

void setup() {
  myservo.attach(4);        // Gắn servo vào chân GPIO4
  myservo.write(90);        // Đặt servo ở vị trí ban đầu (90 độ - cửa MỞ)
  pinMode(POWER_PIN, OUTPUT); // Cấu hình chân cấp nguồn cho cảm biến mưa
  Serial.begin(9600);         // Khởi động giao tiếp Serial để debug
}

void loop() {
  // Bật cảm biến mưa và đọc giá trị
  digitalWrite(POWER_PIN, HIGH); // Cấp nguồn cho cảm biến mưa
  delay(100);                     // Chờ ổn định
  int rain_value = analogRead(A0_PIN); // Đọc giá trị mưa
  digitalWrite(POWER_PIN, LOW);  // Tắt nguồn cảm biến để tiết kiệm năng lượng
  Serial.println(rain_value);    // In giá trị ra Serial Monitor để debug

  // Kiểm tra nếu có mưa (rain_value <= 3600) và cửa chưa đóng
  if (rain_value <= 3600 && isDoorOpen) { 
    Serial.println("Cảm biến phát hiện mưa và cửa chưa đóng, bắt đầu đóng cửa...");
    for (pos = 90; pos >= 0; pos -= 2) { // Giảm từ 90 độ về 0 độ (đóng cửa)
      myservo.write(pos);              // Điều khiển servo đóng cửa
      delay(15);                       // Chờ servo di chuyển
    }
    isDoorOpen = false; // Đánh dấu cửa đã đóng
    Serial.println("Cửa đã đóng!");
  } 
  // Kiểm tra nếu mưa đã hết (rain_value >= 4000) và cửa chưa mở
  else if (rain_value >= 4000 && !isDoorOpen) {
    Serial.println("Cảm biến phát hiện trời khô ráo, bắt đầu mở cửa...");
    for (pos = 0; pos <= 90; pos += 2) { // Tăng từ 0 độ về 90 độ (mở cửa)
      myservo.write(pos);              // Điều khiển servo mở cửa
      delay(15);                       // Chờ servo di chuyển
    }
    isDoorOpen = true; // Đánh dấu cửa đã mở
    Serial.println("Cửa đã mở!");
  } 

  delay(100); // Dừng một chút trước khi lặp lại
}


