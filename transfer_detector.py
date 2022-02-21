from typing import List
from collections import namedtuple
from datetime import datetime

bitcoin_transaction = namedtuple('bitcoin_transaction', ['txn_id', 'wallet_id', 'txn_time', 'txn_type', 'txn_amount'])


def construct_bitcoin_transaction(txn: dict) -> bitcoin_transaction:
    """Constructs the bitcoin transaction namedtuple from the given txn dictionary."""
    return bitcoin_transaction(txn['txn_id'], txn['wallet_id'],
                               datetime.strptime(txn['txn_time'], '%Y-%m-%d %H:%M:%S %Z'), txn['txn_type'],
                               txn['txn_amount'])


def detect_transfers(transactions: List[dict]) -> List[tuple]:
    """Detects transfers amongst the given transactions and returns a list of tuples containing the txn id's of the
    transfers"""
    bitcoin_transactions = [construct_bitcoin_transaction(txn) for txn in transactions]
    out_transactions_dict = {}
    in_transactions_dict = {}
    for txn in bitcoin_transactions:
        key = f'{txn.txn_time}{txn.txn_amount}'
        if txn.txn_type == 'out':
            out_transactions_list = out_transactions_dict.get(key, [])
            out_transactions_list.append(txn)
            out_transactions_dict[key] = out_transactions_list
        elif txn.txn_type == 'in':
            in_transactions_list = in_transactions_dict.get(key, [])
            in_transactions_list.append(txn)
            in_transactions_dict[key] = in_transactions_list
        else:
            raise ValueError(f'Unrecognized txn type : {txn.txn_type}')

    transfers = []

    # Check for every out transaction if there is a corresponding in transaction
    for out_txn_key in out_transactions_dict.keys():
        if out_txn_key in in_transactions_dict:
            out_txns = out_transactions_dict[out_txn_key]
            in_txns = in_transactions_dict[out_txn_key]
            min_transfers = min(len(out_txns), len(in_txns))
            for i in range(min_transfers):
                transfers.append((out_txns[i].txn_id, in_txns[i].txn_id))
    return transfers


###########################################################################################################
########################################## Test Cases #####################################################
###########################################################################################################


def test_one_transfer_exists():
    """Test that one transfer exists in the given list of transactions"""
    TEST_NAME = "One transfer record exists"
    print(f'Running test : {TEST_NAME}')
    txns = [
        {'txn_id': 'tx_id_1', 'wallet_id': 'wallet_id_1', 'txn_time': '2020-01-01 15:30:20 UTC', 'txn_type': 'out', 'txn_amount': 5.3},
        {'txn_id': 'tx_id_2', 'wallet_id': 'wallet_id_1', 'txn_time': '2020-01-03 12:05:25 UTC', 'txn_type': 'out', 'txn_amount': 3.2},
        {'txn_id': 'tx_id_3', 'wallet_id': 'wallet_id_2', 'txn_time': '2020-01-01 15:30:20 UTC', 'txn_type': 'in', 'txn_amount': 5.3},
        {'txn_id': 'tx_id_4', 'wallet_id': 'wallet_id_3', 'txn_time': '2020-01-01 15:30:20 UTC', 'txn_type': 'in', 'txn_amount': 5.3},
    ]
    expected_ans = [('tx_id_1', 'tx_id_3')]
    assert expected_ans == detect_transfers(txns)
    print(f'Test case : {TEST_NAME} succeeded !')


def test_no_transfer_exists():
    """Test that no transfer exists in the given list of transactions."""
    TEST_NAME = "No transfer record exists."
    print(f'Running test : {TEST_NAME}')
    txns = [
        {'txn_id': 'tx_id_1', 'wallet_id': 'wallet_id_1', 'txn_time': '2020-01-01 15:30:21 UTC', 'txn_type': 'out',
         'txn_amount': 5.3},
        {'txn_id': 'tx_id_2', 'wallet_id': 'wallet_id_1', 'txn_time': '2020-01-03 12:05:25 UTC', 'txn_type': 'out',
         'txn_amount': 3.2},
        {'txn_id': 'tx_id_3', 'wallet_id': 'wallet_id_2', 'txn_time': '2020-01-01 15:30:22 UTC', 'txn_type': 'in',
         'txn_amount': 5.3},
        {'txn_id': 'tx_id_4', 'wallet_id': 'wallet_id_3', 'txn_time': '2020-01-01 15:30:20 UTC', 'txn_type': 'in',
         'txn_amount': 5.3},
    ]
    expected_ans = []
    assert expected_ans == detect_transfers(txns)
    print(f'Test case : {TEST_NAME} succeeded !')


def test_that_more_than_one_transfer_exists():
    """Test that more than on transfer transaction exists in the given list of transactions."""
    TEST_NAME = "More than one transfer record exists"
    print(f'Running test : {TEST_NAME}')
    txns = [
        {'txn_id': 'tx_id_1', 'wallet_id': 'wallet_id_1', 'txn_time': '2020-01-01 15:30:20 UTC', 'txn_type': 'out',
         'txn_amount': 5.3},
        {'txn_id': 'tx_id_2', 'wallet_id': 'wallet_id_1', 'txn_time': '2020-01-03 12:05:25 UTC', 'txn_type': 'out',
         'txn_amount': 3.2},
        {'txn_id': 'tx_id_3', 'wallet_id': 'wallet_id_2', 'txn_time': '2020-01-01 15:30:20 UTC', 'txn_type': 'in',
         'txn_amount': 5.3},
        {'txn_id': 'tx_id_4', 'wallet_id': 'wallet_id_3', 'txn_time': '2020-01-03 12:05:25 UTC', 'txn_type': 'in',
         'txn_amount': 3.2},
    ]
    expected_ans = [('tx_id_1', 'tx_id_3'), ('tx_id_2', 'tx_id_4')]
    assert expected_ans == detect_transfers(txns)
    print(f'Test case : {TEST_NAME} succeeded !')


if __name__ == '__main__':
    test_one_transfer_exists()
    test_no_transfer_exists()
    test_that_more_than_one_transfer_exists()



