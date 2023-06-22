## Approach   

To choose the best parameters for this problem, several experimental runs would be conducted.  

For each experimental run, changes would be made to one of the following parameters
- Number of dropouts
- Number of hidden layers (and nodes in each layer)
- Filter size of Convolution layer
- Pooling size of Max Pooling layer
- Number of convolution - pooling layers

Although simultaneous changes might impact the result differently, since the purpose is to observe the affect of each parameter, only one parameter would be changed each run.   

Several values would be tested for each parameter and only those with notable changes would be recorded in the table below. The results recorded are testing results, calculated from an average of 5 runs.

---

## Experimental Results

|Run|No. Convo Layers| Filter size  | Pool size  | Hidden layers  | Dropout| Accuracy | Loss |
|---|----------------|--------------|------------|----------------|--------|----------|------|
|  1|       1        |  (3, 3)      | (2, 2)     | 1 [128]        |  0     | 0.9577   |0.1968|
|  2|       1        |  (3, 3)      | (2, 2)     | 1 [128]        |  0.3   | 0.9741   |0.1165|
|  3|       1        |  (3, 3)      | (2, 2)     | 1 [128]        |  0.5   | 0.9616   |0.1734|
|  4|       1        |  (3, 3)      | (2, 2)     | 2 [256, 128]   |  0.3   | 0.9705   |0.1433|
|  5|       1        |  (3, 3)      | (2, 2)     | 2 [128, 64]    |  0.3   | 0.9606   |0.1243|
|  6|       1        |  (5, 5)      | (2, 2)     | 1 [128]        |  0.3   | 0.9787   |0.0995|
|* 7|       1        |  (5, 5)      | (3, 3)     | 1 [128]        |  0.3   | 0.9790   |0.0961|
|  8|       2        |  (5, 5)      | (3, 3)     | 1 [128]        |  0.3   | 0.9407   |0.1830|

Run that yields the best result is run 7, with accuracy of 0.9790, loss of 0.0961 and training run time of 590ms/epoch

---

## Observations
- When dropout is not applied, there is a drop in accuracy between training and testing -> overfitting issue. 

- Accuracy starts to decrease when dropout values gets higher than 0.4 -> lack of data due to dropout.

- Drop in accuracy between training and testing increase as number of nodes/layers in hidden layers increases -> complex hidden layers may lead to overfitting, especially with simple problem like this particular problem.

- As filter size increases, accuracy also increase slightly, however, computational cost also increases.

- As pool size increases (more than 4x4), accuracy starts to drop, possibly due to the loss in information (as max pooling reduces the size of training data). 

---

## Conclusion
From the experimental runs, the model that yield a good result with relatively low computation time (compared to the sample run shown in the Project Details page) is as followed.
- Convolution layer: filter size 5x5
- Max Pooling layer: pooling size 3x3
- Dense Layer: 1 layer of 128 nodes with "ReLU" activation
- Dropout: 0.3
- Output Dense Layer with "softmax" activation  