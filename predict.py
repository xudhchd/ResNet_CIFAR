import keras
import numpy as np
from keras.datasets import cifar10, cifar100
from keras import backend as K
from keras.models import load_model
from sklearn import metrics
import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt


# set GPU memory 
if('tensorflow' == K.backend()):
    import tensorflow as tf
    from keras.backend.tensorflow_backend import set_session
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)

print("\n== LOADING MODEL... ==")

# model = load_model('/home/bg/Desktop/ResNet_CIFAR/decay_test/resnet_50_cifar100_4_2/146_0.6307.h5')
# model = load_model('/home/bg/Desktop/ResNet_CIFAR/decay_test/resnet_50_cifar100_4_2/148_0.6118.h5')
# model = load_model('/home/bg/Desktop/ResNet_CIFAR/decay_test/resnet_50_cifar100_4_2/147_0.6110.h5')
# model = load_model('/home/bg/Desktop/ResNet_CIFAR/decay_test/resnet_50_cifar100_4_2/149_0.6083.h5')
# model = load_model('/home/cgilab/Desktop/ResNet_CIFAR/decay_test/resnet_50_cifar10_5_1/246_0.8687.h5')
model = load_model('/home/cgilab/Desktop/ResNet_CIFAR/decay_test/resnet_50_cifar10_5_1/247_0.8724.h5')
# model = load_model('/home/cgilab/Desktop/ResNet_CIFAR/decay_test/resnet_50_cifar10_5_1/248_0.8848.h5')
# model = load_model('/home/cgilab/Desktop/ResNet_CIFAR/decay_test/resnet_50_cifar10_5_1/249_0.8944.h5')
# model = load_model('/home/cgilab/Desktop/ResNet_CIFAR/decay_test/resnet_50_cifar10_5_1/250_0.8557.h5')

print("\n== DONE! ==")

num_classes = 100
mean = [129.3, 124.1, 112.4]
std  = [68.2, 65.4, 70.4]
(x_train, label_train), (x_test, label_test) = cifar10.load_data()

y_train = keras.utils.to_categorical(label_train, num_classes)
y_test = keras.utils.to_categorical(label_test, num_classes)

print("\n== DONE! ==\n\n== COLOR PREPROCESSING... ==")

# color preprocessing
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
for i in range(3):
    x_train[:,:,:,i] = (x_train[:,:,:,i] - mean[i]) / std[i]
    x_test[:,:,:,i] = (x_test[:,:,:,i] - mean[i]) / std[i]

#######################################################################

# number = [i for i in range(10)]
# count = [0]*10
# for i in y:
#     count[i] += 1
# plt.bar(number,count)
# # plt.savefig('lable.png')

# count = [0]*10
# for i in x:
#     count[i] += 1
# plt.bar(number,count)
# # plt.savefig('pred_246.png')
# # plt.savefig('pred_247.png')
# # plt.savefig('pred_248.png')
# # plt.savefig('pred_249.png')
# plt.savefig('pred_250.png')	

#######################################################################


pred = model.predict(x_train, batch_size=512, verbose=0, steps=None)
result = np.argmax(pred,axis=1)
print(pred.shape)
print(result.shape)
print(label_train.shape)

x = result.flatten().tolist()
y = label_train.flatten().tolist()

cmat = metrics.confusion_matrix(y, x)
print(cmat)
print(type(cmat))

# Plot confusion matrix
fig = plt.figure(figsize=(10,10))
plt.tight_layout()
ax = fig.add_subplot(111)
res = ax.imshow(cmat, cmap=plt.cm.rainbow,interpolation='nearest')
width, height = cmat.shape
for x in range(width):
    for y in range(height):
        ax.annotate(str(cmat[x,y]), xy=(y, x),horizontalalignment='center',verticalalignment='center')


classes = ['Airplane','Automobile','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck']
plt.xticks(range(width), classes, rotation=0)
plt.yticks(range(height), classes, rotation=0)
ax.set_xlabel('Predicted Class')
ax.set_ylabel('True Class')
plt.title('CIFAR-10 Confusion Matrix')
plt.show()

# plt.savefig('cm_246.png')
plt.savefig('cm_247.png')
# plt.savefig('cm_248.png')
# plt.savefig('cm_249.png')
# plt.savefig('cm_250.png')	
