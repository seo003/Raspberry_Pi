int Output = 2;

void setup() {
  Serial.begin(9600);
  pinMode(Output, INPUT);

}

void loop() {
  int SensorVal = digitalRead(Output);
  
  Serial.println(SensorVal);
  delay(500);
}
