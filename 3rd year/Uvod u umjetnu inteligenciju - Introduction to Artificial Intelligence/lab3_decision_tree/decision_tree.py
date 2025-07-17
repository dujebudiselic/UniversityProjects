import sys
import math


class Leaf:
    def __init__(self, v):
        self.v = v

    def get_v(self):
        return self.v


class Node:
    def __init__(self, x, subtrees, depth, D):
        self.x = x
        self.subtrees = subtrees
        self.depth = depth
        self.D = D

    def get_subtrees(self):
        return self.subtrees

    def get_depth(self):
        return self.depth

    def get_D(self):
        return self.D

    def get_x(self):
        return self.x


def print_tree(node, output=''):
    for v, t in node.get_subtrees():
        if isinstance(t, Node):
            print_tree(t, output + str(node.get_depth() + 1) + ':' + node.get_x() + '=' + v + ' ')
        if isinstance(t, Leaf):
            print(output + str(node.get_depth() + 1) + ':' + node.get_x() + '=' + v + ' ' + t.get_v())

class ID3:
    def __init__(self, restriction=None):
        self.model = Node
        self.restriction = restriction
        self.y = []

    def E(self, total, number_y):
        e = 0
        for p in number_y.values():
            p = p / total
            if p == 0:
                e = e - 0
            else:
                e = e - p * math.log2(p)
        return e

    def entropy_after_split(self, D, number_x_y, kind_x, index):
        enk = 0
        for x in kind_x:
            total = 0
            for row in D:
                if row[index] == x:
                    total += 1
            r = 0
            for y in number_x_y[x].keys():
                r += number_x_y[x][y]
            p = r / len(D)
            enk += p * self.E(total, number_x_y[x])

        return enk

    def IG(self, D, X, number_y):
        E = self.E(len(D), number_y)
        index_goal = len(D[0]) - 1
        info_gain_per_X = {}
        kind_x = {}

        for i, x in enumerate(X):
            if x != '':
                number_x_y = {}
                kind_x[x] = []
                for row in D:
                    if not row[i] in number_x_y:
                        number_x_y[row[i]] = {}
                        kind_x[x].append(row[i])
                        if not row[index_goal] in number_x_y[row[i]]:
                            number_x_y[row[i]][row[index_goal]] = 1
                    else:
                        if not row[index_goal] in number_x_y[row[i]]:
                            number_x_y[row[i]][row[index_goal]] = 1
                        else:
                            number_x_y[row[i]][row[index_goal]] = number_x_y[row[i]][row[index_goal]] + 1
                enk = self.entropy_after_split(D, number_x_y, kind_x[x], i)
                ig = E - enk
                ig = round(ig, 4)
                info_gain_per_X[x] = ig

        info_gain_per_X = dict(sorted(info_gain_per_X.items()))
        x = max(info_gain_per_X, key = info_gain_per_X.get)
        return x, kind_x[x]

    def id3(self, D, Dparent, X, y, depth):
        if self.restriction is not None and depth == int(self.restriction):
            i = len(D[0]) - 1
            v = {}
            for kind in y:
                v[kind] = 0
            for row in D:
                v[row[i]] += 1
            v = max(v, key = v.get)
            return Leaf(v)

        if len(D) == 0:
            i = len(Dparent[0]) - 1
            v = {}
            for kind in y:
                v[kind] = 0
            for row in Dparent:
                v[row[i]] += 1
            v = max(v, key = v.get)
            return Leaf(v)

        i = len(D[0]) - 1
        number_y = {}
        for kind in y:
            number_y[kind] = 0
        for row in D:
            number_y[row[i]] += 1
        v = max(number_y, key = number_y.get)
        if (len(X) > 1 and len(set(X)) == 1) or number_y[v] == len(D):
            return Leaf(v)

        x, V = self.IG(D, X, number_y)
        subtrees = []
        X_new = []
        for feature in X:
            if feature == x:
                X_new.append('')
            else:
                X_new.append(feature)
        index = X.index(x)
        for v in V:
            D_v = []
            for row in D:
                if v == row[index]:
                    D_v.append(row)
            t = self.id3(D_v, D, X_new, y, depth + 1)
            subtrees.append((v, t))
        return Node(x, subtrees, depth, D)

    def fit(self, feature_names, features):
        X = feature_names[:-1]
        i = len(feature_names) - 1
        y = []
        for kind in features:
            if not kind[i] in y:
                y.append(kind[i])
        y.sort()
        self.y = y 
        self.modal = self.id3(features, features, X, y, 0)
        print('[BRANCHES]:')
        print_tree(self.modal)

    def find_goal(self, feature_names_test, row, node):
        x = node.get_x()
        index = feature_names_test.index(x)
        rez = ''
        list_v = []
        for v, t in node.get_subtrees():
            list_v.append(v)
            if v == row[index]:
                if isinstance(t, Node):
                    rez = self.find_goal(feature_names_test, row, t)
                if isinstance(t, Leaf):
                    return t.get_v()
                if rez in self.y:
                    return rez

        if not row[index] in list_v:
            i = len(feature_names_test) - 1
            v = {}
            for kind in self.y:
                v[kind] = 0
            for d in node.get_D():
                v[d[i]] = v[d[i]] + 1
            v = max(v, key = v.get)
            return v

    def confusion_matrix(self, predictions, feature_names_test, features_test, y_test):
        index = len(feature_names_test) - 1
        i = 0
        matrix = {}
        for kind1 in y_test:
            for kind2 in y_test:
                if kind1 not in matrix:
                    matrix[kind1] = {}
                if kind2 not in matrix[kind1]:
                    matrix[kind1][kind2] = 0
        for row in features_test:
            matrix[row[index]][predictions[i]] += 1
            i += 1
        print('[CONFUSION_MATRIX]:')
        for actual in matrix:
            red = []
            for pred in matrix[actual]:
                red.append(str(matrix[actual][pred]))
            print(" ".join(red))

    def get_accuracy(self, predictions, feature_names_test, features_test):
        index = len(feature_names_test) - 1
        correct = 0
        i = 0
        for row in features_test:
            if predictions[i] == row[index]:
                correct += 1
            i += 1
        accuracy = correct / len(features_test)
        print(f"[ACCURACY]: {accuracy:.5f}")

    def predict(self, feature_names_test, features_test):
        i = len(feature_names_test) - 1
        y_test = []
        for kind in features_test:
            if not kind[i] in y_test:
                y_test.append(kind[i])
        y_test.sort()
        predictions = []
        for row in features_test:
            pred = self.find_goal(feature_names_test, row, self.modal)
            predictions.append(pred)
        print('[PREDICTIONS]:', ' '.join(predictions))
        self.get_accuracy(predictions, feature_names_test, features_test)
        self.confusion_matrix(predictions, feature_names_test, features_test, y_test)
        return predictions


