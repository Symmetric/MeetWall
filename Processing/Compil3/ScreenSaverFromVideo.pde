
Movie myMovie0, myMovie1, myMovie2, myMovie3;


//ArrayList tileCollection= new ArrayList();
color c[]= new color[cols*rows];
float r[]= new float[cols*rows];


//Called every time a new frame is available to read
void movieEvent(Movie m) {
  if (m == myMovie0) {
    myMovie0.read();
  } else if (m == myMovie1) {
    myMovie1.read();
  } else if (m == myMovie2) {
    myMovie2.read();
  } else if (m == myMovie3) {
    myMovie3.read();
  }
}


void ScreenSaverSetUp() {

  myMovie0 = new Movie(this, "0.mov"); //HelloWorld
  myMovie1 = new Movie(this, "1.mov"); //Tetris
  myMovie2 = new Movie(this, "2.mov"); //Amlgam Labs
  myMovie3 = new Movie(this, "3.mov"); //WavePropagation
}

void ScreenSaverReset() {

  switch(screensaver) {
  case 0: 
    myMovie0.play();
    myMovie1.stop();
    myMovie2.stop();
    myMovie3.stop();
    break;

  case 1:
    myMovie1.play();
    myMovie0.stop();
    myMovie2.stop();
    myMovie3.stop();
    break;

  case 2:
    myMovie2.play();
    myMovie0.stop();
    myMovie1.stop();
    myMovie3.stop();
    break;

  case 3:
    myMovie3.play(); 
    myMovie0.stop();
    myMovie1.stop();
    myMovie2.stop();
    break;
  }
}
void ScreenSaverloop() {

  switch(screensaver) {
  case 0: 
    image(myMovie0, 0, 112, 640, 256);
    break;
  case 1:
    image(myMovie1, 0, 112, 640, 256);
    break;
  case 2:
    image(myMovie2, 0, 112, 640, 256);
    break;
  case 3:
    image(myMovie3, 0, 112, 640, 256);
    break;
  }


  for (int j=0; j< (rows)*(cols); j++) {
    Vec3D myv=(Vec3D) tileCollection.get(j); 
    c[j]=get(int(myv.x), int(myv.y));
    r[j] = 255-red(c[j]);
  }

  for (int j=0; j< (rows)*(cols); j++) {
    Vec3D myv=(Vec3D) tileCollection.get(j); 

    tileHeight[j]=(r[j]/255)*l/2;
    byteBuffer[j]=byte(int((1-(r[j]/255))*90));
  }
  //println(byteBuffer);
}

