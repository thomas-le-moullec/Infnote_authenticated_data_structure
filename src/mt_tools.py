import math
from enum import Enum
import hashlib


class Position(Enum):
    LEFT = 0
    RIGHT = 1


class Encode:
    def __init__(self):
        pass

    @staticmethod
    def sha256(data):
        return hashlib.sha256(data.encode()).hexdigest()


class MtTools:
    def __init__(self):
        pass

    @staticmethod
    def get_max_level(leaves_nbr):
        if leaves_nbr == 0:
            return 0
        """
        Get the number of levels in our tree based in the number of leaves
        :param leaves_nbr: Leaves Number in the tree
        :return: Number of levels, rounded
        """
        return int(math.log(leaves_nbr, 2) + 0.5)

    @staticmethod
    def get_level_by_index(index, total_leaves_nbr):
        """
        0 if the index of the merkle root. If index == 0 you reached the good level.
        Else you need to obtain 2 subtrees by the division and update the number of nodes.
        :param index: Index that we are looking for
        :param total_leaves_nbr: Total number of leaves in the tree
        :return: specific level for a specific index in a tree
        """
        level = 0
        while index > 0:
            index -= 1
            total_leaves_nbr = (total_leaves_nbr - 1) / 2
            index = index % total_leaves_nbr
            level += 1
        return level

    @staticmethod
    def get_nodes_nbr_on_level(level):
        """
        :param level: Specific level
        :return: Return the number of nodes on a specific level
        """
        return math.pow(level, 2)

    @staticmethod
    def get_nodes_nbr_until_level(level):
        """
        Method to give the number of nodes until a specific level is reached.
        :param level: specific level
        :return: Number of nodes
        """
        result = math.pow(level + 1, 2) - 1
        return result

    @staticmethod
    def get_total_nbr_of_nodes(leaves_nbr):
        """
        :param leaves_nbr: Number of leaves inserted in the tree
        :return: return the total number of nodes - hashes in the tree
        """
        nbr_nodes = pow(2, math.log(leaves_nbr, 2) + 1) - 1
        return round(nbr_nodes)

    @staticmethod
    def is_right_node(index):
        """
        :param index: Just the index of the node.
        :return: Return 0 or 1 based on the index value, if odd return 1 else 0
        """
        return index % 2

    @staticmethod
    def is_odd_end_node(index, height_len):
        """
        Method to check if a node at a specific index is an odd end node or not.
        :param index: index at a height in the tree
        :param height_len: number of nodes at the same height
        :return: Return true if index if the last element of the level and if the number of nodes on this level is odd.
        """
        if (index == height_len - 1) and (height_len % 2 == 1):
            return True
        return False

    @staticmethod
    def get_sibling_index(index):
        """
        Purpose is to get the index of the sibling based on the node index.
        If node is left then sibling index is equal to index + 1, else index - 1
        :param index:
        :return:
        """
        if MtTools.is_right_node(index):
            return index - 1
        return index + 1

    @staticmethod
    def get_sibling_pos(index):
        """
        Get the position of the sibling based on the node index.
        :param index: Node index
        :return: LEFT or RIGHT - Basically returning the opposition position of the node
        """
        if MtTools.is_right_node(index):
            return Position.LEFT
        return Position.RIGHT

    @staticmethod
    def get_proof_hash_by_sibling(proof, target_hash, hash_func=Encode.sha256):
        """
        Generate the correct child of target_hash and the proof fetched from the given array in validate_proof.
        Check the position of the proof with the enum.
        :param proof: Pair hash that we use to check the target_hash.
        :param target_hash: Hash previously generated or received to check.
        :param hash_func: Hash function produce child
        :return: Child of the two parents : target_hash and its sibling.
        """
        if Position.RIGHT in proof:
            sibling = proof[Position.RIGHT]
            proof_hash = hash_func(target_hash + sibling)
        else:
            print("Proof:"+str(proof))
            sibling = proof[Position.LEFT]
            proof_hash = hash_func(sibling + target_hash)
        return proof_hash

    @staticmethod
    def validate_proof(proof_hashes, target_hash, merkle_root, hash_it=False):
        """
        Method called by a node to check if the received data is correct.
        To check the validity, this method is computing the merkle_root with the proof_hashes array.
        E.g:    This proof_hashes can be stored locally by a node and the target hash can be received by another node.
                We are then checking if the compute merkle_tree is the same as the one from the other node.
        :param proof_hashes: Array of proof, Basically the path of siblings to validate the merkle root.
        :param target_hash: The data to validate.
        :param merkle_root: Merkle root of the Server.
        :param hash_it: Can deliver a target_data hashed or not. if True the target_hash need to be hash.
        :return: True if the merkle_root is indeed the same as the other node. False if differs.
        """
        if hash_it:
            target_hash = Encode.sha256(target_hash)
        proof_hash = target_hash
        print("Path in Validate proof:" + str(proof_hashes))
        if len(proof_hashes) == 0:
            return target_hash == merkle_root
        for proof in proof_hashes:
            proof_hash = MtTools.get_proof_hash_by_sibling(proof, proof_hash)
        return proof_hash == merkle_root
