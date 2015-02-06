using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Kinect;
using System.Threading;
using System.IO.Ports;

namespace BodySensor
{
    public class Program
    {
        public static int FRAME_DURATION = 100;
        public static int X_PIXELS = 3;
        public static int Y_PIXELS = 3;
        public static double PIXEL_WIDTH = 1; // Assume 5 px/m => 20px/4m
        public static byte START_OF_MESSAGE = 0; // Assume 5 px/m => 20px/4m

        static void CalculatePixels(Skeleton[] skeletons, int[,] pixels)
        {
            ZeroPixels(pixels);

            foreach (Skeleton skeleton in skeletons)
            {
                if (skeleton.TrackingState == SkeletonTrackingState.PositionOnly || skeleton.TrackingState == SkeletonTrackingState.Tracked)
                {
                    AccumulatePixels(pixels, skeleton.Position);
                }
            }
        }

        static void ZeroPixels(int[,] pixels)
        {
            for (int x = 0; x < X_PIXELS; x++)
            {
                for (int y = 0; y < Y_PIXELS; y++)
                {
                    pixels[x,y] = 0;
                }
            }
        }

        public static void AccumulatePixels(int[,] pixels, SkeletonPoint position)
        {
            // Check if the skeleton is within the FOV that we're covering
            //if (position.X < 2 && position.X > -2 &&
            //    position.Y < 2 && position.Y > -2)
            //{
                for (int x = 0; x < X_PIXELS; x++)
                {
                    // Shift the origin to the mid-point of the array, and scale x to pixel width.
                    double pixel_x = (x - X_PIXELS/2) * PIXEL_WIDTH;
                    for (int y = 0; y < Y_PIXELS; y++)
                    {
                        double pixel_y = -(y - Y_PIXELS/2) * PIXEL_WIDTH;
                        double d_x = pixel_x - position.X;
                        double d_y = pixel_y - position.Y;

                        // TODO: trim pixels to <128 on first side iteration?
                        pixels[x, y] = Gaussian(d_x, d_y, 0.5);
                    }
                }
            //}
        }

        public static int Gaussian(double x, double y)
        {
            return Gaussian(x, y, 1);
        }

        // Calculate the gaussian for a point relative to the origin.
        // Returns an int in the range 0-127 such that the maximum
        public static int Gaussian(double x, double y, double sigma)
        {

            int g = (int)(255 * Math.Exp(-(x * x / (2 * Math.Pow(sigma, 2)) + y * y / (2 * Math.Pow(sigma, 2)))));
            //Console.WriteLine("G(" + x + "," + y + ") = " + g);
            return g;
        }

        // Print pixel grayscale in ASCII
        // Adapted from http://larc.unt.edu/ian/art/ascii/shader/
        static void PrintPixels(int[,] pixels)
        {
            Console.OutputEncoding = System.Text.Encoding.Unicode;
            Console.Clear();
            for (int y = 0; y < Y_PIXELS; y++)
            {
                for (int x = 0; x < X_PIXELS; x++)
                {
                    Console.Write(String.Format("{0,4} ", pixels[x,y]));
                }
                Console.WriteLine();
            }
            Console.WriteLine();Console.WriteLine();Console.WriteLine();
            for (int y = 0; y < Y_PIXELS; y++)
            {
                for (int x = 0; x < X_PIXELS; x++)
                {
                    int pixel = pixels[x,y];
                    if (pixel > 245)
                    {
                        Console.Write('.');
                    }
                    else if (pixel > 237)
                    {
                        Console.Write(':');
                    }
                    else if (pixel > 218)
                    {
                        Console.Write('*');
                    }
                    else if (pixel > 197)
                    {
                        Console.Write('|');
                    }
                    else if (pixel > 181)
                    {
                        Console.Write('V');
                    }
                    else if (pixel > 169)
                    {
                        Console.Write('X');
                    }
                    else if (pixel > 158)
                    {
                        Console.Write('H');
                    }
                    else if (pixel > 144)
                    {
                        Console.Write('M');
                    }
                    else
                    {
                        Console.Write('\u2588');
                    }
                }
                Console.WriteLine();
            }
        }