def get_features(path):
    is_first_line = True
    with open(path, 'r', encoding='utf-8') as f:
        features = []
        for line in f:
            line = line.strip()
            if not line.startswith("#"):
                if is_first_line:
                    feature_names = line.split(',')
                    is_first_line = False
                else:
                    values = line.split(',')
                    features.append(values)

    return feature_names, features


def get_features_test(path_test):
    is_first_line = True
    with open(path_test, 'r', encoding='utf-8') as f:
        features_test = []
        for line in f:
            line = line.strip()
            if not line.startswith("#"):
                if is_first_line:
                    feature_names_test = line.split(',')
                    is_first_line = False
                else:
                    values = line.split(',')
                    features_test.append(values)

    return feature_names_test, features_test


entry = sys.argv

if len(entry) == 3:
    train_path = entry[1]
    test_path = entry[2]

    feature_names, features = get_features(train_path)
    feature_names_test, features_test = get_features_test(test_path)

    model = ID3()
    model.fit(feature_names, features)
    predictions = model.predict(feature_names_test, features_test)

elif len(entry) == 4:
    train_path = entry[1]
    test_path = entry[2]
    restriction = entry[3]

    feature_names, features = get_features(train_path)
    feature_names_test, features_test = get_features_test(test_path)

    model = ID3(restriction)
    model.fit(feature_names, features)
    predictions = model.predict(feature_names_test, features_test)
