import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister,qiskit
from qiskit import Aer, IBMQ, transpile, execute, assemble
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector
from qiskit.quantum_info.operators import Operator
from qiskit.providers.ibmq import least_busy
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from qiskit.algorithms import AmplificationProblem
from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit.algorithms import Grover

def oracle1() -> QuantumCircuit:
    """
    1 solution of 8 items.
    Returns:
        Oracle circuit.
    """
    data_reg = QuantumRegister(3)
    ancilla = QuantumRegister(1)
    circuit = QuantumCircuit(data_reg, ancilla, name='Oracle1')
    
    circuit.x(data_reg[1])
    circuit.mcx(data_reg, ancilla)
    circuit.x(data_reg[1])

    return circuit


def oracle2() -> QuantumCircuit:
    """
    2 solutions of 8 items.
    Returns:
        Oracle circuit.
    """
    data_reg = QuantumRegister(3)
    ancilla = QuantumRegister(1)
    circuit = QuantumCircuit(data_reg, ancilla, name='Oracle2')
    
    circuit.x(data_reg[1])
    circuit.mcx(data_reg, ancilla)
    circuit.x(data_reg[1])
    circuit.x(data_reg[0])
    circuit.mcx(data_reg, ancilla)
    circuit.x(data_reg[0])
    
    return circuit
    
def grover(n):
    var = QuantumRegister(n, 'var')
    out = QuantumRegister(1, 'out')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(var, out, cr)

    qc.x(n)                            
    qc.h(n)
    qc.h(var) 
    qc.append(oracle1(), range(n+1))    
    qc.h(range(n))  
    qc.x(range(n))  
    qc.h(n-1)     
    qc.mct(list(range(n-1)), n-1) 
    qc.h(n-1)
    for qubit in range(n):    
        qc.x(qubit)
    qc.h(range(n))  #H
    qc.measure(var, cr)
    return qc


def grover2(n):
    var = QuantumRegister(n, 'var')
    out = QuantumRegister(1, 'out')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(var, out, cr)

    qc.x(n)                              #initialize the qubit
    qc.h(n)
    qc.h(var)                            #hadamard gate to every qubit
    qc.append(oracle2(), range(n+1))     #oracle to every qubit.
    qc.h(range(n))  #hadamard transform
    qc.x(range(n))  #X transform
    qc.h(n-1)     #CZ gates & CT
    qc.mct(list(range(n-1)), n-1) 
    qc.h(n-1)
    for qubit in range(n):     #X transform
        qc.x(qubit)
    qc.h(range(n))  #H

    qc.measure(var, cr)
    return qc

def execute(qc):
    backend = Aer.get_backend('aer_simulator')
    job = qiskit.execute(qc, backend)
    result = job.result()
    return result

def main():

        o1 = oracle1()
        o2 = oracle2()
        
        #aer_simulator = Aer.get_backend('aer_simulator')
        #print('measurement:', result.top_measurement)

        #print oracle
        """
        print("Oracle1:")
        print(o1.draw())
        print("Oracle2:")
        print(o2.draw())
        print()
        """

        #print circuit
        print("(a)")
        qc = grover(3)
        print(qc.draw())
        result = execute(qc)
        print(result.get_counts())
        print()

        print("(b)")
        qc2 = grover2(3)
        print(qc2.draw())
        result2 = execute(qc2)
        print(result2.get_counts())

if __name__ == "__main__":
    main()