
<p align="center">
  <picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/CATS_Logo_White.png" />
  <source media="(prefers-color-scheme: light)" srcset="assets/CATS_Logo_Black.png" />
  <img alt="CATS Logo">
</picture>
</p>

<h1 align="center">CATS: Conductor-driven Asymmetric Transport Scheme</h1>

<p align="center">
  <b><a href="https://ieeexplore.ieee.org/document/11413235">📄 IEEE Xplore Article</a></b> | 
  <b><a href="https://arxiv.org/abs/2603.13945">🔓 arXiv Version</a></b> | 
  <b><a href="https://github.com/smarizvi110/ns-3-dev-git">💻 View the ns-3 C++ Implementation</a></b>
</p>

This repository serves as the central hub for the **CATS** research project, introduced in our ICIC 2025 paper: *"A Case for CATS: A Conductor-driven Asymmetric Transport Scheme for Semantic Prioritization."*

Standard transport protocols like TCP operate as a blind, FIFO conveyor belt for data, a model that is increasingly suboptimal for latency-sensitive and interactive applications. This paper challenges this model by introducing CATS (Conductor-driven Asymmetric Transport Scheme), a framework that provides TCP with the semantic awareness necessary to prioritize critical content. By centralizing scheduling intelligence in a transport-native "Conductor", CATS significantly improves user-perceived performance by delivering essential data first. This architecture directly confronts a cascade of historical performance workarounds and their limitations, including the high overhead of parallel connections in HTTP/1.1, the transport-layer Head-of-Line blocking in HTTP/2, and the observed implementation heterogeneity of prioritization in HTTP/3 over QUIC. Built upon TCP BBR, our ns-3 implementation demonstrates this principle by reducing the First Contentful Paint by over 78% in a representative webpage download configured as a deliberate worst-case scenario, with no penalty to total page load time compared to the baseline.

---

## 📂 Project Structure and Source Code

This project is divided into this main hub repository and a separate ns-3 simulator fork.

### 1. The Official C++ Implementation (ns-3)
The core protocol modifications and the reproducible experiments used to generate the results in the paper were built directly into the ns-3 network simulator. 

👉 **[Click here to view the ns-3 fork and experiment scripts](https://github.com/smarizvi110/ns-3-dev-git)**

*Note: To reproduce the exact results from the paper, please download the **[v1.0-icic2025 Release](https://github.com/smarizvi110/ns-3-dev-git/releases/tag/v1.0-icic2025)** from the repository linked above.*

### 2. Python Proof-of-Concept (`/python-poc`)
This hub repository contains a simplified Python-based conceptual model built using UDP sockets. It presents the basic scheduling principles of CATS (application-defined priorities, prioritized queues, and debt-based fairness) without the complexity of a full kernel or ns-3 TCP stack. See the `python-poc/` directory for instructions on how to run it.

### 3. Research Archive (`/archive`)
Early brainstorming notes, original proposal documents, and the developmental history of the project are preserved here for reference and transparency.

---

## 📝 Citation

If you find this research or code useful, please consider citing our paper:

```bibtex
@INPROCEEDINGS{11413235,
  author={Rizvi, Syed Muhammad Aqdas},
  booktitle={2025 6th International Conference on Innovative Computing (ICIC)}, 
  title={A Case for CATS: A Conductor-driven Asymmetric Transport Scheme for Semantic Prioritization}, 
  year={2025},
  volume={},
  number={},
  pages={1-6},
  keywords={Transport protocols;Processor scheduling;Semantics;Computer architecture;Conductors;Belts;Data models;Quality of experience;Standards;Paints;TCP;BBR;Quality of Experience (QoE);Prioritization;Transport Layer Scheduling;Head-of-Line (HoL) Blocking},
  doi={10.1109/ICIC68258.2025.11413235}}

```

---

## 📜 License

* **Code:** The Python Proof-of-Concept code in this repository is licensed under the [MIT License](LICENSE). *(Note: The official C++ ns-3 implementation in the linked fork inherits the GPLv2 license of the ns-3 project).*
* **Paper:** The official PDF manuscript is published by and copyright © 2025 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses.

---

## 👨‍💻 Author

**Syed Muhammad Aqdas Rizvi**
* Independent Researcher / Alumnus, Lahore University of Management Sciences (LUMS)
* Email: 25100166@lums.edu.pk | s.muhammadaqdasrizvi@gmail.com
* ORCID: [0009-0004-1491-4839](https://orcid.org/0009-0004-1491-4839)
