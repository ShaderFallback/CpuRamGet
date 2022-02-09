String str;
String cpu;
String ram;

int freq = 2000;    // 频率
int channel_cpu = 0;    // 通道
int channel_ram = 1;    // 通道
int resolution = 8;   // 分辨率
void setup() {
  Serial.begin(115200);
  ledcSetup(channel_cpu, freq, resolution);
  ledcSetup(channel_ram, freq, resolution);
  ledcAttachPin(2, channel_cpu);
  ledcAttachPin(4, channel_ram);
}
void loop() {
  while (!Serial.available());

  String str = Serial.readString();
  //疑惑：arduino uno 貌似不用去掉\n,但esp32则不行
  str.trim();

  if (str.equals("handshake")) {
    Serial.println("handshake");
  } else {
    int index = str.indexOf(",");
    cpu = str.substring(0, index);
    ram = str.substring(index + 1, str.length());
    Serial.print(cpu + " - " + ram);
    //使用ledcWrite实现pwm
    ledcWrite(channel_cpu, map(cpu.toInt(),0,100,0,255));  
    ledcWrite(channel_ram, map(ram.toInt(),0,100,0,255));
  }

}