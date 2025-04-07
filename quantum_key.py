# quantum_key.py
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class QuantumKeyManager:
    def __init__(self):
        self.raw_key = None
        self.aes_key = None
        self.iv = None
        self.encrypted_data = None

    def generate_key(self, key_length=128, add_listener=False):
        key_str, mismatch_rate = generate_quantum_key_batch(
            key_length, add_listener=add_listener
        )
        self.raw_key = key_str
        self.aes_key = bytes(int(key_str, 2).to_bytes(16, byteorder='big'))
        return mismatch_rate

    def clear(self):
        self.raw_key = None
        self.aes_key = None
        self.iv = None
        self.encrypted_data = None

def generate_quantum_key_batch(key_length=128, batch_size=30, add_listener=False):
    key = []
    mismatch_count = 0

    while len(key) < key_length:
        remaining_bits = key_length - len(key)
        current_batch_size = min(batch_size, remaining_bits)

        simulator = AerSimulator()
        alice_circuit = QuantumCircuit(current_batch_size)
        bob_circuit = QuantumCircuit(current_batch_size)

        alice_bases = np.random.choice(['z', 'x'], size=current_batch_size)
        alice_bits = np.random.choice([0, 1], size=current_batch_size)
        for i in range(current_batch_size):
            if alice_bits[i] == 1:
                alice_circuit.x(i)
            if alice_bases[i] == 'x':
                alice_circuit.h(i)

        bob_bases = np.random.choice(['z', 'x'], size=current_batch_size)
        for i in range(current_batch_size):
            if bob_bases[i] == 'x':
                bob_circuit.h(i)

        combined_circuit = alice_circuit.compose(bob_circuit)
        combined_circuit.measure_all()
        compiled_circuit = transpile(combined_circuit, simulator)
        result = simulator.run(compiled_circuit).result()

        counts = result.get_counts()
        measured_bits = list(counts.keys())[0][::-1]

        matching_indices = [i for i in range(current_batch_size) if alice_bases[i] == bob_bases[i]]
        batch_key_bits = [measured_bits[i] for i in matching_indices]

        if add_listener:
            for i in range(len(matching_indices)):
                if np.random.rand() < 0.25:
                    batch_key_bits[i] = '1' if batch_key_bits[i] == '0' else '0'
                    mismatch_count += 1

        key.extend(batch_key_bits)

    mismatch_rate = mismatch_count / len(key) if key else 0
    return ''.join(key[:key_length]), "安全" if mismatch_rate < 0.1 else "不安全"
