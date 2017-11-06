using System;
using System.Collections.Generic;
using System.Linq;



namespace Dr.Perceptron
{

    using Vector = List<double>;
    public class Percepron
    {
        private Vector weight;
        private double bias;

        public Vector Weight { get => weight; set => weight = value; }
        public double Bias { get => bias; set => bias = value; }
        public double Forward(Vector input) => input.Zip(weight, (a, b) => a * b).Sum() + bias;
        public void Renew(Vector input, double target, double rate = 0.3)
        {
            if(Forward(input)*target<0)
            {
                weight = weight.Zip(input, (a, b) => a + rate*target*b).ToList();
                bias = bias + rate * target;
            }
        }
    }
}

