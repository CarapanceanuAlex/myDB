class BTreeNode:
    def __init__(self, keys=None, children=None, isleaf=True):
        self.keys = keys if keys is not None else []
        self.children = children if children is not None else []
        self.isleaf = isleaf

class BTree:
    def __init__(self,maxkeys = 3):
        self.root = BTreeNode()
        self.maxkeys = maxkeys

#----------------------------------------------------------------------------------
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

#----------------------------------------------------------------------------------
    def insert(self, key):
        self._insert_node(self.root, key)
        if len(self.root.keys) > self.maxkeys:
            new_root = BTreeNode(isleaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root

    def _insert_node(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if node.isleaf:
            node.keys.insert(i, key)
        else:
            self._insert_node(node.children[i], key)
            if len(node.children[i].keys) > self.maxkeys:
                self._split_child(node, i)

    def _split_child(self, parent, i):
        child = parent.children[i]
        mid = self.maxkeys // 2
        mid_key = child.keys[mid]

        left = BTreeNode(keys=child.keys[:mid], children=child.children[:mid+1], isleaf=child.isleaf)
        right = BTreeNode(keys=child.keys[mid+1:], children=child.children[mid+1:], isleaf=child.isleaf)

        parent.keys.insert(i, mid_key)
        parent.children[i] = left
        parent.children.insert(i+1, right)