
import java.util.Comparator;
import java.util.Vector;

public class ChromosomeCompare implements Comparator<Vector<Boolean>> {

    public Genetic Gene;
    public ChromosomeCompare(Genetic genetic){
        Gene = genetic;

    }

    public int compare(Vector<Boolean> c1, Vector<Boolean> c2) {
        Double a = Gene.Fit.apply(c1);
        Double b = Gene.Fit.apply(c2);
        return -a.compareTo(b);
    }
}