import numpy as np
import util
import concurrent.futures

class VotingClassifier:
    """
    Razred koji spaja više klasifikatora u jedan te
    donosi odluku na temelju kombinacije svih klasifikatora
    gdje je utjecaj svakog određen težinom koja ovisi o
    točnosti klasifikatora.
    """

    def __init__(self, classifiers, configurations):
        self.classifiers = classifiers
        self.configurations = configurations

    def getProbAndAccuracy(self, subImage, model, configuration):
        """
        Metoda za dobivanje vjerojatnosti klasifikacije pojedinih razreda
        svakog klasifikatora i težina kojima se pojedine vjerojatnosti
        množe

        :param subImage: podslika za koju se stvaraju vjerojatnosti
        :param model: klasifikator koji se koristi za klasifikaciju
        :param configuration: konfiguracija pojedinog klasifikatora
        :return: polje vjerojatnosti i težina
        """

        lbpcm = util.getLBPCM(configuration)

        # normalizacija
        fv = lbpcm.getFeatureVector(subImage, configuration[1])
        mean = np.array(configuration[11])
        sigma = np.array(configuration[12])
        fv -= mean
        fv /= sigma

        # vjerojatnosti klasifikacije po razredima
        predict_proba = model.predict_proba([fv])[0]
        # točnost klasifikacije
        acc = 1 - configuration[13]
        # težina za svaki klasifikator
        weight = np.log(acc / (1 - acc))

        return [predict_proba, weight]

    def clasify(self, image):
        """
        Metoda za klasifikaciju pojedine slike

        :param image: slika koja se klasificira
        :return: lista labela razreda pojedine podslike
        """

        dim = (160, 88)
        # zeljena sirina slikovnog elementa
        x_size = dim[0]
        # zeljena visina slikovnog elementa
        y_size = dim[1]
        # sirina slike
        imageX = image.shape[1]
        # visina slike
        imageY = image.shape[0]
        # cjelobrojni broj koraka u x smjeru(koliko je moguce napraviti slikovnih elemenata sa sirinom x_size)
        stepX = imageX // x_size
        # koraci u y smjeru
        stepY = imageY // y_size

        labels = []

        subImages = []
        for y in range(stepY):
            for x in range(stepX):
                subImages.append(image[y * y_size:(y + 1) * y_size, x * x_size:(x + 1) * x_size])

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for subImage, label in zip(subImages, executor.map(self.classifySubImage, subImages)):
                labels.append(label)

        return labels

    def classifySubImage(self, subImage):
        """
        Metoda za klasifikaciju pojedine podslike

        :param subImage: podslika koja se klasificira
        :return: labela podslike
        """
        predictions_weights = []

        for i in range(len(self.configurations)):
            predictions_weights.append(
                self.getProbAndAccuracy(
                    subImage,
                    self.classifiers[i],
                    self.configurations[i]))

        predictions_weights = np.array(predictions_weights)

        weights = predictions_weights[:, 1]
        weights /= np.sum(weights)

        predictions = predictions_weights[:, 0]

        probs = np.apply_over_axes(np.sum, weights * predictions, axes=0)

        return np.argmax(probs)
