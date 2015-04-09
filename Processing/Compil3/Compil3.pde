/* --------------------------------------------------------------------------
 * SimpleOpenNI User Test
 * --------------------------------------------------------------------------
 * Processing Wrapper for the OpenNI/Kinect 2 library
 * http://code.google.com/p/simple-openni
 * --------------------------------------------------------------------------
 * prog:  Max Rheiner / Interaction Design / Zhdk / http://iad.zhdk.ch/
 * date:  12/12/2012 (m/d/y)
 * ----------------------------------------------------------------------------
 */

import toxi.geom.*;
import SimpleOpenNI.*;
import processing.video.*;
import processing.net.*;




SimpleOpenNI  context;
Client myClient;
Fluid fluid;

color[] userClr = new color[] { 
  color(255, 0, 0), 
  color(0, 255, 0), 
  color(0, 0, 255), 
  color(255, 255, 0), 
  color(255, 0, 255), 
  color(0, 255, 255)
};
int[] membres = { 
  0, 7, 6
};

ArrayList tileCollection= new ArrayList();
ArrayList<PVector> pointCollection = new ArrayList();

boolean userDetected = false;
boolean userDetectedNow = false;
boolean reset = false;
boolean kinect = true;

int swidth = 640;
int sheight = 480;

int lC;
int lL;
int l;
int marginCo;
int marginHB;

int rows = 8;
int cols = 19;

int screensaver = 0;
int NUM_SCREENSAVERS = 4;
int kinectApp = 1;
int NUM_KINECT_APPS = 2;
  // Allows to switch across different interactive animations
  // 0 : MeetWalll
  // 1 : Fluid

int actionRadius = 100;

byte[] byteBuffer=  new byte[cols * rows];
float[] tileHeight=  new float[cols * rows];

void setup()
{
  size(640, 480);

 
 
   // myClient = new Client(this,"192.168.2.1",9999);
  context = new SimpleOpenNI(this);
  fluid = new Fluid();
  KiSetup();
  ScreenSaverSetUp();
  tileSetUp();
  ScreenSaverReset();
}

void draw() {

 background(0);

  
  
 if (keyPressed) {
    if (key == 's') {
      screensaver = (screensaver + 1) % NUM_SCREENSAVERS;
      println((screensaver + 1) % NUM_SCREENSAVERS);
      ScreenSaverReset();
   }
    if (key == 'k') {
      kinectApp = (kinectApp + 1) % NUM_KINECT_APPS;
      println((kinectApp + 1) % NUM_KINECT_APPS);      
   }
 } 
  

if (kinect) {
  context.update();
   image(context.userImage(), 0, 0);


  // draw the skeleton if it's available
  int[] userList = context.getUsers();
  /* Logic: 
  userDetected = was there a user in the previous loop
  userDetectedNow = is there a user in the current loop
 */

  userDetectedNow = (userList.length > 0);
  
  if (!userDetectedNow) {
    // No user now
    if (userDetected) {
      // User left
      userDetected = false;
      println("User left, resetting screensaveri and switching to the next one");
      reset(); // reset the tiles
      screensaver = (screensaver + 1) % NUM_SCREENSAVERS;
       ScreenSaverReset();
    } else { 
      //  No users for several loops, activate screenSaver
      ScreenSaverloop();

   //  println("screensaverloop");
    }
  } else {
    // There is a user now
      if (!userDetected) {
        // The user is fresh
        println("New user just walked in, activating interactive Kinect app");
        reset();
        kinectApp = (kinectApp + 1) % NUM_KINECT_APPS;
           println(kinectApp);
        userDetected = true;
    } else {
      // The user was here before, keep running the Kinect anim
      // println("Keep running Kinect");
      switch(kinectApp) {
      case 0: 
        kiLoop(userList);
        kiComputeAngles();
        break;
      case 1:
        fluid.handleKinect(context);
        break;
      }
    }
  }
} else{
 // Kinect is not here / not working
  ScreenSaverloop();  
}

tileLoop();
pointCollection.clear(); 
}

 /*if (frameCount%30==0){
   println("sending at "+ frameCount); 
 if(!myClient.active()){
        println("CLIENT GOT DISCONNECTED");
        myClient = new Client(this,"192.168.2.1", 9999);
    } 
      myClient.write(byteBuffer);

}*/

