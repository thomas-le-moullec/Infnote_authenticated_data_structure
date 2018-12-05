from src.mt_tools import MtTools


class Client:
    def __init__(self):
        self.proof_hashes = []
        self.last_index = 0

    def _store_proof_hashes(self, hash_post):
        """
        Basically need to do a get_proof_hashes_by_index where index is equal to last index + 1.
        proof_hashes should then take the value of the path.
        :param hash_post:
        :return:
        """
        # with last_index we know how many leaves we have,
        # so we know how many level we have and how many leaves per level
        # We are looking to find the siblings of the potential last node, basically fake an insertion.
        # steps:
        # 0) Found the level and index where to start for the new node.
        # 1) Loop through levels starting by the correct level and index found before
        # 2) Get the index_on_level of the sibling that we are looking at
        # 3) Check if the node is an odd end node,
        #    in this case we should go to the next level and divide index_on_lvl by 2.
        # 4) Append in proof_hashes the value of the position and the value of the sibling
        index = 1
        self.proof_hashes.append({MtTools.get_sibling_pos(index): hash_post})

    def check_post(self, hash_post, merkle_root):
        print("Current Stored hash:"+str(self.proof_hashes)+" Merkle root to achieve:"+str(merkle_root)
              + "hash_post to check:"+str(hash_post))
        # Store the correct hashes in proof_hashes
        result = MtTools.validate_proof(self.proof_hashes, hash_post, merkle_root)
        self._store_proof_hashes(hash_post)
        return result
