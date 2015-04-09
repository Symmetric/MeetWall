void KiSetup() {
  if (context.isInit() == false) {
    println("Can't init SimpleOpenNI, maybe the camera is not connected!"); 
    kinect=false;
    // exit();
  }

  context.setMirror(true);
  // enable depthMap generation 
  context.enableDepth();
  // enable skeleton generation for all joints
  context.enableUser();
}

void kiComputeAngles() {

  for (int j=0; j<rows*cols; j++) {
    float mindist = 10000000;  
    Vec3D myv=(Vec3D) tileCollection.get(j);

    for (int i = 0; i < pointCollection.size (); i++) {  
      PVector mypos=pointCollection.get(i);
      Vec3D laface0= new Vec3D(mypos.x, mypos.y, 0);
      float dist= laface0.distanceTo(myv);
      if (dist<mindist) {
        mindist=dist; //keeping closest face to process
      }
    }


    if (mindist<actionRadius) { // acting only on the tiles in the actionRadius.
      byteBuffer[j]=byte(int((1-(mindist/actionRadius))*90));
      tileHeight[j]=mindist*(l/2)/actionRadius;


      //  print (int(1/mindist*actionRadius/90),"    ");
    } else { //doing nothing if out of actionRadius
      tileHeight[j]=l/2;
      byteBuffer[j]=byte(0);
    }
  }
}
void kiLoop(int[] userList) {
  //imageMode(CENTER);
 
  for (int i=0; i<userList.length; i++) {
    if (context.isTrackingSkeleton(userList[i])) {
      KiUser myKiUser = new KiUser(userList[i]);
      // draw skeleton
      myKiUser.KidrawSkeleton();
      stroke(255, 0, 0);
      noFill();
      // get position of head (more smooth)
      myKiUser.KiGetPosition(membres[0], 2, 0); 
      // get position of hands (less smooth)
      myKiUser.KiGetPosition(membres[1], 5, 1); 
      myKiUser.KiGetPosition(membres[2], 5, 2); 

      for (int j=0; j<3; j++) {
        pointCollection.add(myKiUser.position2d[j]);
      }
    }
  }
}
// -----------------------------------------------------------------
// SimpleOpenNI events

void onNewUser(SimpleOpenNI curContext, int userId) {
  println("onNewUser - userId: " + userId);
  println("\tstart tracking skeleton");
  curContext.startTrackingSkeleton(userId);
}

void onLostUser(SimpleOpenNI curContext, int userId) {
  println("onLostUser - userId: " + userId);
}

void onVisibleUser(SimpleOpenNI curContext, int userId) {
  //println("onVisibleUser - userId: " + userId);
}

