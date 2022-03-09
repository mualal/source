using System;

namespace Fibonacci
{
    class Program
    {
        static void Main(string[] args)
        {
            int position;
            Console.Write("Enter Fibonacci number position: ");
            try
            {
                position = Convert.ToInt32(Console.ReadLine());
            }
            catch(FormatException)
            {
                Console.WriteLine("Only integer numbers are accepted");
                position = 0;
                System.Environment.Exit(0);
            }
            
            double golden_sec = (1 + Math.Sqrt(5)) / 2;

            double fibonacci_num = (Math.Pow(golden_sec, position) - Math.Pow(-golden_sec, -position)) / 
            (2 * golden_sec - 1);
            
            Console.WriteLine(Convert.ToInt64(fibonacci_num));
        }
    }
}
