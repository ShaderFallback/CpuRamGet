String str;
String cpu;
String ram;
void setup() {
  Serial.begin(115200);
  pinMode(5, OUTPUT);//cpu
  pinMode(10, OUTPUT);//ram
}
void loop() {
  while (!Serial.available());
  str = Serial.readString();

  if (str.equals("handshake")) {
    Serial.print("handshake");
  } else {
    int index = str.indexOf(",");
    cpu = str.substring(0, index);
    ram = str.substring(index + 1, str.length());
    Serial.print(cpu + " - " + ram);
    analogWrite(5,map(cpu.toInt(),0,100,0,255));
    analogWrite(10,map(ram.toInt(),0,100,0,255));
  }

}