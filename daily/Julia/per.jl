# __precompile__()
using Gadfly
# constants
W1 = 1.0
W2 = -1.0
bias = 0.2

#types
Dtype = Float64
Vec = Vector{Dtype}
Data = Tuple{Vec, Int}
DataSets = Vector{Data}


# Perceptron Structure
mutable struct Perceptron
    weight :: Vec
    bias :: Dtype
    lr :: Dtype
    Perceptron(size :: Int, LR :: Dtype) = new(rand(size), rand(), LR)
end


doc"""
train Perceptron
"""
function train!(model :: Perceptron, datasets :: DataSets, iter = 100)

    for iter_num in 0:iter-1
        count = 0

        for (vec, target) in datasets
            if  target * (dot(model.weight, vec) + model.bias) <= 0
                count += 1
                model.weight = model.weight + (model.lr * target) .* vec
                model.bias = model.bias + model.lr * target
            end
        end

        if count == 0
            println("converged on current datasets.")
            println("use $iter_num times to converge.")
            break
        else
            println("haven't been converaged yet.")
        end
    end

end

doc"""
use some model to predict the labels of unlabeled data.
"""
function predict(model :: Perceptron, datasets ::  Vector{Vec})
    map(datasets) do data
        dot(model.weight, data) + model.bias > 0 ? 1 : -1
    end
end




function make_data(a :: Dtype, b :: Dtype)
    target = W1*a + W2*b + bias
    ([a, b], target>0? 1 : -1)
end

function make_datasets(size :: Int, radius = 50.0)
    map(1:size) do _
        r = rand()*radius
        θ = 2 * π * rand()
        x = r * cos(θ)
        y = r * sin(θ)
        make_data(x, y)
    end
end


datasets = make_datasets(100, 1.2)
per = Perceptron(2, 0.05)
train!(per, datasets)
train!(per, datasets)
vecs, targets = collect(zip(datasets...))

# println("datasets:")
# println(datasets))

datas = collect(vecs)
println(per)
println("result:")
pred = predict(per, datas)
foreach(collect(zip(pred, targets))) do each
    println("-> $each")
end
acc = map(zip(pred, targets)) do x
    a, b = x
    a == b
end |> sum |> x -> x/size(datasets)[1]

println("acc: $acc")


#plot

W!1, W!2 = per.weight
b! = per.bias
line_fn = x -> (- b! - W!1 * x)/W!2

X, Y = zip(datas...)
X = collect(X)
Y = collect(Y)
AllX = sort(X)


points = layer(x=X, y=Y, color=collect(targets), Geom.point)
line = layer(x=AllX,
             y=map(line_fn, AllX),
             color=map(x->0, collect(targets)), Geom.line)
Gadfly.add_plot_element!(line, Guide.title("formula: $W!1 x + $W!2 y + $b! = 0"))
graph = plot(points, line)
# graph = vstack(line, points)

draw(SVG("perceptron.svg", 5inch, 5inch), graph)
