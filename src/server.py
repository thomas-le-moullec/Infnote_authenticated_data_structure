from src.merkle_tree import MerkleTree
from src.mt_tools import MtTools


class Server:
    def __init__(self):
        self.mt = MerkleTree()

    def reset_data(self):
        self.mt.reset_tree()

    def add_post(self, data, merkle_root):
        self.mt.update_tree(data)
        proof_hashes = self.mt.get_proof_by_index(self.mt.get_leaf_nbr() - 1)
        return MtTools.validate_proof(proof_hashes, data, merkle_root)

    def app_posts(self, data, merkle_root):
        for post in data:
            self.add_post(post, self.mt.get_merkle_root())
        return merkle_root == self.mt.get_merkle_root()