using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Microsoft.Kinect;


namespace UnitTestProject1
{
    [TestClass]
    public class UnitTestBodySensor
    {
        [TestMethod]
        public void TestGaussian()
        {
            Assert.AreEqual(BodySensor.Program.Gaussian(0, 0), 255);
            Assert.AreEqual(BodySensor.Program.Gaussian(1.0, 0.0), BodySensor.Program.Gaussian(0.0, 1.0));
            Assert.AreEqual(BodySensor.Program.Gaussian(1.0, 0.0), BodySensor.Program.Gaussian(-1.0, 0.0));
            Assert.IsTrue(BodySensor.Program.Gaussian(1.0, 1.0) < BodySensor.Program.Gaussian(1.0, 0.0));
        }

        SkeletonPoint BuildPoint(double x, double y)
        {
            SkeletonPoint point = new SkeletonPoint();
            point.X = 1;
            point.Y = 0;

            return point;
        }

        [TestMethod]
        public void TestCalculate()
        {
            int[,] pixels10 = new int[BodySensor.Program.X_PIXELS, BodySensor.Program.Y_PIXELS];
            BodySensor.Program.AccumulatePixels(pixels10, BuildPoint(1.0, 0.0));
            int[,] pixels01 = new int[BodySensor.Program.X_PIXELS, BodySensor.Program.Y_PIXELS];
            BodySensor.Program.AccumulatePixels(pixels01, BuildPoint(0.0, 1.0));
              
            Assert.AreNotEqual(pixels10, pixels01);
        }
    }}
