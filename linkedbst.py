"""
File: linkedbst.py
Author: Ken Lambert
"""
import time
from math import log
from random import sample
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s_1 = ""
            if node is not None:
                s_1 += recurse(node.right, level + 1)
                s_1 += "| " * level
                s_1 += str(node.data) + "\n"
                s_1 += recurse(node.left, level + 1)
            return s_1

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftmaxinleftsubtreetotop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentnode = top.left
            while not currentnode.right is None:
                parent = currentnode
                currentnode = currentnode.right
            top.data = currentnode.data
            if parent == top:
                top.left = currentnode.left
            else:
                parent.right = currentnode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemremoved = None
        preroot = BSTNode(None)
        preroot.left = self._root
        parent = preroot
        direction = 'L'
        currentnode = self._root
        while not currentnode is None:
            if currentnode.data == item:
                itemremoved = currentnode.data
                break
            parent = currentnode
            if currentnode.data > item:
                direction = 'L'
                currentnode = currentnode.left
            else:
                direction = 'R'
                currentnode = currentnode.right

        # Return None if the item is absent
        if itemremoved is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentnode.left is None \
                and not currentnode.right is None:
            liftmaxinleftsubtreetotop(currentnode)
        else:

            # Case 2: The node has no left child
            if currentnode.left is None:
                newchild = currentnode.right

                # Case 3: The node has no right child
            else:
                newchild = currentnode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newchild
            else:
                parent.right = newchild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preroot.left
        return itemremoved

    def replace(self, item, newitem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                olddata = probe.data
                probe.data = newitem
                return olddata
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def children(self, p_1):
        """Generate an iteration of Positions representing p's children."""
        if p_1.left is not None:
            yield p_1.left
        if p_1.right is not None:
            yield p_1.right

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        root = self._root
        if root is None:
            return 0

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return 0
            if (top.right is None) and (top.left is None):
                return 0
            else:
                return 1 + max(height1(c) for c in self.children(top))
        return height1(root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        counter = 0
        for _ in self.inorder():
            counter += 1
        height = self.height()
        if height < (2 * log(counter + 1, 2) - 1):
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return [i for i in self.inorder() if i >= low and i <= high]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        tree = self.inorder()
        self.clear()
        new_tree = LinkedStack()
        for element in tree:
            new_tree.push(element)

        def helper(list_tree):
            """additional function"""
            if len(list_tree) == 1:
                self.add(list_tree.pop())
            elif len(list_tree) == 2:
                self.add(list_tree.pop())
                self.add(list_tree.pop())
            else:
                new_stack1 = LinkedStack()
                new_stack2 = LinkedStack()
                index = len(list_tree) // 2
                for i, value in enumerate(list_tree):
                    if i == index:
                        self.add(value)
                    elif i < index:
                        new_stack1.push(value)
                    else:
                        new_stack2.push(value)
                helper(new_stack1)
                helper(new_stack2)
        helper(new_tree)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        new_lst = self.inorder()
        min_value = float('inf')
        for value in new_lst:
            if (value > item) and (value < min_value):
                min_value = value
        if min_value == float('inf'):
            return None
        return min_value

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        new_lst = self.inorder()
        max_value = float('-inf')
        for value in new_lst:
            if (value < item) and (value > max_value):
                max_value = value
        if max_value == float('-inf'):
            return None
        return max_value

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        data = []
        with open(path, 'r', encoding='utf-8') as file:
            our_data = file.readlines()
        for i in our_data:
            data.append(i.strip())
        all_words = sample(data, 10000)
        sorted_data = sorted(data)
        start_time1 = time.time()
        result = []
        for words in sorted_data:
            if words in all_words:
                result.append(words)
        finish_time1 = time.time()
        time1 = finish_time1 - start_time1
        #second part
        tree2 = LinkedBST()
        for elements in sorted_data:
            tree2.add_to_tree(elements)
        start_time2 = time.time()
        for value in all_words:
            tree2.find_in_tree(value)
        finish_time2 = time.time()
        time2 = finish_time2 - start_time2
        #third part
        tree3 = LinkedBST()
        for word_ele in tree3:
            tree3.add(word_ele)
        start_time3 = time.time()
        result3 = []
        for w_element in tree3:
            if w_element in all_words:
                result3.append(w_element)
        finish_time3 = time.time()
        time3 = finish_time3 - start_time3
        #fourth part
        tree3.new_rebalance()
        start_time4 = time.time()
        result4 = []
        for w_element in tree3:
            if w_element in all_words:
                result4.append(w_element)
        finish_time4 = time.time()
        time4 = finish_time4 - start_time4
        return time1, time2, time3, time4

    def add_to_tree(self, item):
        """add alpha to tree"""
        if self.isEmpty():
            self._root = BSTNode(item)
            node = self._root
        else:
            node = self._root
            while node.right is not None:
                node = node.right
            node.right = BSTNode(item)
        self._size += 1

    def find_in_tree(self, item):
        """find item in tree"""
        node = self._root
        while node.data is not None:
            if item == node.data:
                return node.data
            else:
                node = node.right

    def new_rebalance(self):
        """new method for rebalance of tree"""
        tree = self.inorder()
        self.clear()
        new_tree = []
        for element in tree:
            new_tree.append(element)
        temp = [new_tree]
        while len(temp) != 0:
            temp_element = temp.pop(0)
            if temp_element == []:
                continue
            middle = len(temp_element) // 2
            self.add(temp_element[middle])
            if temp_element[:middle] != []:
                temp.append(temp_element[:middle])
            if temp_element[middle + 1:] != []:
                temp.append(temp_element[middle + 1:])
