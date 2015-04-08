import msafluid.*;

final float FLUID_WIDTH = 19;
final float FLUID_HEIGHT = 8;
float invWidth, invHeight;    // inverse of screen dimensions
float aspectRatio, aspectRatio2;
float lastMillis = 0;
PVector FluidNewHandPosFlat, FluidNewHandPos, FluidOldPos;

MSAFluidSolver2D fluidSolver;
PImage imgFluid;

boolean drawFluid = true;
boolean renderUsingVA = true;

class Fluid {
  Fluid() {
    invWidth = 1.0f / 960;
    invHeight = 1.0f / 384;
    aspectRatio = width * invHeight;
    aspectRatio2 = aspectRatio * aspectRatio;
    // create fluid and set options
    fluidSolver = new MSAFluidSolver2D((int)(FLUID_WIDTH), 
    (int)(FLUID_HEIGHT));

    //TODO adjust parameters
    // Fade: speed at which the fluid goes back to black
    // DeltaT: time delta for simulation: smaller = more precise but more hungry
    // Visc: viscosity, higher means thicker fluid
    fluidSolver.enableRGB(true).setFadeSpeed(0.01).setDeltaT(0.5).setVisc(0.001);

    // create image to hold fluid picture
    imgFluid = createImage(fluidSolver.getWidth(), 
    fluidSolver.getHeight(), RGB);
    initTUIO();

    FluidOldPos = new PVector(0, 0, 0);
    FluidNewHandPos = new PVector(0, 0, 0);
    FluidNewHandPosFlat = new PVector(0, 0, 0);
  }

  void userMoved(PVector oldPos, PVector newPos) {
    float normX = newPos.x * invWidth;
    float normY = newPos.y * invHeight;
    float dt = millis() - lastMillis;
    float velX = (newPos.x - oldPos.x) * invWidth / dt;
    float velY = (newPos.y - oldPos.y) * invHeight / dt;
    lastMillis = millis();
    //println("Velocity " + velX + " " + velY + " " + dt);
    addForce(normX, normY, velX, velY);
  }

  void updateCells() {
    updateTUIO();
    fluidSolver.update();
    if (drawFluid) {
      for (int i = 0; i < fluidSolver.getNumCells (); i++) {
        int d = 2;
        //imgFluid.pixels[i] = color(fluidSolver.r[i] * d, fluidSolver.g[i] * d, fluidSolver.b[i] * d);
        imgFluid.loadPixels();
        float grayscale = RGBToGrayScale(fluidSolver.r[i] * d, fluidSolver.g[i] * d, fluidSolver.b[i] * d);
        imgFluid.pixels[i] = color(grayscale);
        // If you want to display a background image, might conflict
        imgFluid.updatePixels(); 
        //tint(255, 126); 
        image(imgFluid, 0, 0, 40, 40);


        // Update tiles and buffer
        if ( i < rows * cols) {

          tileHeight[i] = converToTileHeight(grayscale);
          byteBuffer[i] = convertToTileAngle(grayscale);
        }

        //TODO: Render the tiles here with rectangles
      }
    }
  }

  byte convertToTileAngle(float grayscale) {
    return byte(int(90 * grayscale));
  }

  float converToTileHeight(float grayscale) {
    return (l * grayscale) / 2.0;
  }

  // add force and dye to fluid, and create particles
  void addForce(float x, float y, float dx, float dy) {
    float speed = dx * dx  + dy * dy * aspectRatio2;    // balance the x and y components of speed with the screen aspect ratio

    if (speed > 0) {
      if (x<0) x = 0; 
      else if (x>1) x = 1;
      if (y<0) y = 0; 
      else if (y>1) y = 1;

      float colorMult = 5;
      float velocityMult = 30.0f;

      int index = fluidSolver.getIndexForNormalizedPosition(x, y);

      color drawColor;

      colorMode(HSB, 360, 1, 1);
      float hue = ((x + y) * 180 + frameCount) % 360;
      drawColor = color(hue, 1, 1);
      colorMode(RGB, 1);  

      fluidSolver.rOld[index]  += red(drawColor) * colorMult;
      fluidSolver.gOld[index]  += green(drawColor) * colorMult;
      fluidSolver.bOld[index]  += blue(drawColor) * colorMult;
      fluidSolver.uOld[index] += dx * velocityMult;
      fluidSolver.vOld[index] += dy * velocityMult;
    }
    colorMode(RGB, 255);
  }

  float RGBToGrayScale(float R, float G, float B) {
    float gamma = 1.0;
    float res = .2126 * pow(R / 1.0, gamma) + .7152 * pow(G / 1.0, gamma) + .0722 * pow(B / 1.0, gamma);
    return res;
  }

  void handleKinect(SimpleOpenNI context) {
    //image(context.userImage(), 0, 0);

    int[] userList = context.getUsers();
    if (userList.length > 0) {
      if (context.isTrackingSkeleton(userList[0])) {
        context.getJointPositionSkeleton(userList[0], 6, FluidNewHandPos);
        context.convertRealWorldToProjective(FluidNewHandPos, FluidNewHandPosFlat);
        userMoved(FluidOldPos, FluidNewHandPosFlat);	    
        FluidOldPos.x = FluidNewHandPosFlat.x;
        FluidOldPos.y = FluidNewHandPosFlat.y;
        fill(255);
        ellipse(FluidOldPos.x, FluidOldPos.y, 50, 50);
      }
    }
    updateCells();
  }
};

