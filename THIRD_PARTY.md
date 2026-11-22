# Sources and attribution

My contribution is the small-displacement response derivation, the Step-3
Fourier/DC witness, and the accompanying physical interpretation and evaluation.
This repository turns that work into scripts; it does not claim authorship of
Alice & Bob's challenge simulator or datasets.

The six modules in `src/catchtheflip/` (`models`, `simulate`, `rates`, `protocol`,
`records`, `scoring`) are unmodified copies of the Alice & Bob challenge helpers,
from <https://aqora.io/Alice_Bob/catch-the-flip>, commit
`63f4db7c09e793f03f65a2610102d2ef5dbca1f532deb6cf44edaadd741def4c`.
Their MIT notice is stored beside those six files in [src/catchtheflip/LICENSE](src/catchtheflip/LICENSE);
[src/catchtheflip/README.md](src/catchtheflip/README.md) identifies exactly which code it covers.
The package initializer is reduced to avoid importing leaderboard or notebook tools.
Only detector-related analysis is exposed by this project's entry point.

The [Tier A](https://aqora.io/datasets/Alice_Bob/catch-the-flip-tier-a) and
[Tier B](https://aqora.io/datasets/Alice_Bob/catch-the-flip-tier-b) dataset pages
both declare **MIT** (`https://spdx.org/licenses/MIT.html` in their public
structured metadata, checked 2026-11-22); the pages identify David Schlegel as
creator and Alice_Bob as publisher/namespace.
The supplied Alice & Bob copyright notice is reproduced in [data/LICENSE](data/LICENSE).
The arrays are redistributed as local NumPy archives of the published `v1.0.0`
splits; test labels are absent and have not been reconstructed.
[data/manifest.json](data/manifest.json) records provenance and checksums.

The theory and presentation PDFs retain their original **Cube it - Alice!** team
attribution and are copied unchanged; no new reuse license is asserted for those
documents. The submitted Step-3 report is preserved in `docs/submitted_results.md`.
The project code added here is MIT licensed under [LICENSE](LICENSE).
