volatile bool inFlag=false, outFlag=false;
volatile long t, t2, t3, t4;
void out(){
  t = millis();
  t4 = millis() - t3;
  if (t4 < 50 || t4 > 150)
  {
    inFlag = false;
  }
  if (inFlag) {
    if (count>0)
    count--;
    inFlag=false;
  } else if (t4>50) {
    outFlag=true;
  }
}

void in(){
  t3 = millis();
  t2 = millis() - t;
  if (t2 > 150 || t2 < 60)
  {
  outFlag = false;
  }
  if (outFlag) {
    count++;
    outFlag=false;
  } else if(t2>50) {
    inFlag=true;
  }
}
