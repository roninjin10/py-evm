import logging

from evm.chains.base import (
    Chain
)

from .base_benchmark import (
    BaseBenchmark
)
from utils.chain_plumbing import (
    get_all_chains
)
from utils.format import (
    format_block
)
from utils.reporting import (
    DefaultStat
)


class MineEmptyBlocksBenchmark(BaseBenchmark):

    def __init__(self, num_blocks: int = 500) -> None:
        self.num_blocks = num_blocks

    @property
    def name(self) -> str:
        return 'Empty block mining'

    def execute(self) -> DefaultStat:
        total_stat = DefaultStat()

        for chain in get_all_chains():

            value = self.as_timed_result(lambda: self.mine_empty_blocks(chain, self.num_blocks))

            stat = DefaultStat(
                caption=chain.get_vm().fork,
                total_blocks=self.num_blocks,
                total_seconds=value.duration
            )
            total_stat = total_stat.cumulate(stat)
            self.print_stat_line(stat)

        return total_stat

    def mine_empty_blocks(self, chain: Chain, number_blocks: int) -> None:

        for _ in range(1, number_blocks + 1):
            block = chain.mine_block()
            logging.debug(format_block(block))
