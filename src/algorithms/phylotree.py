import fastcluster
import pandas as pd
from ete3 import Tree
from scipy.cluster.hierarchy import to_tree


class Dendrogram:

    def __init__(self, tree=None):
        self._nodes = None
        self._tree = tree
        self._newick = None
        self._ete_tree = None

    @property
    def newick(self):
        if not self._newick:
            self._newick = make_newick(self._tree, "", self._tree.dist, self._nodes)
        return self._newick

    @property
    def ete_tree(self):
        if not self._ete_tree:
            self._ete_tree = Tree(self.newick)
        return self._ete_tree

    def make_tree(self, profile_file):
        profiles = pd.read_csv(profile_file, sep="\t", index_col=0)
        self._nodes = list(profiles.columns)
        distances = distance_matrix(profiles)
        self._tree = construct_tree(distances)

    def to_newick(self, file):
        with open(file, "w") as file:
            file.write(self.newick)

    def render_on(self, file, w=800, h=600, units="px", dpi=300, *args):
        self.ete_tree.render(file, w=w, h=h, units=units, dpi=dpi, *args)


def distance_matrix(profiles):
    distances = pd.DataFrame(index=profiles.columns, columns=profiles.columns)
    for x in profiles.columns:
        for y in profiles.columns:
            distances.loc[x, y] = hamming(profiles[x], profiles[y])
    return distances


def hamming(xs, ys):
    results = 0
    for x, y in zip(xs, ys):
        if type(x) == str and type(y) == str and x == y:
            pass
        elif type(x) == float and type(y) == float:
            pass
        else:
            results += 1
    return results


def construct_tree(distances):
    linkage = fastcluster.average(distances)
    tree = to_tree(linkage, False)
    return tree


def make_newick(node, newick, parentdist, leaf_names):
    if node.is_leaf():
        return "{}:{:.2f}{}".format(leaf_names[node.id], parentdist - node.dist, newick)
    else:
        if len(newick) > 0:
            newick = "):{:.2f}{}".format(parentdist - node.dist, newick)
        else:
            newick = ");"
        newick = make_newick(node.get_left(), newick, node.dist, leaf_names)
        newick = make_newick(node.get_right(), ",{}".format(newick), node.dist, leaf_names)
        newick = "({}".format(newick)
        return newick

