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

#ifndef SWAPPERMT_HPP
#define SWAPPERMT_HPP

#include <glog/logging.h>

#include <atomic>
#include <boost/format.hpp>
#include <boost/mpi.hpp>
#include <complex>
#include <list>
#include <thread>
#include <vector>

#include "simulator-mpi/SimulatorMPI.hpp"
#include "simulator-mpi/SwapArrays.hpp"

class EXPORT_API SwapperMT
{
public:
     typedef std::complex<double> value_type;
     typedef SwapBuffers<value_type> swap_buffers_type;

     static const uint64_t MaxGlobal;

    const uint64_t M;
    const mpi::communicator& comm;

     uint64_t n;

     swap_buffers_type& buffs;

    uint64_t n_bits;
    const std::vector<uint64_t>& swap_bits;

    SwapperMT(uint64_t aM, const mpi::communicator& aComm, swap_buffers_type& aBuffs, uint64_t nBits, const std::vector<uint64_t>& aSwap_bits )
              : M(aM), comm(aComm), n( calcSendCount(comm.size(), M, aBuffs.size()) )
              , buffs(aBuffs), n_bits(nBits), swap_bits(aSwap_bits)
    {
        DLOG(INFO) << boost::format("SwapperMT(): n: %d, comm_size: %d") % n % comm.size();

    }

     ~SwapperMT()
     {}

     static uint64_t calcSendCount(size_t comm_size, uint64_t M,
                                   uint64_t maxSendBytes)
     {
          size_t state_vector_size = (1ul << M);

          uint64_t n0 = ((maxSendBytes / sizeof(value_type)) / comm_size);
          n0 = n0 < 1 ? 1 : n0;
          uint64_t n = (state_vector_size / comm_size) < n0
                           ? (state_vector_size / comm_size)
                           : n0;

          return n;
     }

    void runProducer(SimulatorMPI::StateVector::iterator aVector);
    void runConsumer2(SimulatorMPI::StateVector::iterator aVector);

     void join()
     {
          if (this->producer.joinable())
               this->producer.join();

          if (this->consumer2.joinable())
               this->consumer2.join();
     }

    void doSwap(SimulatorMPI::StateVector& state_vector);

private:
     std::thread producer;
     std::thread consumer2;
};

#endif  // SWAPPERMT_HPP
