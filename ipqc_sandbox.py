"""
This file contains a hello world type environment for qiskit for the HY course introduction to programming of quantum computers.
"""
import qiskit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error
from qiskit.tools.visualization import plot_histogram
import matplotlib.pyplot as plt

def create_noise_model(p_reset, p_meas, p_gate1):
    """
    Description of parameters:
    p_reset: probability of a qubit resetting to 0
    p_meas: probability of bit flip in measurement
    p_gate: probability of error when applying gate operations
    """
    error_reset = pauli_error([('X', p_reset), ('I', 1 - p_reset)])
    error_meas = pauli_error([('X',p_meas), ('I', 1 - p_meas)])
    error_gate1 = pauli_error([('X',p_gate1), ('I', 1 - p_gate1)])
    error_gate2 = error_gate1.tensor(error_gate1)

    noise = NoiseModel()
    noise.add_all_qubit_quantum_error(error_reset, "reset")
    noise.add_all_qubit_quantum_error(error_meas, "measure")
    noise.add_all_qubit_quantum_error(error_gate1, ["u1", "u2", "u3"])
    noise.add_all_qubit_quantum_error(error_gate2, ["cx"])

    return noise

def main():
    # Definition of registers
    qr = qiskit.QuantumRegister(2)
    cr = qiskit.ClassicalRegister(2)

    # Quantum circuit goes here!
    qc = qiskit.QuantumCircuit(qr, cr)
    qc.h(0)
    qc.cnot(0, 1)

    # Measure the qubits
    qc.measure(qr, cr)

    # Draw circuit
    print(qc.draw())

    # Run circuit in simulator backend for 1000 shots
    backend = AerSimulator()
    job = backend.run(qc, shots = 1000)
    results = job.result()
    counts = results.get_counts()

    # Plot results
    plot_histogram(counts)
    plt.show()

if __name__ == "__main__":
    main()
