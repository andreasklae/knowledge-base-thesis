![ex3_resources_rgb200.png](https://images.squarespace-cdn.com/content/v1/5a8c400e0abd04c2d35c2f7c/1570440723712-R1X48QYGFIZAAIGRMZKV/ex3_resources_rgb200.png?format=2500w)

## Facilitating research on bleeding-edge HPC technologies

The eX3 infrastructure is continuously under build-up and reconfiguration in order to keep up-to-date with the technology development. The following hardware resources, acquired in the first phase procurement, are currently available. For further details, please consult the [eX3 wiki](http://wiki.ex3.simula.no/).

---

## AMD EPYC

There are four dual processor nodes (Supermicro 2023US-TR4) in the eX3 cluster equipped with the [AMD EPYC 7601](https://en.wikichip.org/wiki/amd/epyc/7601) processor (Naples family, 64-bit, 32-core, x86). Thus, in total eight processors with 256 cores. Each AMD node has 2 TB DDR4 main memory and 2.8 TB local NVMe scratch storage.

There are 12 single-processor nodes (Gigabyte R272-Z30) with the [AMD EPYC 7302P](https://en.wikichip.org/wiki/amd/epyc/7302p) processor (Rome family, 64-bit, 16-core, x86). So, in total 12 processors with 192 cores, primarily intended for networking research. Each of these AMD nodes has 128 GB DDR4 main memory and 256 GB local NVMe scratch storage.

Recently, four additional dual processor nodes (Supermicro 2024US-TRT) with the [AMD EPYC 7302](https://en.wikichip.org/wiki/amd/epyc/7302) processor (Rome family, 64-bit, 16-core, x86) has been added. That is, in total eight processors with 128 cores, primarily as hosts for FPGA accelerators. Each of these AMD nodes has 512 GB DDR4 main memory and 7.6 TB GB local NVMe scratch storage.

Moreover, we have added four dual processor nodes (Supermicro 2024US-TRT) with the [AMD EPYC 7763](https://en.wikichip.org/wiki/amd/epyc/7763) processor (Milan family, 64-bit, 64-core, x86). That is, in total eight processors with 512 cores. Two of the nodes have dual AMD MI100 GPUs and two have dual NVIDIA A100 GPUs (see below). The nodes with AMD accelerators are considered as “lightweight replica” of the nodes to appear in the [LUMI supercomputer](https://www.lumi-supercomputer.eu/). Each of these AMD nodes has 2 TB DDR4 main memory and 7.6 TB GB local NVMe scratch storage. There are also two AMD EPYC 7763 processors in a dedicated 8-way NVIDIA A100 system, see below.

We have added one dual processor node with the [AMD EPYC 9684X](https://www.amd.com/en/products/processors/server/epyc/4th-generation-9004-and-8004-series/amd-epyc-9684x.html) processor (Genoa family, 64-bit, 96-core, x86), giving a total of 192 cores.

---

## ARM CAVIUM

There are four dual processor nodes (Gigabyte R281-T94) in the eX3 cluster equipped with the [ARM Cavium ThunderX2 CN9980](https://en.wikichip.org/wiki/cavium/thunderx2/cn9980) processor (64-bit, 32-core, ARM). Thus, in total eight processors with 256 cores. Each ARM node has 1 TB DDR4 main memory and 5.3 TB local SSD scratch storage.

---

## HiSiliconkunpeng

In a are four dual processor nodes (Huawei TaiShan 200) in the eX3 cluster with the [HiSilicon KunPeng 920](https://en.wikichip.org/wiki/hisilicon/kunpeng/920-6426) processor (64-bit, 64-core, ARM). This makes a total of eight processors with 512 cores. Each Huawei node has 1 TB DDR4 main memory and 4.2 TB local SSD scratch storage.

---

## INTEL XEON

Embedded in the NVIDIA DGX-2 node (see below), eX3 offers access to two [Intel Xeon Platinum 8168](https://en.wikichip.org/wiki/intel/xeon_platinum/8168) CPUs (64-bit, 24-core, x86).

There are four dual processor nodes in the eX3 cluster equipped with the [Intel Xeon Gold 6130](https://en.wikichip.org/wiki/intel/xeon_gold/6130) processor (64-bit, 16-core, x86). Thus, in total eight processors with 128 cores. Each of these nodes has 384 GB DDR4 main memory and 2TB local scratch storage. These nodes doubles as login/management nodes. Two of the nodes are also equipped with additional 384 GB NVDIMM memory.

In addition, eX3 has eight single processor nodes equipped with [Intel Xeon Silver 4112](https://en.wikichip.org/wiki/intel/xeon_silver/4112) processors (64-bit, 4-core, x86), thus in total 32 cores.

There are also two [Intel Xeon Platinum 8360Y](https://www.intel.com/content/www/us/en/products/sku/212459/intel-xeon-platinum-8360y-processor-54m-cache-2-40-ghz/specifications.html) processors (Ice Lake, 64-bit, 36-core, x86) in a dedicated 8-way NVIDIA A100 system, see below.

We have added a dual processor node with [Intel Xeon CPU Max 9480](https://www.intel.com/content/www/us/en/products/sku/232592/intel-xeon-cpu-max-9480-processor-112-5m-cache-1-90-ghz/specifications.html), equipped with two [Intel Data Center GPU Max 1100](https://www.intel.com/content/www/us/en/products/sku/232876/intel-data-center-gpu-max-1100/specifications.html).

---

## AMD GPU

Two of the recently installed AMD Milan CPU nodes are accelerated by two [AMD Radeon Instinct MI100](https://www.amd.com/en/products/server-accelerators/instinct-mi100) GPUs each, see above. These GPUs have 232 GB local memory each. We also have instances of the [AMD Instinct MI250](https://www.amd.com/en/products/accelerators/instinct/mi200/mi250.html) GPU.

---

## NVIDIA V100 GPU

The eX3 infrastructure includes a [DGX-2](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/dgx-2/dgx-2-print-datasheet-738070-nvidia-a4-web-uk.pdf) system consisting of 16 NVIDIA [Tesla V100](https://www.nvidia.com/en-us/data-center/tesla-v100/) GPUs, allowing simultaneous communication between all eight GPU pairs at 300 GBps through the 12 integrated [NVSwitches](http://images.nvidia.com/content/pdf/nvswitch-technical-overview.pdf). This gives a theoretical system-wide system bi-directional bandwidth of 2.4 TBps. All GPUs have 32 GB of local memory (total of 512 GB) and share a 1.5 TB main memory. The total system has 81,920 CUDA cores, and 10,240 Tensor cores delivering 2 Petaflops of tensor performance. The peak performance in double precision is 125 Teraflops.

---

## NVIDIAA100 GPU

Recently, the eX3 infrastructure has added a dedicated 8-way GPU system (Supermicro 4124GO-NART) with NVIDIA A100 GPUs connect by NVLINK. The system hosts two AMD Milan CPUs, see above. All of these A100 GPUs have 80 GB of local memory each (total of 640 GB) and share a 2 TB main memory and 30 TB of local NVMe storage. The total system has 55,296 CUDA cores, and 3,456 Tensor cores.

In addition, there two AMD Milan CPU nodes available, each accelerated with two A100 GPUs, see above. These GPUs have 40 GB local memory each.

---

## NVIDIA H200 GPU

Recently, the eX3 infrastructure has added two [NVIDIA H200 NVL GPUs](https://nvdam.widen.net/s/fdvdqvfvj2/hopper-h200-nvl-product-brief) to one of the nodes.

---

The eX3 infrastructure has added a two nodes 8-way GPU system (Supermicro ARS-111GL-NHR) equipped with the [GH200](https://www.nvidia.com/en-us/data-center/grace-hopper-superchip/) “Grace-Hopper” superchip, using UVM memory.

## NVIDIAGH200

---

## XILINXFPGA

Each of the two recently installed AMD Rome CPU nodes are accelerated by one [Xilinx U280](https://www.xilinx.com/products/boards-and-kits/alveo/u280.html) and one [Xilinx U250](https://www.xilinx.com/products/boards-and-kits/alveo/u250.html) FPGAs.

---

The eX3 infrastructure includes an [IPU-POD](https://www.graphcore.ai/posts/introducing-second-generation-ipu-systems-for-ai-at-scale), consisting of 64 Colossus Mk2 GC200 IPUs with 1472 cores each, making up a total of more than 94,000 cores. The total In-Processor Memory™ is more than 57 GB supported by a memory bandwidth of 47.5 TB/s per IPU. This IPU-POD is capable of 16 petaflops mixed precision peak performance. The IPU processor has been designed bottom-up for machine learning and AI workloads.

## GRAPHCOREIPU-POD64

---

## INTEL HABANA GAUDI HL-205

The eX3 infrastrucutre includes an 8-way system designed for AI/ML workloads (Supermicro SYS-420GH-TNGR), based on the [Intel Habana Gaudi HL-205](https://www.google.com/url?cd=&esrc=s&q=&rct=j&sa=t&source=web&url=https%3A%2F%2Fhabana.ai%2Fwp-content%2Fuploads%2F2019%2F06%2FGaudi-Datasheet.pdf&usg=AOvVaw1eEvKX36WRZmX_WtHIj_oh&ved=2ahUKEwiwwdG2x-v2AhUDv4sKHUgjDt8QFnoECA4QAQ) accelerator. The system, which also hosts two Intel Ice Lake CPUs (see above), has 2TB of local memory and 30 TB of local scratch storage. Each Gaudi accelerator has 32 GB of onboard local memory.

---

## AKIDA NEURAL PROCESSOR

The KunPeng CPU nodes (see above) hosts four Akida Neural Processors from BrainChip. These processors are designed specifically for neuromorphic computing.

---

## Interconnects

All eX3 nodes are connected through a 200 Gbps Infiniband HDR network using Mellanox components ([Quantum switches](https://www.mellanox.com/page/products_dyn?mtag=qm8700&product_family=263&ssn=m9gk5g6cvis74v4bunv6h8odj0) and [ConnectX-6 VPI HCAs](https://www.mellanox.com/page/products_dyn?mtag=connectx_6_vpi_card&product_family=265)). There is a also a smaller cell with 400 Gbps Infiniband NDR connectivity ([Quantum-2 switches](https://www.nvidia.com/content/dam/en-zz/Solutions/networking/infiniband-adapters/infiniband-connectx7-data-sheet.pdf) and [ConnectX-7 NDR endpoints](https://resources.nvidia.com/en-us-accelerated-networking-resource-library/connectx-7-datasheet)). In addition, some nodes are equipped with 32 GT/s Gen3 PCI Express networking provided by Dolphin Interconnect Solutions ([MXS824 switches](https://www.dolphinics.com/products/MXS824.html) and [Non-Transparent Bridging HCAs](https://www.dolphinics.com/products/MXH830.html)). There are also some nodes with Dolphin’s more recent 64 GT/s per port Gen4 PCIe products ([MXS924 switches](https://www.dolphinics.com/products/MXS924.html) and [MXH940 endpoints](https://mxh940%20endpoints/)). In addition, all nodes are connected to a 10/25/100 Gbps Ethernet network dependent on interfaces and managed through a 1 Gbps management network.

---

## Data storage

All nodes in the eX3 infrastructure have access to a [NetApp E5760 Enterprise hybrid storage unit](https://www.netapp.com/us/products/storage-systems/hybrid-flash-array/e5700.aspx) through the [BeeGFS parallel file system](https://www.beegfs.io/content/). The total storage capacity is 1 PB, based on a combination of spinning disks and SDDs. Please notice that eX3 does not offer long-term storage. This resource is only meant for the temporary storage of input data and computed results for the execution of experiments.