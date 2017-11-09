training_data_file = "data.txt"
predict_file = "predict.txt"

dat = read.table(training_data_file, sep=",", col.names = c(1,2,3))
row= dim(dat)[1]; col = dim(dat)[2];
datas = dat[1:row,1:(col-1)]
target = dat[1:row, col]
pred = read.table(predict_file, sep=",", col.name=c(1))[,1]


idx = target==-1
x <- datas[!idx, 1]
y<-datas[!idx, 2]
plot(x, y, col ='blue', ylim =  c(-2, 2),xlim = c(-2, 2), sub = "True Categories")
points(datas[idx, 1], datas[idx, 2], col ='red', ylim = c(-2, 2),xlim = c(-2, 2), sub = "True Categories")
idx = pred==-1
x <- datas[!idx, 1]
y <- datas[!idx, 2]
plot(x, y, col ='yellow', ylim = c(-2, 2),xlim = c(-2, 2), sub = "Predictions")
points(datas[idx, 1], datas[idx, 2], col ='purple', ylim = c(-2, 2),xlim = c(-2, 2), sub = "Predictions")
