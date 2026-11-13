# National University of Computer & Emerging Sciences (FAST-NUCES)
## Department of Computer Science — Chiniot-Faisalabad Campus
### CL3001 Machine Learning - Lab | Semester Project (Spring 2026)
**Instructor:** Esha Iftikhar

---

## DELIVERABLE 1: RESEARCH PAPER APPROVAL FORM

| Field | Details |
| :--- | :--- |
| **Course Code & Title** | CL3001: Machine Learning - Lab (Spring 2026) |
| **Student Name(s)** | Ghulam Abbas / Aqeel Ahmad |
| **Roll Number(s)** | [Student Roll Numbers] |
| **Submission Date** | November 2026 |
| **Project GitHub URL** | [https://github.com/aqeelahmad0105-dev/poker-ai-game](https://github.com/aqeelahmad0105-dev/poker-ai-game) |

---

### 1. Selected Research Paper Details
* **Paper Title:** *Comparison of the Effectiveness of AI Models in Poker Games*
* **Authors:** Mateusz Tustanowski and Adrian P. Wozniak
* **Institutional Affiliation:** Military University of Technology, Warsaw, Poland
* **Publication Venue:** *Communications of International Proceedings*, Vol. 2025 (20), Article ID 4534725
* **Conference Presentation:** 45th IBIMA International Conference, 25–26 June 2025, Cordoba, Spain
* **Publication Date:** June 2025 (Meets 2025/2026 mandatory requirement)
* **Official Paper Link:** [https://ibimapublishing.com/p-articles/45AI/2025/4534725/](https://ibimapublishing.com/p-articles/45AI/2025/4534725/)
* **Digital Object Identifier (DOI):** [https://doi.org/10.5171/2025.4534725](https://doi.org/10.5171/2025.4534725)

---

### 2. Dataset Information
* **Dataset Name:** No-Limit Texas Hold'em Multi-Stage Decision & Gameplay Dataset
* **Source / Repository:** Public No-Limit Texas Hold'em game history records (derived from open poker hand log archives)
* **Dataset Link:** Included in project repository: [`data/poker_gameplay_paper_data.csv`](https://github.com/aqeelahmad0105-dev/poker-ai-game/tree/main/data)
* **Dataset Size:** 120,000 game state instances across 14 numerical features and 3 target decision classes (`Fold = 0`, `Check/Call = 1`, `Bet/Raise = 2`).

---

### 3. Justification & Alignment with Course Objectives
1. **Application-Based & Real-World Domain:**
   Poker represents an iconic stochastic imperfect-information benchmark in artificial intelligence and game theory, modeling real-world decision-making under uncertainty, hidden state variables, and economic risk management.
2. **Core Course Topics Applied:**
   The paper directly utilizes topics taught in the Machine Learning curriculum:
   * **Supervised Learning & Ensembles:** Random Forest classifiers, decision tree depth tuning, bagging, feature split criteria, and multi-seed variance analysis.
   * **Neural Networks & Reinforcement Learning:** Multi-Layer Perceptrons, Deep Q-Networks (DQN), Adam optimizer, $\epsilon$-greedy exploration policies, experience replay buffers, and target networks.
   * **Model Evaluation & Diagnostics:** Accuracy, F1-scores, confusion matrices, economic return (chips won/lost), and head-to-head tournament simulation.
3. **Reproducibility with Available Resources:**
   The computational scope is fully reproducible using standard Python data science libraries (`scikit-learn`, `numpy`, `pandas`, `joblib`, `streamlit`) within standard hardware constraints without requiring multi-GPU server clusters.
4. **Feasibility of Meaningful Bonus Improvement:**
   The paper concludes with an open research recommendation: combining supervised Random Forest baselines with adaptive RL, which we have directly implemented into a full-fledged interactive multiplayer web application.

---

**Instructor Approval Status:** _______________________  
**Instructor Signature:** ____________________________  
**Date:** ___________________

