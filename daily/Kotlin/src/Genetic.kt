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
        val ChromosomeSize = chromosomeSize
        val GroupSize = groupSize
        val MutateRate = mutateRate
        val CrossoverRate = crossoverRate
        val Fit = fit;
        private val GetCrossoverHead = { prob: Double -> (prob * rnd.nextDouble()).toInt() }
        private fun GenChromosome(size: Int) = IntRange(0, size).map { rnd.nextBoolean() }
        var Popularity = IntRange(0, GroupSize).map{ GenChromosome(it) }
        
        fun Mutate(c: Chromosome): Chromosome = c.map { it ->
            if (rnd.nextDouble() > MutateRate) {
                !it
            }
            it
        }

        fun Crossover(c1: Chromosome, c2: Chromosome): Pair<Chromosome, Chromosome> {
            val head = GetCrossoverHead(rnd.nextDouble())
            return c1.zip(c2).mapIndexed { idx, gene ->
                if (idx <= head)
                    Pair<Boolean, Boolean>(gene.second, gene.first)
                gene
            }.unzip()
        }

        fun evolution(order: Int) {
            Popularity
        }

    }
}