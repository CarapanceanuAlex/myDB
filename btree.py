class BTreeNode:
    def __init__(self, keys=None, children=None, isleaf=True):
        self.keys = keys if keys is not None else []
        self.children = children if children is not None else []
        self.isleaf = isleaf

class BTree:
    def __init__(self,maxkeys = 3):
        self.root = BTreeNode()
        self.maxkeys = maxkeys

    def search_key(self, key):
        return self._search_node(self.root, key)

    def _search_node(self, node, key):
        for i in range(len(node.keys)):
            if node.keys[i] == key:
                return node.keys[i]
            elif key < node.keys[i]:
                return self._search_node(node.children[i], key)
        if node.isleaf == False:
            return self._search_node(node.children[len(node.keys)], key)
        elif node.isleaf == True:
            return None