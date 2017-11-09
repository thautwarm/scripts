import java.util.List;
import java.util.Random;
import java.util.Vector;
import java.util.stream.IntStream;


public class Perceptron {
    private static Random rnd = new Random();
    public Vector<Double> Weight;
    public Double Bias;
    private int Size;

    public Perceptron(int size){
        Size = size;
        Weight = new Vector<>(Size);
        IntStream.range(0, size).forEach(
                i-> {
                    Weight.add(rnd.nextDouble());
                }
        );
        Bias = rnd.nextDouble();
    }

    public Double Forward(Vector<Double> input) {
        return Math.signum(IntStream.range(0, Size).mapToDouble(i->Weight.get(i)*input.get(i)).sum()+Bias);
    }
    public void Renew(Vector<Double> input, double target){
        double learningRate = 0.3;
        Renew(input, target, learningRate);
    }
    public void Renew(Vector<Double> input, double target, double learningRate){
        if (Forward(input)*target<0){
            IntStream.range(0, Size).forEach(i->{
                Weight.set(i, Weight.get(i) + learningRate * target * input.get(i));
            });
            Bias = learningRate*target + Bias;
        }
    }

}
