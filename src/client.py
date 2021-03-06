from src.mt_tools import MtTools, Encode, Enum


class Client:
    def __init__(self):
        self.proof_hashes = []
        self.nbr_leaves = 0
        self.nbr_lvl = 0

    def _set_nbr_lvl(self):
        self.nbr_lvl = MtTools.get_max_level(self.nbr_leaves)

    def _check_nth_post(self, index, hash_post):
        new_hashes = []
        if index == 0:
            new_hashes.append({0: hash_post})
            return new_hashes
        while index > 0:
            index -= 1
            self.nbr_leaves = (self.nbr_leaves - 1) / 2 + 0.5
            index = index % self.nbr_leaves
            """if MtTools.is_right_node(index):
                new_hashes.append(
                    {MtTools.get_sibling_pos(index): Encode.sha256(self.proof_hashes[index] + hash_post)})
            else:
                new_hashes.append(
                    {MtTools.get_sibling_pos(index): Encode.sha256(self.proof_hashes[index] + hash_post)})"""

        return new_hashes

    def _store_proof_hashes(self, hash_post):
        """
        Basically need to do a get_proof_hashes_by_index where index is equal to nbr_leaves.
        proof_hashes should then take the value of the path.
        :param hash_post:
        :return:
        """
        # with nbr_leaves we know how many leaves we have,
        # so we know how many level we have and how many leaves per level
        # We are looking to find the siblings of the potential last node
        # steps:
        # 0) Found the level and index where to start for the new node.
        # 1) Loop through levels starting by the correct level and index found before
        # 2) Get the index_on_level of the sibling that we are looking at
        # 3) Check if the node is an odd end node,
        #    in this case we should go to the next level and divide index_on_lvl by 2.
        # 4) Append in proof_hashes the value of the position and the value of the sibling
        self.nbr_leaves += 1
        self._set_nbr_lvl()
        index = self.nbr_leaves -1  # We want to add the post at the end of the tree
        self.proof_hashes = self._check_nth_post(index, hash_post)
        self.proof_hashes = []
        print("We are storing this hashes in Client:"+str(self.proof_hashes))

    def add_post(self, hash_post, merkle_root):
        print("Current Stored hash:"+str(self.proof_hashes)+" Merkle root to achieve:"+str(merkle_root)
              + "hash_post to check:"+str(hash_post))
        # Store the correct hashes in proof_hashes
        result = MtTools.validate_proof(self.proof_hashes, hash_post, merkle_root)
        self._store_proof_hashes(hash_post)  # Anticipate the next post insertion
        return result
