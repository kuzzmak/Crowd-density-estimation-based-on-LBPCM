import numpy as np
import util


class VotingClassifier:

    def __init__(self, classifiers, configurations):
        self.classifiers = classifiers
        self.configurations = configurations

    def predictSubImage(self, subImage):

        fv = []
        mean = []
        sigma = []
        classifier_acc = []

        for c in self.configurations:

            lbpcm = util.getLBPCM(c)
            fv.append(lbpcm.getFeatureVector(subImage, c[1]))
            mean.append(c[11])
            sigma.append(c[12])
            classifier_acc.append(1 - c[13])

        fv = np.array(fv)
        mean = np.array(mean)
        sigma = np.array(sigma)

        fv -= mean
        fv /= sigma

        weights = []
        for acc in classifier_acc:
            weights.append(np.log(acc / (1 - acc)))

        weights /= np.sum(weights)
        weights = np.reshape(weights, (len(weights), -1))

        predict_proba = []
        i = 0
        for cl in self.classifiers:
            predict_proba.append(cl.predict_proba(fv[i]))
            i += 1
        predict_proba = np.array(predict_proba)
        probs = np.apply_over_axes(np.sum, weights * predict_proba, axes=0)
        print(np.argmax(probs))