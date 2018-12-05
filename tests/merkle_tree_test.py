import unittest
from src import merkle_tree, mt_tools
from resources import messages_example, transactions_example
import random


class MerkleTreeTests(unittest.TestCase):

    def test_empty_data_error(self):
        tree = merkle_tree.MerkleTree()
        tree.build_tree()
        self.assertEqual(0, tree.get_leaf_nbr())

    def test_one_elem_valid(self):
        mt = merkle_tree.MerkleTree()
        mt.add_leaf(messages_example.ONE_DATA, True)
        mt.build_tree()
        expected_digest = mt_tools.Encode.sha256(messages_example.ONE_DATA[0])
        self.assertTrue(mt_tools.MtTools.validate_proof([], expected_digest, mt.get_merkle_root()))
        print("merkle_root:"+str(mt.get_merkle_root())+" digest:"+str(expected_digest))
        self.assertEqual(mt.get_merkle_root(), expected_digest)

    def test_two_element_valid(self):
        mt = merkle_tree.MerkleTree()
        mt.update_tree(messages_example.TWO_DATA, True)
        expected_digest = mt_tools.Encode.sha256((mt_tools.Encode.sha256(messages_example.TWO_DATA[0]) +
                                                  mt_tools.Encode.sha256(messages_example.TWO_DATA[1])))
        self.assertEqual(expected_digest, mt.get_merkle_root())
        self.assertEqual(2, mt.get_leaf_nbr())
        self.assertEqual(mt.get_leaf_by_index(1), mt_tools.Encode.sha256(messages_example.TWO_DATA[1]))

    def test_three_element_valid(self):
        mt = merkle_tree.MerkleTree()
        mt.update_tree(messages_example.THREE_DATA, True)
        expected_digest = mt_tools.Encode.sha256((mt_tools.Encode.sha256
                                                  (mt_tools.Encode.sha256(messages_example.THREE_DATA[0]) +
                                                   mt_tools.Encode.sha256(messages_example.THREE_DATA[1])) +
                                                  mt_tools.Encode.sha256(messages_example.THREE_DATA[2])))
        self.assertEqual(expected_digest, mt.get_merkle_root())
        self.assertEqual(2, mt_tools.MtTools.get_max_level(mt.get_leaf_nbr()))

    def test_six_elements_valid(self):
        mt = merkle_tree.MerkleTree()
        mt.update_tree(messages_example.SIX_DATA, True)
        proof_hashes = mt.get_proof_by_index(mt.get_leaf_nbr()-1)
        target_hash = mt_tools.Encode.sha256(messages_example.SIX_DATA[5])
        self.assertTrue(mt_tools.MtTools.validate_proof(proof_hashes, target_hash, mt.get_merkle_root()))
        self.assertEqual(3, mt_tools.MtTools.get_max_level(mt.get_leaf_nbr()))

    def test_seven_elements_valid(self):
        mt = merkle_tree.MerkleTree()
        mt.update_tree(messages_example.SEVEN_DATA, True)
        proof_hashes = mt.get_proof_by_index(3)
        target_hash = mt_tools.Encode.sha256(messages_example.SIX_DATA[3])
        self.assertTrue(mt_tools.MtTools.validate_proof(proof_hashes, target_hash, mt.get_merkle_root()))
        self.assertEqual(3, mt_tools.MtTools.get_max_level(mt.get_leaf_nbr()))

    def test_three_elements_merkle_proof(self):
        mt = merkle_tree.MerkleTree()
        mt.update_tree(messages_example.THREE_DATA, True)
        last_post = mt_tools.Encode.sha256(messages_example.THREE_DATA[-1])
        proof_hashes = mt.get_proof_by_index(len(messages_example.THREE_DATA) - 1)
        """self.assertTrue(mt_tools.MtTools.validate_proof([mt_tools.Encode.sha256
                                                 (mt_tools.Encode.sha256(messages_example.THREE_DATA[0]) +
                                                  mt_tools.Encode.sha256(messages_example.THREE_DATA[1]))],
                                                mt_tools.Encode.sha256(messages_example.THREE_DATA[2]),
                                                mt.get_merkle_root()))"""
        self.assertTrue(mt_tools.MtTools.validate_proof(proof_hashes, last_post, mt.get_merkle_root()))

    def test_six_elements_merkle_proof(self):
        mt = merkle_tree.MerkleTree()
        mt.update_tree(messages_example.SIX_DATA, True)
        post_valid_hash = mt_tools.Encode.sha256(messages_example.SIX_DATA[3])
        path = mt.get_proof_by_index(3)
        # Correct case where the path is corresponding with the hash of the data
        self.assertTrue(mt_tools.MtTools.validate_proof(path, post_valid_hash, mt.get_merkle_root()))
        path = mt.get_proof_by_index(3)

        # Error case where the path is not corresponding with the hash of the data
        post_error_hash = mt_tools.Encode.sha256(messages_example.SIX_DATA[1])
        self.assertFalse(mt_tools.MtTools.validate_proof(path, post_error_hash, mt.get_merkle_root()))

    def test_seven_elements_build_tree(self):
        mt = merkle_tree.MerkleTree()
        self.assertEqual(0, mt_tools.MtTools.get_max_level(mt.get_leaf_nbr()))
        mt.add_leaf(messages_example.SEVEN_DATA)
        mt.build_tree()
        self.assertEqual(3, mt_tools.MtTools.get_max_level(mt.get_leaf_nbr()))

    def test_all_data_merkle_proof_and_valid_tree(self):
        all_data = [messages_example.TWO_DATA, messages_example.THREE_DATA, messages_example.SIX_DATA,
                    messages_example.SEVEN_DATA, transactions_example.TX_HASHES]
        mt = merkle_tree.MerkleTree()
        false_post = "Not in the tree data"
        false_post = mt_tools.Encode.sha256(false_post)
        for data_row in all_data:
            mt.reset_tree()
            mt.update_tree(data_row, True)
            secure_random = random.randint(0, len(data_row) - 1)
            post = mt_tools.Encode.sha256(data_row[secure_random])
            path = mt.get_proof_by_index(secure_random)
            self.assertTrue(mt_tools.MtTools.validate_proof(path, post, mt.get_merkle_root()))
            path = mt.get_proof_by_index(secure_random)
            self.assertFalse(mt_tools.MtTools.validate_proof(path, false_post, mt.get_merkle_root()))
#            self.assertEqual(mt_tools.MtTools.get_total_nbr_of_nodes(mt.get_leaf_nbr()), tree_len)


if __name__ == "__main__":
    unittest.main()