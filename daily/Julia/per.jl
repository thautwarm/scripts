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
# train the perceptron
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
            println("traverse the datsets  $iter_num times to converge.")
            return count == 0 # return is the model fitted or not
        else
            println("haven't been converaged yet.")
        end
    end

    false
end

doc"""
use some model to predict the labels of unlabeled data.
"""
function predict(model :: Perceptron, datasets ::  Vector{Vec})
    map(datasets) do data
        dot(model.weight, data) + model.bias > 0 ? 1 : -1
    end
end





function make_datasets(size :: Int, radius = 50.0)
    const make_data(a :: Dtype, b :: Dtype) = begin
        target = W1*a + W2*b + bias
        ([a, b], target>0? 1 : -1)
    end

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


while train!(per, datasets) == false
    # retrain perceptron
end

vecs, targets = collect(zip(datasets...))

datas = collect(vecs)
println(per)  # print the fitted perceptron model
pred = predict(per, datas)
# print all the predictions with their corresponding true value.
# foreach(collect(zip(pred, targets))) do each
#     println("-> $each")
# end
acc = map(zip(pred, targets)) do x
    a, b = x
    a == b
end |> sum |> x -> x/size(datasets)[1]

println("acc: $acc")


# plot
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
graph = plot(points, line)
Gadfly.add_plot_element!(graph,
                         Guide.title("formula: x + $(round(W!2/W!1, 2)) y + $(round(b!/W!1, 2)) = 0"))

draw(SVG("perceptron.svg", 5inch, 5inch), graph)

# write the pairs into text file.
open("datas.txt", "w") do f
    write(f, "true classifier : f(x, y) = x - y - 0.2\n")
    write(f, string(datas))
end
