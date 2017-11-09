
## 感知机

Class 文件路径:
`./out/production/Java`
```
java Console [Perceptron] [dataSize默认100] [featureLength默认2]
```

## GA
因为我不知道怎么让Java从命令行参数parse一个函数(也不想为这个来造一个dsl一般的东西)，所以使用者需要在源代码里修改如下参数直接运行:

- Fit, 一个lambda， 从Vector<Boolean>映到Double.
- groupSize, 种群数量(固定
- chromosomeLength, 基因序列的长度。

# 简单示例：

```Java
Genetic genetic = new Genetic(      // Fit
                                data->   (data.get(0)==true ?1.0:0)
                                        +(data.get(1)==false?1.0:0)
                                        +(data.get(2)==true ?1.0:0),
                                
                                100, // groupSize
                                3);  // chromosomeLength
genetic.NaturalSelection(100);
genetic.BestIndividual.forEach(i->System.out.print(i+","));
System.out.println();
```
正如所期望的，结果是[true, false, true]。

