# -*- coding:utf-8 -*-
# CREATED BY: bohuai jiang 
# CREATED ON: 2020/8/14 4:30 PM
# LAST MODIFIED ON:
# AIM:
from typing import List

from automata.state_machine import StateMachine
from automata.sequence import StrSequence

from sentence_spliter.logic_graph import long_short_cuter, simple_cuter, special_cuter

# --  init default state machine -- #
__long_short_machine = StateMachine(long_short_cuter())
__simple_logic = StateMachine(simple_cuter())
__special_logic = StateMachine(special_cuter())


def cut_to_sentences(paragraph: str, verbose: bool = False):
    m_input = StrSequence(paragraph, verbose)
    __special_logic.run(m_input)
    return m_input.sentence_list()


def run_cut(str_block: str, logic_graph: dict) -> List[str]:
    machine = StateMachine(logic_graph)
    m_input = StrSequence(str_block)
    machine.run(m_input, verbose=False)
    return m_input.sentence_list()
