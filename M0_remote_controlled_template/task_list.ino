Array ts;
Array2 command, nr, ex;

void initArrays()
{
initArray(&ts, 5);
initArray2(&command, 5);
initArray2(&nr, 5);
initArray2(&ex, 5);
}


void insertTask(uint32_t time2, uint8_t cmd, uint8_t param){
  
    insertArray(&ts, time2);
    insertArray2(&command, cmd);
    insertArray2(&nr, param);
    insertArray2(&ex, 0);
    
}

void printTasklist(){


    for(int i=0;i<ts.size;i++)
    {
      if (ts.array[i]==0)
        break;
      Serial.print("Task no. ");
      Serial.print(i+1);
      Serial.print(": ");
      Serial.print(ts.array[i]);
      Serial.print(" ");
      Serial.print(command.array[i]);
      Serial.print(" ");
      Serial.print(nr.array[i]);
      Serial.print("\n");
    }

    Serial.print("Free RAM = ");
    Serial.println(freeMemory(), DEC);
  
}

void runAvailTasks(){
  //Run all task with a timestamp before current time

  for(int i=0;i<ts.size;i++) 
  {
    if (ts.array[i]==0)
      break;
    if (ex.array[i]==0 && ts.array[i]<getTimeInSeconds())
    {
    runTaskOnce(command.array[i],nr.array[i]);
    ex.array[i] = 1;
    }
    
  }
 
 
}
