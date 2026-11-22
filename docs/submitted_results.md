# Step 3 results

$$
\boxed{S=\frac{z_D+z_F}{2}+z_C,\qquad T=2,\quad L=4,\quad \Delta t=0.5}
$$

$$
\begin{aligned}
D&=\max_m\sqrt{T}\left[I_{\mathrm{base}}(\bar n)-\frac1L\sum_{r=0}^{L-1}I_{m+r}\right],\\
F&=\max_m T\left|\frac1L\sum_{r=0}^{L-1}I_{m+r}e^{-i\Omega r\Delta t}\right|^2,\\
z_X&=\frac{X-\operatorname{median}_{\mathrm{train}}(X\mid\bar n)}{\operatorname{IQR}_{\mathrm{train}}(X\mid\bar n)/1.349},\quad X\in\{D,F\},\\
z_C&=\frac{-\bar n-\operatorname{mean}_{\mathrm{train}}(-\bar n)}{\operatorname{std}_{\mathrm{train}}(-\bar n)},\\
\Omega^2&=\kappa_2\kappa_b\bar n-\frac{(\kappa_b-\kappa_1-\kappa_\phi)^2}{16}.
\end{aligned}
$$

| Detector / dataset | ROC AUC | Suppression at 70% yield | Flips caught | DET point: FPR / FNR |
|---|---:|---:|---:|---:|
| Cat size alone / validation | 0.667 | 31.7% | 52.2% | 28.12% / 47.78% |
| DC + cat, T=2 / validation | 0.759 | 50.8% | 65.5% | 26.99% / 34.47% |
| **Final score / held-out training (4,500 rows)** | **0.790** | **61.8%** | **73.3%** | **28.39% / 26.71%** |
| **Final score / validation (7,500 rows)** | **0.753** | **51.2%** | **65.9%** | **26.96% / 34.13%** |
| T=4 + lower-30% amplitude gate / validation | 0.736 | 44.4% | 61.1% | 27.36% / 38.91% |
| Final submission / Aqora hidden test (reported) | — | 47% | — | — |

D measures the strongest downward excursion of the gliding-window mean, while F measures the strongest Fourier power at the predicted Ω over identical windows advancing one sample at a time.
The baseline is the median training-trajectory mean for each cat size; all centers and scales use 10,500 training rows, and κb=4 is a tutorial reference value, not a hidden-device fit.
We flag the largest 30% of scores and retain 70%; suppression is the relative reduction in flip fraction among retained records, so 51.2% suppression means approximately halving that fraction, rather than catching 51.2% of flips.
Evidence **(1)**: on validation, the final score improves suppression over cat size alone by **19.5 percentage points**, with ROC AUC increasing from **0.667 to 0.753**.
Evidence **(2)**: held-out training gives **61.8% suppression**, and validation AUC within individual cat sizes ranges from **0.581 to 0.723**, showing that the measured trajectories carry information beyond cat size.
Evidence **(3)**: doubling the window and gating weak Fourier amplitudes gives **44.4% suppression**, which is **6.8 percentage points below** the retained detector.
Adding F to DC + cat improves validation suppression by only **0.5 percentage points** and lowers AUC, so these measurements do not establish a reliable incremental benefit from F.
The table summarizes the ROC curves by AUC and the DET operating point by false-positive/false-negative rates at 70% yield; validation was inspected during development and is not a pristine test.
The reported Aqora hidden-test result is **47% suppression, worth 6.8/10 points**.
