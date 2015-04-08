void tileSetUp() {
  lC = swidth/cols;
  lL = sheight/rows;
  l = min(lC, lL);
  marginCo = (swidth%(l*cols))/2;
 // println(l);
  marginHB = (sheight%(l*rows))/2;
  //  println(marginHB);
  rectMode(RADIUS);

  //tile position definition 
  for (int j = 0; j<cols; j++) {
    for (int i = 0; i<rows; i++) {
      Vec3D myVec  =  new Vec3D(j*(l)+l/2+marginCo, i*l+l/2+marginHB, 0);
      tileCollection.add(myVec);
    }
  }
}

void tileLoop() {


  for (int j=0; j<rows*cols; j++) {
    Vec3D myv=(Vec3D) tileCollection.get(j);
    stroke(255);
    fill(255, 20, 147);
    rect(myv.x, myv.y, l/2, tileHeight[j]);
    fill(255);
    textAlign(CENTER);
    text(j, myv.x, myv.y);   //  print(byteBuffer+"*");
  }
}


