using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Calc.Data;
namespace Calc.Genetic
{
    using Chromosome = List<Boolean>;
    using Popularity = List<List<Boolean>>;
    class Genetic
    {
        public Popularity Popularity;
        public int PopuSize;
        

        public Chromosome BestFitter;
        public int ChromosomeLength;

        public Func<double, int> GetCrossOverHead;
        public Func<Chromosome, double> Score;

        public double MutateRatio;
        public double CrossoverRatio;

        private double split;

        private int ChromosomeCompare(Chromosome c1, Chromosome c2) { 
            return - Score(c1).CompareTo(Score(c2));
        }

        static Random rnd = new Random();
        public static Chromosome GenChromosome(int size)
        {
            return Range.Stream(size).Select(i => rnd.Next() % 2 == 0).ToList();
        }

        public Genetic(int popuSize, 
                       int chromosomeLength, 
                       Func<Chromosome, double> score,
                       double crossoverRatio = 0.1, double mutateRatio = 0.05)
        {
            MutateRatio = mutateRatio;
            CrossoverRatio = crossoverRatio;
            ChromosomeLength = chromosomeLength;
            PopuSize = popuSize;
            split = 1.0 / chromosomeLength;
            Score = score;
            GetCrossOverHead = prob => (int)(prob / split);
            Popularity = Range.Stream(popuSize).Select(i => ChromosomeLength).Select(GenChromosome).ToList();
        }

        public void Mutate(Chromosome chromosome)
        {

            Range.Stream(ChromosomeLength).ForEach(i =>
            { 
                if (MutateRatio > rnd.NextDouble())
                    chromosome[i] = !chromosome[i];
                });
        }

        public void Crossover(Chromosome c1, Chromosome c2) {

            var headIdx = GetCrossOverHead(rnd.NextDouble());
            Range.Stream(headIdx).ForEach(i =>
                {
                    var tmp = c1[i];
                    c1[i] = c2[i];
                    c2[i] = tmp;
                });
        }


        public void evolution(int number){
            Console.WriteLine($"the {number}-th iter");

            Chromosome last = null;
            foreach(Chromosome c in Popularity)
            {
                Mutate(c);
                if (last != null)
                {
                    Crossover(last, c);
                }
                last = c;
            }
            Popularity.Sort(ChromosomeCompare);
            BestFitter = Popularity[0];
            Range.Stream(PopuSize/2, PopuSize).ForEach(
                i => { Popularity[i] = GenChromosome(ChromosomeLength); }
                );

        }

        public Chromosome NaturalSelection(int iter = 100)
        {
            Popularity.Sort(ChromosomeCompare);
            Range.Stream(0, iter).ForEach(evolution);
            return BestFitter;
        }

    }
}
