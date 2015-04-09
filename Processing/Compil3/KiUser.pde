class KiUser {
  //GLOBAL VARIABLES= give a value and initialise variables

  PVector[] position = {
    new PVector(0, 0, 0), new PVector(0, 0, 0), new PVector(0, 0, 0)
  };
  PVector[] position2d = {
    new PVector(0, 0, 0), new PVector(0, 0, 0), new PVector(0, 0, 0)
  };

  int user=0;

  //CONSTRUCTOR = where you specifie how to build your class
  KiUser/*name of class*/(int _user) {

    user = _user;
  }


  //FUNCTIONS 


  void KiGetPosition(int limb, int smooth, int num) {

    PVector NewPosition2d = new PVector();
    // to get the 3d joint data
    

    context.getJointPositionSkeleton(user, limb, position[num]);
    context.convertRealWorldToProjective(position[num], NewPosition2d);

    float dist=PVector.dist(NewPosition2d, position2d[num]);
    //Smoothing movement
    if (dist<smooth && position2d[num].mag()==0) {
      position2d[num] = NewPosition2d;
    } else {
      NewPosition2d.sub(position2d[num]);

      if (dist<400) {
        NewPosition2d.setMag(smooth);
      }
      position2d[num].add(NewPosition2d);
    }
    ellipse(position2d[num].x, position2d[num].y, 50, 50);
  }

  // draw the skeleton with the selected joints
  void KidrawSkeleton()
  {
    context.drawLimb(user, SimpleOpenNI.SKEL_HEAD, SimpleOpenNI.SKEL_NECK);
    context.drawLimb(user, SimpleOpenNI.SKEL_NECK, SimpleOpenNI.SKEL_LEFT_SHOULDER);
    context.drawLimb(user, SimpleOpenNI.SKEL_LEFT_SHOULDER, SimpleOpenNI.SKEL_LEFT_ELBOW);
    context.drawLimb(user, SimpleOpenNI.SKEL_LEFT_ELBOW, SimpleOpenNI.SKEL_LEFT_HAND);

    context.drawLimb(user, SimpleOpenNI.SKEL_NECK, SimpleOpenNI.SKEL_RIGHT_SHOULDER);
    context.drawLimb(user, SimpleOpenNI.SKEL_RIGHT_SHOULDER, SimpleOpenNI.SKEL_RIGHT_ELBOW);
    context.drawLimb(user, SimpleOpenNI.SKEL_RIGHT_ELBOW, SimpleOpenNI.SKEL_RIGHT_HAND);
  }
}

