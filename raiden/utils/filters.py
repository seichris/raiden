# -*- coding: utf-8 -*-
from typing import Dict

from eth_utils import decode_hex
from web3.utils.filters import construct_event_filter_params
from raiden_contracts.contract_manager import ContractManager
from raiden_contracts.constants import CONTRACT_TOKEN_NETWORK, EVENT_CHANNEL_OPENED

from raiden.utils.typing import Address, ChannelID, BlockSpecification


def get_filter_args_for_channel_from_token_network(
        token_network_address: Address,
        channel_identifier: ChannelID,
        from_block: BlockSpecification = 0,
        to_block: BlockSpecification = 'latest',
) -> Dict:
    event_abi = ContractManager.get_contract_abi(CONTRACT_TOKEN_NETWORK, EVENT_CHANNEL_OPENED)

    # Here the topics for a specific event are created
    # The first entry of the topics list is the event name, then the first parameter is encoded,
    # in the case of a token network, the first parameter is always the channel identifier
    data_filter_set, event_filter_params = construct_event_filter_params(
        event_abi=event_abi,
        contract_address=token_network_address,
        argument_filters={
            'channel_identifier': decode_hex(channel_identifier),
        },
        fromBlock=from_block,
        toBlock=to_block,
    )

    # As we want to get all events for a certain channel we remove the event specific code here
    # and filter just for the channel identifier
    event_filter_params['topics'][0] = None

    return event_filter_params