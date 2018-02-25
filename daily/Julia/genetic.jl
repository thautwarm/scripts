# integer permutation genetic algorithm
# permutation chromosome:
#   a permutation to represent genetic information.

using Base.Iterators.take
Dtype = Float64
Gene = Int  # allele.
Chromosome  = Vector{Gene} # a chromosome is a vector of genes.
Popu  = Vector{Chromosome}  # a population os a vector of chromosomes.

Point = Tuple{Int, Int}

doc"""
# a rnadom disturb
"""
function defaultDisturb(chromosome :: Chromosome, actualScore :: Dtype)
    return actualScore * (1 + (rand() - 0.5)/100)
end

doc"""
# create a new permutation chromosome with length = `size`
"""
function newChromosome(size)
    randperm(size)
end

doc"""
# a way of transgenation, mutate some gene
#   of the chromosome immediately, inplace.
"""
function mutate!(chromosome :: Chromosome, size :: Int)

    loc1, loc2 = rand(1:size), rand(1:size)
    # select 2 location in a chromosome and exchange them.

    if (loc1 != loc2)
        chromosome[loc1], chromosome[loc2] = chromosome[loc2], chromosome[loc1]
    end
end

doc"""
# the non-side-effect version of mutate transgenation.
"""
function mutate(chromosome :: Chromosome, size :: Int)
    loc1, loc2 = rand(1:size), rand(1:size)
    new_chromosome = chromosome[1:end]
    if (loc1 != loc2)
        new_chromosome[loc1], new_chromosome[loc2] = new_chromosome[loc2], new_chromosome[loc1]
    end
    new_chromosome  # do not change the original gene and return a new one
end

doc"""
# cross over transgenation take place in the inner of the chromosome.
"""
function innerCrossOver!(chromosome :: Chromosome, size :: Int)
    loc = rand(1:size)
    left = size - loc
    arrBuff = chromosome[1:loc]
    chromosome[1:left] = chromosome[loc+1:end]
    chromosome[left+1:end] = arrBuff
end

doc"""
# the non-side-effect version of inner cross over transgenation.
"""
function innerCrossOver(chromosome :: Chromosome, size :: Int)
    loc = rand(1:size)
    new_chromosome = chromosome[loc+1:end]
    append!(new_chromosome, chromosome[1:loc])
    new_chromosome
end

doc"""
# genetic algorithm.
"""
function ga(chromosome_length :: Int, fitness :: Function,
            iter = 500, popu_size = 500,
            p_c = 0.02, p_m = 0.05,
            use_disturb :: Any = false)

    popu :: Popu = map(1:popu_size) do _
        newChromosome(chromosome_length)
    end

    if use_disturb == false
        fitnessWrap = fitness
    else
        fitnessWrap = x -> disturb(x, fitness(x))
    end

    for iter_num = 1:iter

        # sort the population according to the fitness score.
        sort!(popu, by=fitnessWrap)

        # generate a random number to decide how many chromosomes to survive.
        remain_num = trunc(Int, clamp.(rand(), 0.2, 0.5) * popu_size)

        # filter the population, drop the dead, take the survivor(winner of living competition)
        popu = collect(take(popu, remain_num))


        # in the following codes, I implement an algorithm
        #   to decide how to distribute the new and the trans.
        #
        # in case of avoid eager scenes, I partition the sorted
        #   remained individuals into 2 groups, first of which contains
        #   the better N/2(better partition),
        #   while the second takes the tail(worse partition).
        #
        # I hold the only one who're the best immutable in current iter,
        #   and apply 2 kinds of transgenation methods upon the left of
        #   "better partition". I do not change any in "better partition",
        #   but use them to assign the "worse partition".

        p_m_rand = rand(remain_num-1)
        p_c_rand = rand(remain_num-1)
        half = div(remain_num, 2)
        for i = 1:half - 1
            chromosome = popu[half + i + 1]
            # mutate vary
            will_m = p_m_rand[i] > p_m
            will_c = p_c_rand[i] > p_c
            if will_m
                mutate!(chromosome, chromosome_length)
            end
            # (inner) cross over vary
            if will_c
                innerCrossOver!(chromosome, chromosome_length)
            end

            # ntr
            if !will_c && !will_m
                master = popu[i+1]
                if rand() > 0.5
                    popu[half + i + 1] = mutate(master, chromosome_length)
                else
                    popu[half + i + 1] = innerCrossOver(master, chromosome_length)
                end
            end
        end

        # chromosomerate new chromosomes to fill population
        new_borned = map(1:popu_size - remain_num) do _
            newChromosome(chromosome_length)
        end |> it -> append!(popu, it)

    end
    println(popu[1], fitness(popu[1]))
    (popu[1], fitness(popu[1]))

end


# the x-locations of the cities
X = [34, 56, 27, 44, 4, 10, 55, 14, 28, 12, 16, 68, 24, 29,49, 51, 45, 78, 82, 32, 95, 53,
     7, 64, 88, 23, 87, 34, 71, 98]

# the y-locations
Y = [57, 64, 82, 94, 18, 64, 69, 30, 54, 70, 40, 46, 82, 38, 15, 26, 31, 56,
          33, 11, 8,  46, 94, 62, 52, 61, 76, 58, 41, 69]

# generate the map
Map = collect(zip(X, Y))
# Map = [
#     (100, 200),
#     (50, 70),
#     (40, 20),
#     (9, 200),
#     (170, 33),
#     (110, 120),
#     (300, 120),
#     (200, 70),
#     (180, 50)
# ]

indexOfMap = x -> getindex(Map, x)

doc"""
# the fitness function of TSP on the above map.
"""
function TSP(pathIndex)
    roadLen = 0
    path = map(indexOfMap, pathIndex)
    start = path[1]
    for next in path[2:end]
        x1, y1 = start
        x2, y2 = next
        roadLen += hypot(x2-x1, y2-y1)
        start = next
    end
    x2, y2  = path[1]
    x1, y1  = path[end]
    roadLen + hypot(x2-x1, y2-y1)
end

route, score = ga(size(Map)[1], TSP, 1200, 500, 0.4, 0.45)

# sort x-locations and y-locations with the route.
X! = X[route]
Y! = Y[route]
push!(X!, X![1])
push!(Y!, Y![1])
# plot the route.

using Gadfly
# plot the line chart from A to B
A::Point → B::Point=begin
    x1, y1 = A
    x2, y2 = B
    layer(x = [x1, x2], y = [y1, y2], Geom.point, Geom.line)
end
layers = [from → to for (from, to) in zip(zip(X![1:end-1], Y![1:end-1]),
                                          zip(X![2:end],   Y![2:end]))]
points = plot(layers...)

Gadfly.add_plot_element!(points, Guide.title("the length of route: $(round(score, 2))"))
draw(SVG("tsp_route.svg", 5inch, 5inch), points)

open("tsp_route.txt", "w") do f
    write(f, string(route))
end
