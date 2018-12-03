from src import encryption
from enum import Enum


class Position(Enum):
    LEFT = 0
    RIGHT = 1


def is_right_node(index):
    return index % 2


def is_odd_end_node(index, height_len):
    if (index == height_len - 1) and (height_len % 2 == 1):
        return True
    return False


def get_sibling_index(index):
    if is_right_node(index):
        return index - 1
    return index + 1


def get_sibling_pos(index):
    if is_right_node(index):
        return Position.LEFT
    return Position.RIGHT


def get_proof_hash_by_sibling(proof, target_hash, hash_func=encryption.Encode.sha256):
    if Position.RIGHT in proof:
        sibling = proof[Position.RIGHT]
        proof_hash = hash_func(target_hash + sibling)
    else:
        sibling = proof[Position.LEFT]
        proof_hash = hash_func(sibling + target_hash)
    return proof_hash


def validate_proof(proof_hashes, target_hash, merkle_root):
    print("Path in Validate proof:"+str(proof_hashes))
    if len(proof_hashes) == 0:
        return target_hash == merkle_root
    proof_hash = target_hash
    for proof in proof_hashes:
        proof_hash = get_proof_hash_by_sibling(proof, proof_hash)

    return proof_hash == merkle_root


class MerkleTree:
    def __init__(self):
        self.leaves = list()
        self.tree = []
        self.is_built = False
        self.hash_function = encryption.Encode.sha256

    def reset_tree(self):
        self.leaves = list()
        self.tree = None
        self.is_built = False

    def update_tree(self, values, hash_it=False):
        self.add_leaf(values, hash_it)
        self.build_tree()

    def add_leaf(self, values, hash_it=False):
        self.is_built = False
        # Transform the single leaf in a list
        if not isinstance(values, tuple) and not isinstance(values, list):
            values = [values]
        for v in values:
            # If data is not hashed yet
            if hash_it:
                v = self.hash_function(v)
            self.leaves.append(v)

    def get_hash_function(self):
        return self.hash_function

    def get_sibling_value(self, level, index):
        return self.tree[level][get_sibling_index(index)]

    def get_leaf_nbr(self):
        return len(self.leaves)

    def _get_new_level(self, solo_leaf, last_height, nbr_leaves_lvl):
        new_level = []
        # Group two nodes, the two futures parents
        print("last_height before:"+str(last_height))
        for left, right in zip(last_height[0:nbr_leaves_lvl:2], last_height[1:nbr_leaves_lvl:2]):
            new_level.append(self.hash_function(left + right))
        if solo_leaf is not None:  # promote the solo leaf to the next level.
            new_level.append(solo_leaf)
        return new_level

    def _create_next_height(self):
        solo_leaf = None
        last_height = self.tree[0]
        nbr_leaves_lvl = len(last_height)  # number of leaves on the level
        if nbr_leaves_lvl % 2 == 1:
            # if odd number of leaves on the level;
            # We are storing solo leaf to promote it to the next level, we decrease number of leaves for current level.
            solo_leaf = last_height[-1]
            nbr_leaves_lvl -= 1
        new_height = self._get_new_level(solo_leaf, last_height, nbr_leaves_lvl)
        self.tree = [new_height, ] + self.tree  # prepend new level

    def build_tree(self):
        self.is_built = False
        if self.get_leaf_nbr() > 0:
            # Get first level: the leaves
            self.tree = [self.leaves, ]
            print("Leaves: " + str(self.leaves))
            # Creating the children for each level until root is reached
            while len(self.tree[0]) > 1:
                self._create_next_height()
        print("-----")
        print("Final Height :"+str(self.tree))
        print("-----")
        self.is_built = True

    def get_merkle_root(self):
        if self.is_built:
            if self.tree is not None:
                return self.tree[0][0]
            return None
        return None

    def get_leaf_by_index(self, index):
        return self.leaves[index]

    def _check_valid_search(self, index):
        if self.tree is None:
            return False
        elif not self.is_built or index > len(self.leaves) - 1 or index < 0:
            return False
        return True

    def get_proof_by_index(self, index):
        if not self._check_valid_search(index):
            return None
        proof_hashes = []
        index_on_lvl = index
        for level in range(len(self.tree) - 1, 0, -1):
            height_len = len(self.tree[level])
            if is_odd_end_node(index_on_lvl, height_len):
                index_on_lvl = int(index_on_lvl / 2.)
                continue
            proof_hashes.append({get_sibling_pos(index_on_lvl): self.get_sibling_value(level, index_on_lvl)})
            index_on_lvl = int(index_on_lvl / 2.)
        return proof_hashes

    def print_tree(self):
        print("/ Print Tree /")
        leaves_nbr = self.get_leaf_nbr()
        print("We have :" + str(leaves_nbr) + " leaves in the tree")
        cnt = 0
        while cnt < leaves_nbr:
            print("leaf(" + str(cnt) + ")_value = " + str(self.get_leaf_by_index(cnt)))
            cnt += 1
        for x in range(0, len(self.tree), +1):
            if x == len(self.tree) - 1:
                print("--- Leaves level{"+str(x)+"}:"+str(self.tree[x]))
            else:
                print("--- Branch level{" + str(x) + "}:" + str(self.tree[x]))
        if self.is_built:
            print("Tree is ready and has been built")
            root_value = self.get_merkle_root()
            print("Digest of the tree:" + str(root_value))
        else:
            print("Tree is not ready and has not been built, So no digest")