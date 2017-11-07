using System;
using System.Collections.Generic;
using System.Linq;


namespace Calc.Perceptron
{
    using Vector = List<double>;
    public class Perceptron
    {
        public Vector Weight;
        public double Bias;
        public double Forward(Vector input)
        {
            return Math.Sign(input.Zip(Weight, (a, b) => a * b).Sum() + Bias);
            
        }
        public void Renew(Vector input, double target, double rate = 0.3)
        {
            if (target * Forward(input) < 0)
            {
                Weight = Weight.Zip(input, (a, b) => a + rate * target * b).ToList();
                Bias = Bias + rate * target;
            }

        }
    }
}
