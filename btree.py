class BTreeNode:
    def __init__(self, keys=None, children=None, isleaf=True):
        self.keys = keys if keys is not None else []
        self.children = children if children is not None else []
        self.isleaf = isleaf

class BTree:
    def __init__(self,maxkeys = 3):
        self.root = BTreeNode()
        self.maxkeys = maxkeys
        self.t = (maxkeys + 1) // 2      # minimum degree
        self.min_keys = self.t - 1       # min keys a non-root node must hold

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

#----------------------------------------------------------------------------------
    def delete(self, key):
        self._delete_node(self.root, key)
        # if root became empty and has a child, shrink the tree's height
        if len(self.root.keys) == 0 and not self.root.isleaf:
            self.root = self.root.children[0]
 
    def _delete_node(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
 
        if i < len(node.keys) and node.keys[i] == key:
            # key found in this node
            if node.isleaf:
                node.keys.pop(i)
            else:
                self._delete_from_internal(node, i)
        else:
            if node.isleaf:
                raise ValueError("Key not found")
            # make sure the child we're about to descend into has enough keys
            self._fill_child(node, i)
            # after filling, the key might have shifted position if a merge happened
            if i > len(node.keys):
                i -= 1
            self._delete_node(node.children[i], key)
 
    def _delete_from_internal(self, node, i):
        key = node.keys[i]
        left_child = node.children[i]
        right_child = node.children[i+1]
 
        if len(left_child.keys) > self.min_keys:
            pred = self._get_predecessor(left_child)
            node.keys[i] = pred
            self._delete_node(left_child, pred)
        elif len(right_child.keys) > self.min_keys:
            succ = self._get_successor(right_child)
            node.keys[i] = succ
            self._delete_node(right_child, succ)
        else:
            self._merge(node, i)
            self._delete_node(left_child, key)
 
    def _get_predecessor(self, node):
        while not node.isleaf:
            node = node.children[-1]
        return node.keys[-1]
 
    def _get_successor(self, node):
        while not node.isleaf:
            node = node.children[0]
        return node.keys[0]
 
    def _fill_child(self, node, i):
        child = node.children[i]
        if len(child.keys) > self.min_keys:
            return  # already has enough, nothing to do
 
        if i > 0 and len(node.children[i-1].keys) > self.min_keys:
            self._borrow_from_prev(node, i)
        elif i < len(node.keys) and len(node.children[i+1].keys) > self.min_keys:
            self._borrow_from_next(node, i)
        else:
            if i < len(node.keys):
                self._merge(node, i)
            else:
                self._merge(node, i-1)
 
    def _borrow_from_prev(self, node, i):
        child = node.children[i]
        sibling = node.children[i-1]
 
        child.keys.insert(0, node.keys[i-1])
        if not sibling.isleaf:
            child.children.insert(0, sibling.children.pop())
        node.keys[i-1] = sibling.keys.pop()
 
    def _borrow_from_next(self, node, i):
        child = node.children[i]
        sibling = node.children[i+1]
 
        child.keys.append(node.keys[i])
        if not sibling.isleaf:
            child.children.append(sibling.children.pop(0))
        node.keys[i] = sibling.keys.pop(0)
 
    def _merge(self, node, i):
        left = node.children[i]
        right = node.children[i+1]
 
        left.keys.append(node.keys.pop(i))
        left.keys.extend(right.keys)
        left.children.extend(right.children)
 
        node.children.pop(i+1)
