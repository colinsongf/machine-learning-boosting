__author__ = 'jiachiliu'

from boosting.dataset import load_crx
from boosting.cross_validation import train_test_shuffle_split, k_fold_cross_validation, shuffle
from boosting.AdaBoost import *


def random_c():
    data, target = load_crx()
    train, test, train_target, test_target = train_test_shuffle_split(data, target, len(data) / 10)
    train_target = np.array(map(lambda v: -1.0 if v == 0 else 1.0, train_target))
    test_target = np.array(map(lambda v: -1.0 if v == 0 else 1.0, test_target))

    indices = range(len(train))
    param = 0.05
    res = []
    while param < 0.5:
        print "Choose %.2f%% of data" % (param * 100)
        choose_size = int(len(indices) * param)
        choose_indices = random.sample(indices, choose_size)

        X = train[choose_indices]
        Y = train_target[choose_indices]

        adaboost = AdaBoost(OptimalWeakLearner())
        acc, err, auc = adaboost.boost(X, Y, test, test_target, discrete_features=[0, 3, 4, 5, 6, 8, 9, 11, 12])
        res.append((acc, err, auc))
        param += 0.05

    print res


def cross():
    train, target = load_crx()
    train, target = shuffle(train, target)
    target = np.array(map(lambda v: -1.0 if v == 0 else 1.0, target))

    k = 10
    train_size = len(train)
    test_index_generator = k_fold_cross_validation(train_size, k)
    fold = 1
    overall_acc = 0
    overall_error = 0
    overall_auc = 0

    for start, end in test_index_generator:
        print "====================Fold %s============" % fold
        k_fold_train = np.vstack((train[range(0, start)], train[range(end, train_size)]))
        test = train[range(start, end)]
        train_target = np.append(target[range(0, start)], target[range(end, train_size)])
        test_target = target[range(start, end)]

        adaboost = AdaBoost(OptimalWeakLearner())
        acc, err, auc = adaboost.boost(k_fold_train, train_target, test, test_target)

        overall_auc += auc
        overall_acc += acc
        overall_error += err
        fold += 1

    print "Overall test accuracy: %s, overall test error: %s, overall test auc: %s" % (
        overall_acc / k, overall_error / k, overall_auc / k)


def entire():
    data, target = load_crx()
    train, test, train_target, test_target = train_test_shuffle_split(data, target, len(data) / 10)
    train_target = np.array(map(lambda v: -1.0 if v == 0 else 1.0, train_target))
    test_target = np.array(map(lambda v: -1.0 if v == 0 else 1.0, test_target))

    adaboost = AdaBoost(OptimalWeakLearner())
    adaboost.boost(train, train_target, test, test_target, discrete_features=range(train.shape[1]))


if __name__ == '__main__':
    cross()
