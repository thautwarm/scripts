import javax.swing.*;
import java.security.acl.Group;
import java.util.Comparator;
import java.util.Random;
import java.util.List;
import java.util.Vector;
import java.util.function.Function;
import java.util.stream.IntStream;


public class Genetic {

    public static Random rnd = new Random();
    public double MutateRate=0.05;
    public double CrossoveRate = 0.03;
    public Function<Vector<Boolean>, Double> Fit;

    public Vector<Vector<Boolean>> Popularity;
    public Vector<Boolean> BestIndividual;
    public ChromosomeCompare comparator;

    public int ChromosomeLength;
    public int GroupSize;

    private Function<Double, Integer> GetCrossoverLoc;



    public Genetic(Function<Vector<Boolean>, Double>  fit, int groupSize, int chromosomeLength){
        Fit = fit;
        GroupSize = groupSize;
        ChromosomeLength = chromosomeLength;
        GetCrossoverLoc = random-> ((int) (random*ChromosomeLength));
        comparator = new ChromosomeCompare(this);
        Popularity = new Vector<Vector<Boolean>>(GroupSize);
        IntStream.range(0, GroupSize).forEach(i->{
            Popularity.add(GenChromosome(ChromosomeLength));
        });
    }
    private boolean ChromosomeCompare(Vector<Boolean> a, Vector<Boolean> b){
        return Fit.apply(a).equals(Fit.apply(b));
    }

    public void Mutate(Vector<Boolean> chromosome){
        IntStream.range(0, ChromosomeLength).forEach( i-> {
                    if (rnd.nextDouble() > MutateRate) {
                        chromosome.set(i, !chromosome.get(i));
                    }
                }
        );
    }

    public void Crossover(Vector<Boolean> c1, Vector<Boolean> c2){
        if (rnd.nextDouble() > CrossoveRate){
            int idx = GetCrossoverLoc.apply(rnd.nextDouble());
            IntStream.range(0, idx).forEach(i->{
                Boolean tmp = c1.get(i);
                c1.set(i, c2.get(i));
                c2.set(i, tmp);
            });
        }
    }

    public static Vector<Boolean> GenChromosome(int size){
        Vector<Boolean> c = new Vector<>(size);
        IntStream.range(0, size).forEach(i->{
            c.add(rnd.nextBoolean());
        });
        return c;
    }

    public void evolution(int nth){
        System.out.println(nth+"-th iter.");


        IntStream.range(1, GroupSize).forEach(i->
                {
                    Mutate(Popularity.get(i));
                }
        );
        Vector<Boolean>[] last = new Vector[]{null};
        IntStream.range(1, GroupSize).forEach(i->
        {
            if (last[0] == null){
                last[0] = Popularity.get(i);
            }
            else Crossover(last[0], Popularity.get(i));
        });


        Popularity.parallelStream().mapToDouble(Fit::apply);
        Popularity.sort(comparator);
        BestIndividual = Popularity.get(0);

        IntStream.range(GroupSize/2, GroupSize).forEach(i->{
            Popularity.set(i, GenChromosome(ChromosomeLength));
        });

    }
    public Vector<Boolean> NaturalSelection(){
        return NaturalSelection(100);

    }

    public Vector<Boolean> NaturalSelection(int iter){
        System.out.print(comparator);
        Popularity.sort(comparator);
        BestIndividual = Popularity.get(0);

        IntStream.range(0, iter).forEach(i->{
            evolution(i);
        });
        return BestIndividual;
    }



}
