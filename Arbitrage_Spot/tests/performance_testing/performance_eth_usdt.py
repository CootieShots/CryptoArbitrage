import sys
sys.path.append('../')
sys.path.append('../../')
import os
import time
import asyncio

from dquant.constants import Constants
from dquant.markets._binance_spot_rest import Binance
from dquant.markets._huobi_spot_ws import HuobiWs
from dquant.markets._bitfinex_spot_ws import BitfinexSpotWs
from dquant.markets._okex_spot_ws_v2 import OkexSpotWs
from tests.performance_testing.performance_common import Performance


class EthUsdtWithoutLoop(Performance):

    def __init__(self, Market):
        os.environ[Constants.DQUANT_ENV] = "dev"

        self.mkt = Market('eth_usdt')
        self.mkt.setDaemon(True)
        self.mkt.start()
        time.sleep(10)
        super().__init__(self.mkt)

    def buy(self):
        res_b = self.mkt.buy(0.02, price=1)
        return res_b


class EthUsdtWithLoop(Performance):

    def __init__(self, Market):
        os.environ[Constants.DQUANT_ENV] = "dev"
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.mkt = Market('eth_usdt', loop)
        self.mkt.setDaemon(True)
        self.mkt.start()
        time.sleep(10)
        super().__init__(self.mkt)

    def buy(self):
        res_b = self.mkt.buy(0.02, price=1)
        return res_b


class OkexEthUsdtWithLoop(Performance):

    def __init__(self, Market):
        os.environ[Constants.DQUANT_ENV] = "dev"
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.mkt = Market('eth_usdt', loop)
        self.mkt.setDaemon(True)
        self.mkt.start()
        time.sleep(10)
        super().__init__(self.mkt)

    def buy(self):
        res_b = self.mkt.buy(1, amount=0.02)
        return res_b


def test_bi():
    bi = EthUsdtWithoutLoop(Binance)
    bi.run()


def test_huobi_bfx_okex():

    hb_ws = EthUsdtWithLoop(HuobiWs)
    hb_ws.setDaemon(True)

    bfx = EthUsdtWithLoop(BitfinexSpotWs)
    bfx.setDaemon(True)

    okex = OkexEthUsdtWithLoop(OkexSpotWs)
    okex.setDaemon(True)

    hb_ws.start()
    bfx.start()
    okex.start()

    hb_ws.join()
    bfx.join()
    okex.join()


if __name__ == '__main__':
    os.environ[Constants.DQUANT_ENV] = "dev"
    test_huobi_bfx_okex()