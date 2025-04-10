# 🧊 Microtubule (MT) Signal Subtraction in cryoSPARC Pipeline

This guide describes the workflow for performing MT signal subtraction under the **cryoSPARC** processing pipeline. Command-line experience is recommended for following this workflow.

**Kai Zhang Lab, Yale**  
**Last updated: April 2025**

---

## 📦 Requirements

- **pyem**: [https://github.com/asarnow/pyem](https://github.com/asarnow/pyem)
- **Scripts (this repo):**
  - [`multi-curve-fitting`](https://github.com/PengxinChai/multi-curve-fitting)
  - [`tubulin-lattice-subtraction`](https://github.com/PengxinChai/tubulin-lattice-subtraction)

Clone the necessary repositories:

```bash
git clone https://github.com/PengxinChai/multi-curve-fitting 
git clone https://github.com/PengxinChai/tubulin-lattice-subtraction
