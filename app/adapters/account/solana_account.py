from app.adapters.account.base_account import AccountAdapterBase
from app.config.constants import LAMPORT_TO_SOL_RATE
from app.external.binance_api import BinanceApiInterface
from app.external.solana_network import SolanaNetworkInterface


class SolanaAccountDataAdapter(AccountAdapterBase):

    def __init__(self, tracked_account):
        self.account_pubkey = tracked_account.key
        self.display_name = tracked_account.display_name
        self.is_staked = tracked_account.is_staked
        self.binance_api = BinanceApiInterface.instance()
        self.solana_network_interface = SolanaNetworkInterface.instance()
        self.lamport_value = self._get_lamport_value()

    @property
    def crypto_currency_value(self):
        return self.lamport_value * LAMPORT_TO_SOL_RATE

    @property
    def usd_value(self):
        usd_sol_rate = self.binance_api.get_sol_usd_rate()
        return self.crypto_currency_value * usd_sol_rate

    @property
    def is_staked_str(self):
        return str(self.is_staked)

    def _get_lamport_value(self):
        return self.solana_network_interface.get_account_balance(self.account_pubkey)
