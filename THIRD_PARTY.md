# Third-party components

- HyperFrames 0.9.19: installed through npm; Apache-2.0. The core authoring skills in `Misc/` are included as workflow references. Upstream: https://github.com/heygen-com/hyperframes
- GSAP 3.15.1: pinned npm dependency and a bundled browser runtime in each composition's `assets/vendor/`. Licence header preserved. Terms: https://gsap.com/standard-license/
- Inter: SIL Open Font License; `licenses/OFL-Inter.txt`.
- Caveat: SIL Open Font License; `licenses/OFL-Caveat.txt`. Used only for short handwritten annotations in diagrams.
- Other OFL fonts whose licence texts sit in `licenses/` are not bundled in the template; the texts are kept so a copy that adds them stays compliant.
- The npm lockfile overrides HyperFrames' transitive Undici dependency to 7.30.1 to address npm audit advisories while keeping the tested renderer version.

Your footage, music, brand and content brain are yours. Including a music track in a release does not grant anyone else publication rights to it.
