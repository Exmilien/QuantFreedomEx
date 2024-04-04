from requests import get

from quantfreedom.exchanges.exchange import Exchange


class BSC_Scan:
    url = "https://api.bscscan.com/api"

    def __init__(
        self,
        api_key: str,
    ) -> None:
        self.api_key = api_key

    def check_contract_execution_status(self, tx_hash: str):
        """
        [Check Contract Execution Status](https://docs.bscscan.com/api-endpoints/stats#check-contract-execution-status)
        """
        params = {
            "module": "transaction",
            "action": "getstatus",
            "apikey": self.api_key,
            "txhash": tx_hash,
        }
        response = get(url=self.url, params=params).json()
        try:
            result = response["result"]["isError"]
            if result == "0":
                return True
            else:
                return False
        except Exception as e:
            raise Exception(
                f"Response -> {response['message']} - Exception for check_contract_execution_status -> {e} "
            )

    def check_transaction_receipt_status(
        self,
        tx_hash: str,
    ):
        """
        [Check Transaction Receipt Status](https://docs.bscscan.com/api-endpoints/stats#check-transaction-receipt-status)
        """
        params = {
            "module": "transaction",
            "action": "gettxreceiptstatus",
            "apikey": self.api_key,
            "txhash": tx_hash,
        }
        response = get(url=self.url, params=params).json()
        try:
            result = response["result"]["status"]
            if result == "1":
                return True
            else:
                return False
        except Exception as e:
            raise Exception(
                f"Response -> {response['message']} - Exception for check_transaction_receipt_status -> {e} "
            )

    def get_transactions(
        self,
        address: str = "0x7192b3AA5878293075951b53dEcefb09F3C6F37c",
        contractaddress: str = "0x55d398326f99059fF775485246999027B3197955",
        startblock: int = 0,
        endblock: int = 99999999,
        page: int = 1,
        offset: int = 1000,
        sort="desc",
    ):
        """
        [Get a list of 'Normal' Transactions By Address](https://docs.bscscan.com/api-endpoints/accounts#get-a-list-of-bep-20-token-transfer-events-by-address)
        
        Default address is quantfreedom wallet
        Default contract address is USDT
        """
        params = {
            "module": "account",
            "address": address,
            "contractaddress": contractaddress,
            "action": "tokentx",
            "startblock": startblock,
            "endblock": endblock,
            "page": page,
            "offset": offset,
            "sort": sort,
            "apikey": self.api_key,
        }
        response = get(url=self.url, params=params).json()
        try:
            data_list = response["result"]
            sorted_list = Exchange(use_test_net=False).sort_list_of_dicts(data_list)
            return sorted_list
        except Exception as e:
            raise Exception(
                f"Response -> {response['message']} - Exception for check_transaction_receipt_status -> {e} "
            )

    def get_transaction_by_hash(
        self,
        tx_hash: str,
        address: str = "0x7192b3AA5878293075951b53dEcefb09F3C6F37c",
        contractaddress: str = "0x55d398326f99059fF775485246999027B3197955",
        startblock: int = 0,
        endblock: int = 99999999,
        page: int = 1,
        offset: int = 1000,
        sort="desc",
    ):
        """
        Default address is quantfreedom wallet
        Default contract address is USDT
        """
        transactions = self.get_transactions(
            address=address,
            contractaddress=contractaddress,
            startblock=startblock,
            endblock=endblock,
            page=page,
            offset=offset,
            sort=sort,
        )
        for event in transactions:
            if event["hash"] == tx_hash:
                return event
        return "Couldn't find transaction"

    def get_transaction_value_by_hash(
        self,
        tx_hash: str,
        address: str = "0x7192b3AA5878293075951b53dEcefb09F3C6F37c",
        contractaddress: str = "0x55d398326f99059fF775485246999027B3197955",
        startblock: int = 0,
        endblock: int = 99999999,
        page: int = 1,
        offset: int = 1000,
        sort="desc",
    ):
        """
        Default address is quantfreedom wallet
        Default contract address is USDT
        """
        try:
            transaction = self.get_transaction_by_hash(
                tx_hash=tx_hash,
                address=address,
                contractaddress=contractaddress,
                startblock=startblock,
                endblock=endblock,
                page=page,
                offset=offset,
                sort=sort,
            )
            value = round(float(transaction["value"]) / 10 ** int(transaction["tokenDecimal"]), 2)
            return value
        except:
            return transaction

    def get_transaction_by_from_address(
        self,
        from_address: str,
        address: str = "0x7192b3AA5878293075951b53dEcefb09F3C6F37c",
        contractaddress: str = "0x55d398326f99059fF775485246999027B3197955",
        startblock: int = 0,
        endblock: int = 99999999,
        page: int = 1,
        offset: int = 1000,
        sort="desc",
    ):
        """
        Default address is quantfreedom wallet
        Default contract address is USDT
        """
        transactions = self.get_transactions(
            address=address,
            contractaddress=contractaddress,
            startblock=startblock,
            endblock=endblock,
            page=page,
            offset=offset,
            sort=sort,
        )
        for event in transactions:
            if event["from"] == from_address:
                return event
        return "Couldn't find transaction"

    def get_transaction_value_from_address(
        self,
        from_address: str,
        address: str = "0x7192b3AA5878293075951b53dEcefb09F3C6F37c",
        contractaddress: str = "0x55d398326f99059fF775485246999027B3197955",
        startblock: int = 0,
        endblock: int = 99999999,
        page: int = 1,
        offset: int = 1000,
        sort="desc",
    ):
        """
        Default address is quantfreedom wallet
        Default contract address is USDT
        """
        try:
            transaction = self.get_transaction_by_from_address(
                from_address=from_address,
                address=address,
                contractaddress=contractaddress,
                startblock=startblock,
                endblock=endblock,
                page=page,
                offset=offset,
                sort=sort,
            )
            value = round(float(transaction["value"]) / 10 ** int(transaction["tokenDecimal"]), 2)
            return value
        except:
            return transaction
