using System;
using System.Collections.Generic;
using Dr.Perceptron;
using System.Linq;
namespace Dr
{
    using Vector = List<double>;
    using DataSets = List<ValueTuple<List<double>, double>>;
    class Program
    {
        static Vector Vector(double a, double b) => new Vector { a, b };

        static void Main(string[] args)
        {
            var perceptron = new Percepron
            {
                Weight = new Vector { 0.5, 0.2 },
                Bias = 0.5
            };

            foreach (var i in (new List<int> { 0, 0, 0, 0 }))
            {
                new DataSets {
                (Vector(1,1), -1),
                (Vector(3,2), -1),
                (Vector(-1,-1), 1),
                (Vector(-1,-2), 1),
                (Vector(-1,-2),  1),
                (Vector(-2,-1.2), 1) }.ForEach(data => perceptron.Renew(data.Item1, data.Item2));

            }


            new DataSets {
                (Vector(1,1), -1),
                (Vector(3,2), -1),
                (Vector(-1,-1), 1),
                (Vector(-1,-2), 1),
                (Vector(-1,-2),  1),
                (Vector(-2,-1.2), 1) }.Select(data => perceptron.Forward(data.Item1))
                .ToList().ForEach(Console.WriteLine);


        breaker:;


        }
    }
}
