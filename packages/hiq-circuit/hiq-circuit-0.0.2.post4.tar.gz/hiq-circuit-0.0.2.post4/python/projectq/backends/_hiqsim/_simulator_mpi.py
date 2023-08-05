#   Copyright 2019 <Huawei Technologies Co., Ltd>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Contains the projectq interface to a C++-based simulator, which has to be
built first. If the c++ simulator is not exported to python, a (slow) python
implementation is used as an alternative.
"""

import math
import random

import numpy
from projectq.cengines import BasicEngine
from projectq.meta import get_control_count, LogicalQubitIDTag
from projectq.ops import (NOT,
                          H,
                          R,
                          Measure,
                          FlushGate,
                          Allocate,
                          Deallocate,
                          BasicMathGate,
                          TimeEvolution, FastForwardingGate, Command,
                          MetaSwap, AllocateQuregGate)
from projectq.types import WeakQubitRef

from ._cppsim_mpi import SimulatorMPI as SimulatorBackend

from mpi4py import rc
rc.thread = True
rc.thread_level = 'funneled'
rc.finalize = True
from mpi4py import MPI  # properly loads and initializes MPI environment


class SimulatorMPI(BasicEngine):
    """
    SimulatorMPI is a compiler engine which simulates a quantum computer using
    C++-based kernels.

    OpenMP is enabled and the number of threads can be controlled using the
    OMP_NUM_THREADS environment variable, i.e.

    .. code-block:: bash

        export OMP_NUM_THREADS=4 # use 4 threads
        export OMP_PROC_BIND=spread # bind threads to processors by spreading
    """
    def __init__(self, gate_fusion=False, rnd_seed=None, num_local_qubits=33, max_fused_qubits=4):
        """
        Construct the C++/Python-simulator object and initialize it with a
        random seed.

        Args:
            gate_fusion (bool): If True, gates are cached and only executed
                once a certain gate-size has been reached (only has an effect
                for the c++ simulator).
            rnd_seed (int): Random seed (uses random.randint(0, 4294967295) by
                default).
            num_local_qubits (int): maximum number of qubits the MPI node can
                allocate by itself
            max_fused_qubits (int): the maximum number of qubits the fused gate
                can act on

        Example of gate_fusion: Instead of applying a Hadamard gate to 5
        qubits, the simulator calculates the kronecker product of the 1-qubit
        gate matrices and then applies one 5-qubit gate. This increases
        operational intensity and keeps the simulator from having to iterate
        through the state vector multiple times. Depending on the system (and,
        especially, number of threads), this may or may not be beneficial.
        """
        if not MPI.Is_thread_main():
            raise RuntimeError("Incorrect MPI initialization: MPI must be initialized with Init_thread()!")

        if MPI.Query_thread() < MPI.THREAD_FUNNELED:
            raise RuntimeError("Incorrect MPI thread level: thread level must be >= THREAD_FUNNELED!")
    
        if rnd_seed is None:
            rnd_seed = random.randint(0, 4294967295)
        BasicEngine.__init__(self)
        self._simulator = SimulatorBackend(rnd_seed, num_local_qubits, max_fused_qubits)
        self._gate_fusion = gate_fusion

    def is_available(self, cmd):
        """
        Specialized implementation of is_available: The simulator can deal
        with all arbitrarily-controlled gates which provide a
        gate-matrix (via gate.matrix) and acts on 5 or less qubits (not
        counting the control qubits).

        Args:
            cmd (Command): Command for which to check availability (single-
                qubit gate, arbitrary controls)

        Returns:
            True if it can be simulated and False otherwise.
        """
        if (cmd.gate == Measure or cmd.gate == Allocate or
                cmd.gate == Deallocate or
                isinstance(cmd.gate, AllocateQuregGate)):
            return True
        elif (isinstance(cmd.gate, BasicMathGate) or  # current version don't support this
               isinstance(cmd.gate, TimeEvolution)):
            return False
            
        try:
            m = cmd.gate.matrix
            # Allow up to 5-qubit gates
            if len(m) > 2 ** 5:
                return False
            return True
        except:
            return False

    def _convert_logical_to_mapped_qureg(self, qureg):
        """
        Converts a qureg from logical to mapped qubits if there is a mapper.

        Args:
            qureg (list[Qubit],Qureg): Logical quantum bits
        """
        mapper = self.main_engine.mapper
        if mapper is not None:
            mapped_qureg = []
            for qubit in qureg:
                if qubit.id not in mapper.current_mapping:
                    raise RuntimeError("Unknown qubit id. "
                                       "Please make sure you have called "
                                       "eng.flush().")
                new_qubit = WeakQubitRef(qubit.engine,
                                         mapper.current_mapping[qubit.id])
                mapped_qureg.append(new_qubit)
            return mapped_qureg
        else:
            return qureg

    def _get_exp_value(self, pairs, terms2send, coeff2send, flag):
        return self._simulator.get_expectation_value(pairs, terms2send, coeff2send, flag)

    def _app_qubit_oper(self, pairs, terms2send, coeff2send, flag):
        return self._simulator.app_qubit_oper(pairs, terms2send, coeff2send, flag)

    def get_probability(self, bit_string, qureg):
        """
        Return the probability of the outcome `bit_string` when measuring
        the quantum register `qureg`.

        Args:
            bit_string (list[bool|int]|string[0|1]): Measurement outcome.
            qureg (Qureg|list[Qubit]): Quantum register.

        Returns:
            Probability of measuring the provided bit string.

        Note:
            Make sure all previous commands (especially allocations) have
            passed through the compilation chain (call main_engine.flush() to
            make sure).

        Note:
            If there is a mapper present in the compiler, this function
            automatically converts from logical qubits to mapped qubits for
            the qureg argument.
        """
        qureg = self._convert_logical_to_mapped_qureg(qureg)
        bit_string = [bool(int(b)) for b in bit_string]
        return self._simulator.get_probability(bit_string,
                                               [qb.id for qb in qureg])

    def get_amplitude(self, bit_string, qureg):
        """
        Return the probability amplitude of the supplied `bit_string`.
        The ordering is given by the quantum register `qureg`, which must
        contain all allocated qubits.

        Args:
            bit_string (list[bool|int]|string[0|1]): Computational basis state
            qureg (Qureg|list[Qubit]): Quantum register determining the
                ordering. Must contain all allocated qubits.

        Returns:
            Probability amplitude of the provided bit string.

        Note:
            Make sure all previous commands (especially allocations) have
            passed through the compilation chain (call main_engine.flush() to
            make sure).

        Note:
            If there is a mapper present in the compiler, this function
            automatically converts from logical qubits to mapped qubits for
            the qureg argument.
        """
        qureg = self._convert_logical_to_mapped_qureg(qureg)
        bit_string = [bool(int(b)) for b in bit_string]
        return self._simulator.get_amplitude(bit_string,
                                             [qb.id for qb in qureg])

    def set_state_vec_components(self, new_state_vec):
        """
        Set state vector components. This function does not change the ordering of qureg. It sequentially assigns
        the corresponding components of a new vector to the components of the state vector. Therefore, the length of
        the new vector must be equal to 2 to the power of the number of qubits.

        Args:
            new_state_vec (list[complex]): Array of complex amplitudes
                describing the wavefunction (must be normalized).
        """
        self._simulator.set_state_vec_components(new_state_vec)

    def collapse_wavefunction(self, qureg, values):
        """
        Collapse a quantum register onto a classical basis state.

        Args:
            qureg (Qureg|list[Qubit]): Qubits to collapse.
            values (list[bool|int]|string[0|1]): Measurement outcome for each
                                                 of the qubits in `qureg`.

        Raises:
            RuntimeError: If an outcome has probability (approximately) 0 or
                if unknown qubits are provided (see note).

        Note:
            Make sure all previous commands have passed through the
            compilation chain (call main_engine.flush() to make sure).

        Note:
            If there is a mapper present in the compiler, this function
            automatically converts from logical qubits to mapped qubits for
            the qureg argument.
        """
        qureg = self._convert_logical_to_mapped_qureg(qureg)
        return self._simulator.collapse_wavefunction([qb.id for qb in qureg],
                                                     [bool(int(v)) for v in
                                                      values])

    def cheat_local(self):
        """
        Access the ordering of the qubits and this MPI process's part of
        of state vector directly.

        Returns:
            A tuple where the first entry is a dictionary mapping qubit
            indices to bit-locations (all qubits) and the second entry is the local part
            of state vector.

        """
        return self._simulator.cheat_local()

    def cheat(self):
        """
        Access the ordering of the qubits and the state vector directly.

        This is a cheat function which enables, e.g., more efficient
        evaluation of expectation values and debugging.

        Returns:
            A tuple (id2pos, tot_vec) where the first entry is a dictionary mapping qubit
            indices to bit-locations and the second entry is the corresponding
            state vector.

        Note:
            The function performs MPI_Allgather() and returns concatenated
            full state vector. It is always concatenated from np parts, so
            it is presumed that there are log(np) global qubits. One should
            check qubit ordering returned to find out which bit positions are
            valid. For example: np = 4, id2pos = {0:0, 1:2} then state vector
            size is 8 and valid data at indices 0, 1, 4, 5.

        Note:
            Make sure all previous commands have passed through the
            compilation chain (call main_engine.flush() to make sure).

        Note:
            If there is a mapper present in the compiler, this function
            DOES NOT automatically convert from logical qubits to mapped
            qubits.
        """
        id2pos, vec = self.cheat_local()
        tot_vec = numpy.zeros(len(vec)*MPI.COMM_WORLD.Get_size(), dtype=complex)
        MPI.COMM_WORLD.Allgather([numpy.array(vec), MPI.COMPLEX], [tot_vec, MPI.COMPLEX])
        return id2pos, tot_vec

    def get_qubits_ids(self):
        """
        Returns:
             A list of all qubits ids allocated in simulator
        """
        return self._simulator.get_qubits_ids()

    def get_local_qubits_ids(self):
        """
        Returns:
             A list of local qubits ids
        """
        return self._simulator.get_local_qubits_ids()

    def get_global_qubits_ids(self):
        """
        Returns:
             A list of global qubits ids
        """
        return self._simulator.get_global_qubits_ids()

    def set_qubits_perm(self, ids):
        """
        Sets the initial permutation of qubits in simulator
        just after a first Qureg has been allocated

        Args:
            ids (list[int]): list of all qubits ids
        """
        self._simulator.set_qubits_perm(ids)

    def swap_qubits(self, qubits):
        self._simulator.swap_qubits(qubits)

    def _handle(self, cmd):
        """
        Handle all commands, i.e., call the member functions of the C++-
        simulator object corresponding to measurement, allocation/
        deallocation, and (controlled) single-qubit gate.

        Args:
            cmd (Command): Command to handle.

        Raises:
            Exception: If a non-single-qubit gate needs to be processed
                (which should never happen due to is_available).
        """
        if isinstance(cmd.gate, FlushGate):
            pass
        elif cmd.gate == MetaSwap:
            qubits = [qb.id for qr in cmd.all_qubits for qb in qr]
            self.swap_qubits(qubits)
        elif cmd.gate == Measure:
            assert(get_control_count(cmd) == 0)
            ids = [qb.id for qr in cmd.qubits for qb in qr]
            out = self._simulator.measure_qubits(ids)
            i = 0
            for qr in cmd.qubits:
                for qb in qr:
                    # Check if a mapper assigned a different logical id
                    logical_id_tag = None
                    for tag in cmd.tags:
                        if isinstance(tag, LogicalQubitIDTag):
                            logical_id_tag = tag
                    if logical_id_tag is not None:
                        qb = WeakQubitRef(qb.engine,
                                          logical_id_tag.logical_qubit_id)
                    self.main_engine.set_measurement_result(qb, out[i])
                    i += 1
        elif cmd.gate == Allocate:
            ID = cmd.qubits[0][0].id
            self._simulator.allocate_qubit(ID)
        elif isinstance(cmd.gate, AllocateQuregGate):
            ids = [qb.id for qr in cmd.qubits for qb in qr]
            self._simulator.allocate_qureg(ids, cmd.gate.init)
        elif cmd.gate == Deallocate:
            ID = cmd.qubits[0][0].id
            self._simulator.deallocate_qubit(ID)
        elif isinstance(cmd.gate, BasicMathGate):
            qubitids = []
            for qr in cmd.qubits:
                qubitids.append([])
                for qb in qr:
                    qubitids[-1].append(qb.id)
            math_fun = cmd.gate.get_math_function(cmd.qubits)
            self._simulator.emulate_math(math_fun, qubitids,
                                         [qb.id for qb in cmd.control_qubits])
        elif isinstance(cmd.gate, TimeEvolution):
            op = [(list(term), coeff) for (term, coeff)
                  in cmd.gate.hamiltonian.terms.items()]
            t = cmd.gate.time
            qubitids = [qb.id for qb in cmd.qubits[0]]
            ctrlids = [qb.id for qb in cmd.control_qubits]
            self._simulator.emulate_time_evolution(op, t, qubitids, ctrlids)
        elif len(cmd.gate.matrix) <= 2 ** 5:
            matrix = cmd.gate.matrix
            ids = [qb.id for qr in cmd.qubits for qb in qr]
            if not 2 ** len(ids) == len(cmd.gate.matrix):
                raise Exception("Simulator: Error applying {} gate: "
                                "{}-qubit gate applied to {} qubits.".format(
                                    str(cmd.gate),
                                    int(math.log(len(cmd.gate.matrix), 2)),
                                    len(ids)))
            self._simulator.apply_controlled_gate(matrix.tolist(),
                                                  ids,
                                                  [qb.id for qb in
                                                   cmd.control_qubits])
            if not self._gate_fusion:
                self._simulator.run()
        else:
            raise Exception("This simulator only supports controlled k-qubit"
                            " gates with k < 6!\nPlease add an auto-replacer"
                            " engine to your list of compiler engines.")

    def receive(self, command_list):
        """
        Receive a list of commands from the previous engine and handle them
        (simulate them classically) prior to sending them on to the next
        engine.

        Args:
            command_list (list<Command>): List of commands to execute on the
                simulator.
        """
        for cmd in command_list:
            if isinstance(cmd.gate, FlushGate) or isinstance(cmd.gate, FastForwardingGate):
                self._simulator.run()  # flush gate --> run all saved gates

            self._handle(cmd)

            if not self.is_last_engine:
                self.send([cmd])
