testDataX = [[1,1,1],[1,2,2],[1,3,3],[1,4,4],[1,5,5]]
testDataY = [1,2,3,4,5]

learningRate = 0.05
theta = [0,0,0]
lastLoss = 100000000
for n in range(10000):
        print "loop ", n, theta
        delta = [0,0,0]
        loss = 0
        for j in range(len(testDataX)):
                calY = 0
                for i in range(len(theta)):
                        calY +=  theta[i] * testDataX[j][i]
#               print "Calculated:" , testDataX[j][1], calY
                loss += (testDataY[j] - calY)**2
                for i in range(len(theta)):
                        delta[i] += (testDataY[j] - calY) * testDataX[j][i]
        print "Loss:", loss
        for i in range(len(theta)):
                theta[i] += learningRate * delta[i] / len(testDataX)
        if abs(lastLoss - loss) < 0.000000001:
                print("Done at ", n)
                break
        else:
                lastLoss = loss