        static void SerialPixels(int[,] pixels, SerialPort port)
        {
            byte[] valByte = new Byte[X_PIXELS * Y_PIXELS + 1];
            valByte[0] = START_OF_MESSAGE;
            for (int y = 0; y < Y_PIXELS; y++)
            {
                for (int x = 0; x < X_PIXELS; x++)
                {
                    byte val = Convert.ToByte(pixels[x, y] / 3);
                    if (val < 1)
                    {
                        val = 1;
                    }
                    else if (val > 90)
                    {
                        val = 90;
                    }
                    // Add 1-byte offset for start-of-message.
                    valByte[y * Y_PIXELS + x + 1] = val;
                }
            }

            Console.WriteLine("Sending: " + valByte);
            port.Write(valByte, 0, valByte.Length);

            try
            {
                Console.WriteLine(String.Format("Read {0} bytes", port.ReadExisting()));
            }
            catch (TimeoutException) { }
        }

        static int Main(string[] args)
        {
            string port_name = "COM3";
            if (args.Length > 0)
            {
                port_name = args[0];
            }

            Console.WriteLine("Using serial port " + port_name);
            SerialPort port = new SerialPort(port_name, 9600);
            port.ReadTimeout = 10;
            port.Open();

            KinectSensorCollection sensors = KinectSensor.KinectSensors;

            foreach (KinectSensor sensor in KinectSensor.KinectSensors)
            {
                Console.WriteLine("Evaluating sensor " + sensor);
                if (sensor.Status == KinectStatus.Connected)
                {
                    Console.WriteLine("Sensor " + sensor + " is connected.");
                }
            }

            if (sensors.Count == 0)
            {
                Console.WriteLine("No sensors found.");
                return 1;
            }

            KinectSensor sensorOne = sensors[0];

            if (sensorOne.Status != KinectStatus.Connected)
            {
                Console.WriteLine("Sensor not connected.");
                return 1;
            }

            sensorOne.SkeletonStream.Enable();

            int maxSkeletons = sensorOne.SkeletonStream.FrameSkeletonArrayLength;
            Console.WriteLine("Can track this many skeletons: " + maxSkeletons);
            sensorOne.Start();
            SkeletonFrame frame;
            Skeleton[] skeletons = new Skeleton[maxSkeletons];
            int[,] pixels = new int[X_PIXELS, Y_PIXELS];

            while (true) 
            {
                DateTime startTime = DateTime.Now;
                frame = sensorOne.SkeletonStream.OpenNextFrame(100);

                if (frame != null)
                {
                    //Console.WriteLine("Processing frame " + frame.FrameNumber);
                    frame.CopySkeletonDataTo(skeletons);

                    //Console.WriteLine("Processing skeleton " + skeleton.TrackingId);
                    ////Console.WriteLine("Skeleton instance: " + skeleton);
                    //Console.WriteLine(String.Format("TrackingState: {0}, Joints: {1}", skeleton.TrackingState, skeleton.Joints));
                    CalculatePixels(skeletons, pixels);
                    PrintPixels(pixels);
                    Console.WriteLine();
                    Console.WriteLine();
                    foreach (Skeleton skeleton in skeletons)
                    {
                        if (skeleton.TrackingState == SkeletonTrackingState.PositionOnly || skeleton.TrackingState == SkeletonTrackingState.Tracked)
                        {
                            Console.WriteLine(String.Format("Position: x {0}, y {1}, z {2}", skeleton.Position.X, skeleton.Position.Y, skeleton.Position.Z));
                        }
                        
                    }

                    SerialPixels(pixels, port);
                    
                    frame.Dispose();
                }

                TimeSpan timeDelta = DateTime.Now - startTime;
                int timeStepRemaining = (FRAME_DURATION - timeDelta.Milliseconds) > 0 ? (FRAME_DURATION - timeDelta.Milliseconds) : 0;
                if (timeStepRemaining > 0)
                {
                    Thread.Sleep(timeStepRemaining);
                }
            }
        }
    }
}
