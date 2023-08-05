//   Copyright 2019 <Huawei Technologies Co., Ltd>
//
//   Licensed under the Apache License, Version 2.0 (the "License");
//   you may not use this file except in compliance with the License.
//   You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
//   Unless required by applicable law or agreed to in writing, software
//   distributed under the License is distributed on an "AS IS" BASIS,
//   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//   See the License for the specific language governing permissions and
//   limitations under the License.

#include "SwapperMT.hpp"

#include <glog/logging.h>
#include <mpi.h>

#include <boost/format.hpp>
#include <chrono>
#include <iostream>
#include <thread>

#include "mpi_ext.hpp"
#include "swapping.hpp"

const uint64_t SwapperMT::MaxGlobal = 17;

template<class InputIterator>
void f_producer(SwapperMT& s, InputIterator aVector, const std::vector<uint64_t>& swap_bits) {
    size_t start_free_idx = 0;
    while(start_free_idx < (1ul << (s.M - s.n_bits)) ) {
        auto arrs = s.buffs.old_arrays.pull_front();

        start_free_idx =
            swapping::Swapping<SwapperMT::MaxGlobal>::calcSwap<SwapperMT::swap_buffers_type::swap_arrays_type::value_type, InputIterator, swapping::BufferExchange<InputIterator, SwapperMT::swap_buffers_type::swap_arrays_type::value_type*>::state_to_buffer>( s.n_bits, aVector, s.n, start_free_idx
                                                              , arrs->svalues.data(), swap_bits);

          s.buffs.fresh_arrays.push_back(arrs);
     }

     s.buffs.fresh_arrays.push_back(nullptr);

     DLOG(INFO) << "f_producer(): exit";
}

template<class InputIterator>
void f_consumer2(SwapperMT& s, InputIterator aVector, const std::vector<uint64_t>& swap_bits) {
    size_t start_free_idx = 0;
    while(start_free_idx < (1ul << (s.M - s.n_bits)) ) {
        auto arrs = s.buffs.fresh_arrays2.pull_front();

        start_free_idx =
                swapping::Swapping<SwapperMT::MaxGlobal>::calcSwap<SwapperMT::swap_buffers_type::swap_arrays_type::value_type, InputIterator, swapping::BufferExchange<InputIterator, SwapperMT::swap_buffers_type::swap_arrays_type::value_type*>::buffer_to_state>( s.n_bits, aVector, s.n, start_free_idx
                        , arrs->rvalues.data(), swap_bits);
        s.buffs.old_arrays.push_back(arrs);
    }

     DLOG(INFO) << "f_consumer2(): exit";
}

void SwapperMT::runProducer(SimulatorMPI::StateVector::iterator aVector) {
    this->producer = std::thread(f_producer<typename SimulatorMPI::StateVector::iterator>, std::ref(*this), aVector, std::ref(swap_bits));
}

void SwapperMT::runConsumer2(SimulatorMPI::StateVector::iterator aVector) {
    this->consumer2 = std::thread(f_consumer2<typename SimulatorMPI::StateVector::iterator>, std::ref(*this), aVector, std::ref(swap_bits));
}

void SwapperMT::doSwap(SimulatorMPI::StateVector& state_vector) {
    this->runConsumer2(state_vector.begin());
    this->runProducer(state_vector.begin());

     do {
          swap_buffers_type::swap_arrays_type* arrs;
          buffs.fresh_arrays.pull_front(arrs);
          if (arrs == nullptr)
               break;

          mpi::all_to_all(comm, arrs->svalues.data(), n, arrs->rvalues.data());

          buffs.fresh_arrays2.push_back(arrs);

     } while (true);

    this->join();
}
