class BTreeNode:
    def __init__(self, keys=None, children=None, isleaf=True):
        self.keys = keys if keys is not None else []
        self.children = children if children is not None else []
        self.isleaf = isleaf

class BTree:
    def __init__(self,maxkeys = 3):
        self.root = BTreeNode()
        self.maxkeys = maxkeys