Dtype = Float64
Membership = Vector{Dtype}
Relation = Matrix{Dtype}
Rule = Matrix{Int}

A::Membership → B::Membership = begin
    row = size(A)[1]
    col = size(B)[1]
    relation = zeros(row, col)
    @parallel for i = 1:row
        @parallel for j = 1:col
            relation[i, j] = min(A[i], B[j])
        end
    end
    relation
end

transform_mat = [0.0, 0.5, 1.0] → [0, 0.6, 1]
display(transform_mat)
# 3×3 Array{Float64,2}:
#  0.0  0.0  0.0
#  0.0  0.5  0.5
#  0.0  0.6  1.0

function decision(relation :: Relation, rule :: Rule)
    size_relation = size(relation)
    size_rule = size(rule)
    if size_rule != size_relation
        throw(ArgumentError(
        "relation matrix($size_relation) and rule matrix($size_rule) don't match size."))
    end
    row, col = size(relation)
    categories = unique(rule)

    function handle(maxval, maxindex, col)
        return maxval, (1+div(maxindex, col), maxindex%col)
    end
    Dict(category => handle(findmax(relation[rule .== category])..., col)
        for category in categories)
end

rule = [1 2 3;
        2 3 1;
        3 1 2]

decision(transform_mat, rule) |> println
# Dict(2=>(1.0, (2, 0)),3=>(0.5, (1, 2)),1=>(0.6, (1, 2)))
