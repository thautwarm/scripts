
import java.io.*;
import java.util.List;
import java.util.Vector;
import java.util.stream.IntStream;

public class Console {

    private static void Perceptron(String[] args) {
        int dataSize = 100, featureLength = 2;

        if (args.length == 2) {
            dataSize = Integer.parseInt(args[0]);
            featureLength = Integer.parseInt(args[1]);
        } else if (args.length == 1) {
            dataSize = Integer.parseInt(args[0]);
        }

        Perceptron perceptron = new Perceptron(2);
        List<Tuple<Vector<Double>, Double>> datas = DataGen.DataSets(dataSize, featureLength, i -> -1 + i.get(0) + i.get(1));

        IntStream.range(0, 3).forEach(cycle -> {
            datas.forEach(data -> {
                perceptron.Renew(data.fst, data.snd);
            });

        });

        Vector<Double> prediction = new Vector<>(dataSize);


        for (Tuple<Vector<Double>, Double> data : datas) {
            prediction.add(perceptron.Forward(data.fst));
        }


        try {
            FileWriter dataIO = new FileWriter("./data.txt");
            FileWriter predIO = new FileWriter("./predict.txt");
            datas.forEach(data -> {

                data.fst.forEach(i -> {
                    try {
                        dataIO.write(i.toString() + ",");
                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                });
                try {
                    dataIO.write(data.snd.toString() + "\n\r");
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });

            prediction.forEach(i -> {
                try {
                    predIO.write(i.toString() + "\n\r");
                } catch (IOException e) {
                    e.printStackTrace();
                }

            });

            dataIO.close();
            predIO.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {

        switch (args.length) {
            case 1:
                Perceptron(new String[]{"100", "2"});
                break;
            default:
                if (args.length == 2)
                    Perceptron(new String[]{args[1]});
                else if (args.length == 3) {

                    Perceptron(new String[]{args[1], args[2]});

                }
                break;
        }
        Genetic();
    }

    private static void Genetic() {

        Genetic genetic = new Genetic(data -> (data.get(0) ? 1.0 : 0)
                + (!data.get(1) ? 1.0 : 0)
                + (data.get(2) ? 1.0 : 0),
                100, 3);
        genetic.NaturalSelection(100);
        genetic.BestIndividual.forEach(i -> System.out.print(i + ","));
        System.out.println();

    }
}
