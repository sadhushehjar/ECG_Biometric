void setup() {      
  // initialize the serial communication:
  Serial.begin(9600);
  pinMode(14, INPUT); // Setup for leads off detection LO +
  pinMode(12, INPUT); // Setup for leads off detection LO - 
}
//
const unsigned long READ_PERIOD = 4000;  // 4000 us: 250 Hz
unsigned long prev_micros = 0;
void loop() {
  unsigned long curr_micros = micros();
 if(curr_micros-prev_micros>=READ_PERIOD)
 {
      Serial.sprintf("%d,%lu \n",analogRead(A0),curr_micros);
      prev_micros = curr_micros;
  }  
}
