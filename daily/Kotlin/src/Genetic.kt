import java.util.Random

typealias Chromosome = List<Boolean>
typealias Popularity = List<Chromosome>
object Genetic {
    val rnd = Random()

    class Genetic(fit: (Chromosome) -> Double,
                  groupSize: Int,
                  chromosomeSize: Int,
                  mutateRate: Double = 0.2,
                  crossoverRate: Double = 0.1) {
        private val ChromosomeSize = chromosomeSize
        private val GroupSize = groupSize
        private val MutateRate = mutateRate
        private val CrossoverRate = crossoverRate
        private val Fit = fit;
        private val GetCrossoverHead = { prob: Double -> (prob * rnd.nextDouble()).toInt() }
        private fun GenChromosome(size: Int) = IntRange(0, size).map { rnd.nextBoolean() }
        var Popularity = IntRange(0, GroupSize).map{ GenChromosome(chromosomeSize) }
        var BestInd = GenChromosome(chromosomeSize)
        private var swap = BestInd

        private fun Mutate(c: Chromosome): Chromosome = c.map { it ->
            if (rnd.nextDouble() > MutateRate) {
                !it
            }
            it
        }

        private fun Crossover(c1: Chromosome): Chromosome {
            if (rnd.nextDouble()>CrossoverRate) return c1
            val head = GetCrossoverHead(rnd.nextDouble())
            return c1.zip(swap).mapIndexed { idx, (first, second) ->
                if (idx <= head){
                    swap = c1
                    second
                }
                else first
            }
        }

        private fun evolution(order: Int) {
            println("""$order-th cycle.""")
            Popularity = Popularity
                    .map { Mutate(it) }
                    .map { Crossover(it) }
                    .sortedBy(Fit)
                    .mapIndexed{
                        idx, chromosome->
                            if(idx<GroupSize/2) chromosome
                            else GenChromosome(ChromosomeSize)
                    }
            BestInd = Popularity.get(0)
        }
        fun NaturalSelection(iter:Int=100) = {
            IntRange(0, iter).forEach{evolution(it)}
            BestInd
        }
    }
}