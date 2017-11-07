using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
namespace Calc.Data
{
    using DataSets = List<Tuple<List<double>, double>>;
    public class Range 
    {
        public int[] C;
        public Range(int N)
        {
            C = new int[N];
            var it=0;
            while (it < N)
            {
                C[it] = 1;
                it += 1;
            }
        }

        public Range(int begin, int end)
        {
            if (end < begin) return;
            var N = end - begin;
            C = new int[N];
            var it = 0;
            while (it < N)
            {
                C[it] = it;
                it += 1;
            }
        }

        public static List<int> Stream(int N) => new Range(N).C.ToList();
        public static List<int> Stream(int begin, int end) => new Range(begin, end).C.ToList();
    }
    public static class Data
    {
        static double Pi = 3.14159;
        public static DataSets sample(int size, Func<List<double>, double> f)
        {
            

            var rnd = new Random();
            return Range.Stream(size)
                                  .Select(a => a * rnd.NextDouble())
                                  .Select(_base => new List<double>{Math.Cos(2*Pi* _base), Math.Sin(2*Pi* _base)})
                                  .Select(data => new Tuple<List<double>, double>(data, f(data)))
                                  .ToList();

            

        }
        public static void Test(int size)
        {
            var rnd = new Random();
            var s = new Range(size).C.Select(a => a * rnd.NextDouble()).ToList();
            s.ForEach(Console.WriteLine);
        }
    }

}

