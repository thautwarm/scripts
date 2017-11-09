import java.util.*
import java.util.stream.IntStream
import kotlin.streams.toList
typealias Vector = List<Double>
typealias DataSets = List<Pair<Vector, Double>>

object Perceptron {
    val rnd = Random()
    fun dataGen(size: Int, featureLength: Int, f: (Vector) -> Double) =
            IntStream.range(0, size).toList().map {
                val features =
                        IntStream
                                .range(0, featureLength)
                                .toList()
                                .map { rnd.nextDouble() }
                                .toList()

                val d = Math.signum(f(features))
                Pair(features, d)
            }


    class Perceptron(size: Int) {
        var Weight: Vector = rnd.doubles(size.toLong(), 0.0, 1.0).toList()
        var Bias: Double = rnd.nextDouble()
        val Size = size
        fun Forward(input: Vector): Double = Math.signum(Weight.zip(input).sumByDouble { it.first + it.second } + Bias)
        fun Renew(input: Vector, target: Double, learningRate: Double = 0.3) {
            if (Forward(input) * target < 0) {
                IntStream.range(0, Size).forEach {
                    Weight = Weight.zip(input).map { it.first + learningRate * target * it.second }
                    Bias += learningRate * target
                }
            }
        }
    }


}
fun main(args: Array<String>) {
    val datas: DataSets = Perceptron.dataGen(100, 2, { it[0] * 2 + it[1] - 1.5 })
    val perceptron = Perceptron.Perceptron(2)
    IntStream.range(0, 3).forEach {
        for ((data, target) in datas) {
            perceptron.Renew(data, target)
        }
    }
    datas.forEach {
        val (data, target) = it
        println(message = """${perceptron.Forward(data)} $target""")
    }
}
