using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
namespace Calc.Data
{
    using DataSets = List<(List<double>, double)>;
  
    public static class Data
    {
        static double Pi = 3.14159;
        public static DataSets sample(int size, Func<List<double>, double> f)
        {
            

            var rnd = new Random();
            return Enumerable.Range(0, size)
                                  .Select(a => { return (rnd.NextDouble(), rnd.NextDouble()); } ) // R
                                  .Select(_base =>
                                        {
                                            var theta = 2 * Pi * _base.Item1;
                                            var x = _base.Item2 * Math.Cos(theta);
                                            var y = _base.Item2 * Math.Sin(theta);
                                            return new List<double> { x, y };
                                        })
                                  .Select(data =>(data, f(data)))
                                  .ToList();

            

        }
        public static void Test(int size)
        {
            var rnd = new Random();
            var s = Enumerable.Range(0, size).Select(any => 1 * rnd.NextDouble()).ToList();
            s.ForEach(Console.WriteLine);
        }
    }

}

