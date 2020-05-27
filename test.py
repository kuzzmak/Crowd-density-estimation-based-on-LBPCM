# from PIL.ImageFont import _imagingft_not_installed
# from scipy.ndimage import label
#
# import LBPCM
# import numpy as np
# import util
# from sklearn.preprocessing import normalize
# from scipy import stats
# from sklearn.svm import SVC
# import Writer
# import os
# import cv2 as cv
# import joblib
# import App
#
#
#
# lbpcm = LBPCM.LBPCM('gray',
#                             1,
#                             32,
#                             [64, 64],
#                             [0, np.pi],
#                             [1],
#                             ['angular second moment', 'contrast', 'inverse difference moment', 'entropy'],
#                             0,
#                             0)
#
# writer = Writer.Writer()
# writer.loadAnnotedDataFromFile(r'data\models\labeledData.txt')
#
# labelDictionary = writer.labelDictionary
#
# vectors = []
# images = []
#
# imagesPath = os.listdir(r'_data\processedData')
#
# # for i in range(int(0.7 * len(imagesPath))):
# #     images.append(cv.imread(os.path.join('_data\processedData', imagesPath[i]), cv.IMREAD_GRAYSCALE))
# #
# # i = 0
# # for image in images:
# #     print(i)
# #     fv = lbpcm.getFeatureVector(image, 'gray')
# #     vectors.append(fv)
# #     i += 1
#
# c0 = []
# c1 = []
# c2 = []
# c3 = []
# c4 = []
#
# # util.normalize(np.array(vectors))
#
# import joblib
#
# # joblib.dump(vectors, os.path.join('data', 'featureVectors.pkl'))
# vectors = joblib.load(r'data\featureVectors.pkl')
# i = 0
# for i in range(int(0.7 * len(imagesPath))):
#
#     label = labelDictionary[imagesPath[i]]
#
#     if label == "0":
#         c0.append(vectors[i])
#         # c0 = np.add(c0, np.array(vectors[i]))
#     elif label == '1':
#         c1.append(vectors[i])
#         # c1 = np.add(c1, np.array(vectors[i]))
#     elif label == '2':
#         c2.append(vectors[i])
#         # c2 = np.add(c2, np.array(vectors[i]))
#     elif label == '3':
#         c3.append(vectors[i])
#         # c3 = np.add(c3, np.array(vectors[i]))
#     elif label == '4':
#         c4.append(vectors[i])
#         # c4 = np.add(c4, np.array(vectors[i]))
#
#
# c0 = np.apply_over_axes(np.sum, 1 / len(c0) * np.array(c0), axes=0)[0]
# c1 = np.apply_over_axes(np.sum, 1 / len(c1) * np.array(c1), axes=0)[0]
# c2 = np.apply_over_axes(np.sum, 1 / len(c2) * np.array(c2), axes=0)[0]
# c3 = np.apply_over_axes(np.sum, 1 / len(c3) * np.array(c3), axes=0)[0]
# c4 = np.apply_over_axes(np.sum, 1 / len(c4) * np.array(c4), axes=0)[0]
#
# im0 = cv.imread(r'_data\processedData\3169.jpg', cv.IMREAD_GRAYSCALE)
# im1 = cv.imread(r'_data\processedData\187.jpg', cv.IMREAD_GRAYSCALE)
# im2 = cv.imread(r'_data\processedData\213.jpg', cv.IMREAD_GRAYSCALE)
# im3 = cv.imread(r'_data\processedData\3333.jpg', cv.IMREAD_GRAYSCALE)
# im4 = cv.imread(r'_data\processedData\452.jpg', cv.IMREAD_GRAYSCALE)
#
# knn = joblib.load(r'data\models\grayModels\4.pkl')
# app = App.App()
# conf = writer.loadConfFromJSON(4, app.gui)
# picType = 'gray'
#
# mean = np.array(conf[11])
# sigma = np.array(conf[12])
#
# c0 -= mean
# c0 /= sigma
#
# c1 -= mean
# c1 /= sigma
#
# c2 -= mean
# c2 /= sigma
#
# c3 -= mean
# c3 /= sigma
#
# c4 -= mean
# c4 /= sigma
#
# # print(np.linalg.norm(c0-c1))
# # print(np.linalg.norm(c0-c2))
# # print(np.linalg.norm(c0-c3))
# # print(np.linalg.norm(c0-c4))
# # print(np.linalg.norm(c1-c2))
# # print(np.linalg.norm(c1-c3))
# # print(np.linalg.norm(c1-c4))
# # print(np.linalg.norm(c2-c3))
# # print(np.linalg.norm(c2-c4))
# # print(np.linalg.norm(c3-c4))
#
# def function(im, labelNum):
#
#     fev = lbpcm.getFeatureVector(im, picType)
#     fev -= mean
#     fev /= sigma
#
#     label = knn.predict([fev])[0]
#     print('label' + str(labelNum) + ':', label)
#     print('dist from classes: ')
#     print('\tfrom0: ', np.linalg.norm(c0 - fev))
#     print('\tfrom1: ', np.linalg.norm(c1 - fev))
#     print('\tfrom2: ', np.linalg.norm(c2 - fev))
#     print('\tfrom3: ', np.linalg.norm(c3 - fev))
#     print('\tfrom4: ', np.linalg.norm(c4 - fev))
#
#
# function(im0, 0)
# function(im1, 1)
# function(im2, 2)
# function(im3, 3)
# function(im4, 4)
#
# # print(np.linalg.norm(c0-c1))
# # print(np.linalg.norm(c0-c2))
# # print(np.linalg.norm(c0-c3))
# # print(np.linalg.norm(c0-c4))
# # print(np.linalg.norm(c1-c2))
# # print(np.linalg.norm(c1-c3))
# # print(np.linalg.norm(c1-c4))
# # print(np.linalg.norm(c2-c3))
# # print(np.linalg.norm(c2-c4))
# # print(np.linalg.norm(c3-c4))
#
# # import multiprocessing
# #
# # print(multiprocessing.cpu_count())
# #
# # a = [1, 2 , 3, 4]
# # b = [2]
#
# # import numpy as np
# # X = np.array([[-1, -1], [-2, -2], [1, 1], [2, 1]])
# # y = np.array([1, 2, 2, 2])
# #
# # X_test = np.array([[3, 1], [0, 0], [3, 0]])
# # Y_test = np.array([2, 2, 2])
# #
# # from sklearn.svm import SVC
# #
# # clf = SVC(gamma='auto')
# # clf.fit(X, y)
# # error = 1 - clf.score(X_test, Y_test)
# #
#
#
# # import cv2 as cv
# # import joblib
# # import Writer
# # import App
# # import util
# # import numpy as np
#
# # app = App.App()
# #
# # writer = Writer.Writer()
# #
# # image = cv.imread('data/processedData/292.jpg', cv.IMREAD_GRAYSCALE)
# #
# # knn_gray_conf = writer.loadConfFromJSON(30, app.gui)
# # svm_grad_conf = writer.loadConfFromJSON(29, app.gui)
# # # svm_gray_conf = writer.loadConfFromJSON(28, app.gui)
# # # knn_grad_conf = writer.loadConfFromJSON(27, app.gui)
# #
# # lbpcm_knn_gray = util.getLBPCM(knn_gray_conf)
# # lbpcm_svm_grad = util.getLBPCM(svm_grad_conf)
# # # lbpcm_svm_gray = util.getLBPCM(svm_gray_conf)
# # # lbpcm_knn_grad = util.getLBPCM(knn_grad_conf)
# #
# # fv_knn_gray = lbpcm_knn_gray.getFeatureVector(image, 'gray')
# # mean = np.array(knn_gray_conf[11])
# # sigma = np.array(knn_gray_conf[12])
# # fv_knn_gray -= mean
# # fv_knn_gray /= sigma
# #
# # fv_svm_grad = lbpcm_svm_grad.getFeatureVector(image, 'grad')
# # mean = np.array(svm_grad_conf[11])
# # sigma = np.array(svm_grad_conf[12])
# # fv_svm_grad -= mean
# # fv_svm_grad /= sigma
#
# # fv_svm_gray = lbpcm_svm_gray.getFeatureVector(image, 'gray')
# # mean = np.array(svm_gray_conf[11])
# # sigma = np.array(svm_gray_conf[12])
# # fv_svm_gray -= mean
# # fv_svm_gray /= sigma
#
# # fv_knn_grad = lbpcm_knn_grad.getFeatureVector(image, 'grad')
# # mean = np.array(knn_grad_conf[11])
# # sigma = np.array(knn_grad_conf[12])
# # fv_knn_grad -= mean
# # fv_knn_grad /= sigma
#
# # model_knn_gray = joblib.load('data/models/grayModels/30.pkl')
# # model_svm_grad = joblib.load('data/models/gradModels/29.pkl')
# # model_svm_gray = joblib.load('data/models/grayModels/28.pkl')
# # model_knn_grad = joblib.load('data/models/gradModels/27.pkl')
#
# # predict_proba_knn_gray = model_knn_gray.predict_proba([fv_knn_gray])[0]
# # predict_proba_svm_grad = model_svm_grad.predict_proba([fv_svm_grad])[0]
# # predict_proba_svm_gray = model_svm_gray.predict_proba([fv_svm_gray])[0]
# # predict_proba_knn_grad = model_knn_grad.predict_proba([fv_knn_grad])[0]
# #
# # knn_gray_acc = 1 - knn_gray_conf[13]
# # svm_grad_acc = 1 - svm_grad_conf[13]
# # svm_gray_acc = 1 - svm_gray_conf[13]
# # knn_grad_acc = 1 - knn_grad_conf[13]
# #
# # w_knn_gray = np.log(knn_gray_acc / (1 - knn_gray_acc))
# # w_svm_grad = np.log(svm_grad_acc / (1 - svm_grad_acc))
# # w_svm_gray = np.log(svm_gray_acc / (1 - svm_gray_acc))
# # w_knn_grad = np.log(knn_grad_acc / (1 - knn_grad_acc))
# #
# # w1w1 = w_knn_gray + w_svm_grad
# #
# # w_knn_gray /= w1w1
# # w_svm_grad /= w1w1
# #
# # w = np.array([[w_knn_gray], [w_svm_grad]])
# #
# # probabilities = np.array([predict_proba_knn_gray, predict_proba_svm_grad])
# #
# # print('w_k')
# # print(w_knn_gray)
# # print('w_s')
# # print(w_svm_grad)
# # print()
# # print(predict_proba_knn_gray)
# # print(predict_proba_svm_grad)
# # print('Final probabilities')
# # probs = np.apply_over_axes(np.sum, w * probabilities, axes=0)
# # print(probs)
# # print(np.sum(probs))
# # print(np.argmax(probs))
#
# # import VotingClassifier
# # vc = VotingClassifier.VotingClassifier([model_knn_gray, model_svm_grad], [knn_gray_conf, svm_grad_conf])
# # vc.predictSubImage(image)

import util

util.makeSubPictures(r'C:\Users\kuzmi\Downloads\data2\data2Raw', r'C:\Users\kuzmi\Downloads\data2\data2Processed')