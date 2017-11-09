using System;
using System.Collections.Generic;
using Calc.Data;
using Calc.Perceptron;
using Calc.Genetic;
using System.Linq;
using System.IO;
namespace Proj.Exec
{
    using Vector = List<double>;
    public class Program
    {
        public static void Perceptron()
        {
            var datas = Data.sample(100, args => Math.Sign(2 * args[0] + args[1]) );
            Console.WriteLine(datas.Count);
            // datas.ForEach(data => Console.WriteLine(data.Item1[0] + " " + data.Item1[1] + " : " + data.Item2));

            var perceptron = new Perceptron
            {
                Weight = datas[0].Item1,
                Bias = 0.3
            };
            Enumerable.Range(0, 3).ToList().ForEach(i =>
                datas.ForEach(data => { perceptron.Renew(data.Item1, data.Item2); }));


            
            using (StreamWriter s = File.CreateText("./data.txt"))
            {
                datas.ForEach(data => s.WriteLine(data.Item1[0]+","+data.Item1[1]+","+data.Item2));
            }

            using (StreamWriter s = File.CreateText("./predict.txt"))
            {
                datas.Select(data => perceptron.Forward(data.Item1)).ToList().ForEach(s.WriteLine);
            }
            using (StreamWriter s = File.CreateText("./params.txt"))
            {
                perceptron.Weight.ForEach(s.WriteLine);
                s.WriteLine(perceptron.Bias);
            }
        }
        public static void Genetic()
        {
            Func<List<bool>, double> score = list => (list[0] == true ? 1 : 0) + (list[1] == false ? 1 : 0);

            var gene = new Genetic(
                100,
                7,
               score);
            Console.WriteLine(
            String.Join(",", gene.NaturalSelection().Select(a => a.ToString())));
        }

        public static void Main(String[] args)
        {
            
            if (args.Length == 1)
            {
                var prog = args[0];
                if (prog == "genetic")
                {
                    Genetic();
                }
                else if (prog == "perceptron")
                {
                    Perceptron();
                }
                else
                {
                    Console.WriteLine("Unsolved Program Initial Argument.");
                }
            }
            else
            {
                Perceptron();
            }

        }

       
    }

   

}