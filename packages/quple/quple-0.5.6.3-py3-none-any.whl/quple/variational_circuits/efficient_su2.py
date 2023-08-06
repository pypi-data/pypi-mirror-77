from typing import List, Union, Optional, Callable, Sequence, Tuple

from quple import ParameterisedCircuit

class EfficientSU2(ParameterisedCircuit):
    '''The efficient SU2 circuit
    
    The efficient SU2 
    '''    
    def __init__(self, n_qubit: int, copies: int=2, 
                 su2_gates:Optional[Union[str, 'cirq.Gate', Callable, 'TemplateCircuitBlock',
                                               List[str],List['cirq.Gate'],List[Callable],
                                               List['TemplateCircuitBlock']]]=None,
                 entangle_strategy:Optional[Union[str,List[str], Callable[[int,int],List[Tuple[int]]],
                                                 List[Callable[[int,int],List[Tuple[int]]]]]]=None,
                 parameter_symbol:str='θ', name:str='EfficientSU2', *args, **kwargs):
        
        su2_gates = su2_gates or ['RY','RZ']
        super().__init__(n_qubit=n_qubit, copies=copies,
                         rotation_blocks=su2_gates,
                         entanglement_blocks='CX',
                         entangle_strategy=entangle_strategy,
                         parameter_symbol=parameter_symbol,
                         name=name,
                         flatten_circuit=False,
                         final_rotation_layer=True,
                         *args, **kwargs)