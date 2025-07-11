from collections import defaultdict
from enum import Enum
from typing import List
from ..ir import Insts, Variable, Op, IRInst


class EdgeType(Enum):
    tree = 0
    forward = 1
    back = 2
    cross = 3

class BasicBlockBranchType(Enum):
    jump = 0
    cond = 1
    switch = 2


class BasicBlock:
    def __init__(self, bb_id: int, start_idx: int, end_idx: int, insts: Insts):
        self.inst_idx_list: List[int] = [i for i in range(start_idx, end_idx)]
        self.insts: List[IRInst] = insts.ir_insts[start_idx: end_idx]
        self.phi_insts_idx_end = 0

        self.num_of_insts = (end_idx - start_idx)
        self.id = bb_id

        self.comment = ""

        self.tag = "B" + str(bb_id) + "[addr " + str(self.inst_idx_list[0]) + "]"

        self.branch_type: BasicBlockBranchType = BasicBlockBranchType.jump
        # 1. if the branch_type is jump,
        # then the ordered_suc_bbs only has one element, the next bb id.
        # 2. if the branch_type is cond,
        # then the first element of ordered_succ_bbs is true branch target,
        # the second element is false branch target.
        # 3. if the branch_type is switch,
        # then the ordered_succ_bbs has more than two elements.
        self.ordered_succ_bbs: list[int] = []

        self.pred_bbs = defaultdict(list)
        self.succ_bbs = defaultdict(list)

        self.dominator_tree_parent = None
        self.dominator_tree_children_id: List = [ ]


    def add_comment(self, comment: str):
        self.comment = comment

    def add_insts(self, start_index, end_index):
        self.inst_idx_list.extend([i for i in range(start_index, end_index)])
        self.num_of_insts += (end_index - start_index)

    def add_phi(self, phi_inst: IRInst):
        self.insts.insert(0, phi_inst)
        self.phi_insts_idx_end += 1

    def inst_exist(self, inst_index: int):
        return inst_index in self.inst_idx_list

def has_phi_for_var(block: BasicBlock, varname: str):
    # iterate all insts
    for inst in block.insts:
        if inst.op == Op.CALL and inst.operand1.value.varname == "φ":
            if inst.result.value.varname == varname:
                return True
    return False
