import java.util.Collection;
import java.util.List;
import java.util.Random;
import java.util.Vector;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.DoubleStream;
import java.util.stream.IntStream;


public class DataGen {
    public static Random rnd = new Random();

    public static List<Tuple<Vector<Double>, Double>> DataSets(int dataSize,
                                                               int featureLength,
                                                               Function<Vector<Double>, Double> f,
                                                               double inf, double sup) {

        return IntStream.range(0, dataSize).mapToObj(
                i -> {
                    Vector<Double> a = new Vector<>(featureLength);
                    IntStream.range(0, featureLength).forEach( j->{
                        a.add(rnd.nextDouble() ) ;
                    });
                    double target = Math.signum(f.apply(a));
                    return new Tuple<Vector<Double>, Double>(a, target);
                }
        ).collect(Collectors.toList());
    }
    public static List<Tuple<Vector<Double>, Double>> DataSets(int dataSize,
                                                               int featureLength,
                                                               Function<Vector<Double>, Double> f){
        return DataSets(dataSize, featureLength,f, 0, 1);
    }

//    public static void main(String[] args) {
//
//        List<Tuple<Vector<Double>, Double>> a = DataSets(10, 2,
//                                            list -> list.get(0) + list.get(1) - 1.0,
//                                            0, 1);
//        a.forEach(i->System.out.println(i.snd));
//
//    }

}

