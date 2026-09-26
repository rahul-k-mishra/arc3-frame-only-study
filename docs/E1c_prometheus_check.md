# E1c check: ZubMono "Prometheus"

Checked 26 September 2026, reading only. Nothing was cloned, adapted or run. Files were downloaded
from raw.githubusercontent.com at a fixed commit and read in a scratch folder:
- **Repository:** github.com/ZubMono/arc-prize-2026, subfolder `arc-agi3-kaggle-agent/`.
- **Commit:** d2d574a98ba17714d0ca4b17045afdb5bdb50d80, HEAD on 26 September 2026 (confirmed with
  `git ls-remote` immediately before download).
- **File checked:** `agent/my_agent.py` (10,683 lines). It is the shipped agent: a bundle of the
  `arc_agent/` modules, each introduced by a marker line such as
  `# ============ arc_agent/priors.py ============` (line 415). Every line number below is in
  this file unless another file is named.
- **Protocol:** docs/TOG_PLAN_v2.md Section 3.1 (A1-A7) and docs/E1c_search.md.

## Verdict (author, 26 September 2026): REJECTED

Prometheus is rejected as an E1 agent. Its `DIRECTION_PRIORS` were measured on all 25 public
games, which include our 17 held-out games, so the agent carries parameters fitted on our
evaluation set, and A5 forbids removing them. The size of the priors is irrelevant; the
contamination is the reason. Check (4) and an adapter are not pursued.

## Result

**Check (3) fails: the agent ships pretrained weights fitted offline on recorded ARC-AGI-3
games.** Among them is a direction prior measured on all 25 public games, which include our 17
held-out games. As instructed, the check stops at this first failure. Checks (1) and (2) pass;
check (4) was not carried out.

| check | result |
|---|---|
| (1) nothing keyed on a public game id | **pass** |
| (2) no reading of game source, metadata.json or environment_files | **pass** |
| (3) no pretrained weights, model files or network calls; stdlib (+ numpy) only | **FAIL** (pretrained weights) |
| (4) API compatible with arc-agi 0.9.8 offline; entry point and loop | not carried out |

## (1) No branch, table, constant or configuration keyed on a public game id: PASS

Method:
- **Tokens:** the file was tokenised with Python's `tokenize`. Every match of the 25 public game
  ids (whole-word, case-insensitive) was classified as a comment, a docstring or bare string
  statement (identified with `ast`: an `Expr` whose value is a string constant), or code (a name,
  a string used as a value, an f-string, anything else).
- **Version hashes:** the 25 version hashes (the directory names under `environment_files/`,
  listed without opening any file) were searched the same way.

Result:
- 163 mentions of the 25 ids: 69 in comments, 94 in docstrings or bare string statements,
  **0 in code**.
- The version hashes appear only in comments and docstrings. For example:
  - line 2421: `# fondo GLOBAL de la grilla no sirve: en dc22-fdcac232 el color mas frecuente del
    frame es la pared`
  - line 5536: `# oficial sobre tr87-cd924810, en 10 transiciones reales de 64x64 la BFS profunda
    explico CERO y`
  - line 7470: `#: lp85-305b61c3 gasto 403 de 499 clicks en la cenefa decorativa del borde. ...`
  - lines 6720-6721, inside a docstring: `partida era ciclado PERFECTO: ar25-0c556536 {A1:15,
    A2:16, ...}`

  These record measurements; none is read by code.
- Per id: lp85 30, vc33 15, dc22 14, ft09 13, ar25 12, sp80 9, cn04 8, ka59 8, lf52 8, tn36 8,
  sb26 7, su15 6, g50t 3, re86 3, tu93 3, bp35 2, r11l 2, s5i5 2, sc25 2, sk48 2, tr87 2, cd82 1,
  ls20 1, m0r0 1, wa30 1.

Every use of `game_id` in code (from `ast`), 4 in all, none of which branches on its value:
- line 395: `game_id: str` (a dataclass field);
- line 10563: `game_id=str(frame.game_id or ""),` (frame conversion);
- line 10618: `semilla = self.SEMILLA if self.SEMILLA is not None else
  f"{self.game_id}.{time.time_ns()}"` (a random seed);
- line 10626: `self._manija_de_reloj = self._reloj.registrar_partida(str(self.game_id))` (per-game
  time accounting).

Signature tables (a game can be recognised without its id, e.g. by a hash of its first frame): no
literal dict, set, list or tuple in the file has hex-like string keys or three or more large
integers. The four literal collections with 12 or more elements are:
- `DIRECTION_PRIORS` (line 468), keyed by action names and counts;
- a `__slots__` tuple (line 7626);
- two internal diagnostic dicts (lines 4290, 4773).

The priors section itself states the rule the authors enforce (lines 425-426): "QUE NO PUEDE
CONTENER: claves con forma de game_id (`abcd-01234567`) ni de firma de estado (entero de 32 bits)"
("it may not contain keys shaped like a game_id ... nor like a state signature").

Recorded as a caveat, not a failure of (1): constants were tuned by measurement on the public
games. Examples:
- `CLICS_DE_WARMUP = 9` (opening book section, starting line 9071) is justified by "Nueve
  destrabaron a los dos juegos con pantalla de titulo que la sonda midio" ("nine unlocked the two
  title-screen games the probe measured");
- the opening-book docstring counts "5 [of the 25 public games] arrancan en un estado donde las
  flechas no tocan el tablero".

## (2) No reading of game source, metadata.json or environment_files at play time: PASS

A raw-line search over the whole file found **no line at all** (code, comment or string)
containing:
- `importlib`;
- `glob`;
- `open(`;
- `os.listdir`, `os.walk` or `os.scandir`;
- `pathlib` or `Path(`;
- `metadata.json`;
- `exec(`, `eval(`, `compile(` or `__import__(`;
- `sys.modules`, `_getframe`, `inspect` or `gc.`;
- `Arcade`, `._game`, `LocalEnvironmentWrapper`, `environment_info` or `.env`.

The single line containing `environment_files` is text inside a docstring:
- line 10443: ``        `environment_files/`) y esa evidencia no llega a ningun lado si nadie la mira.``

The file's imports (all of them, module-level and nested, from `ast`) contain no module that could
read files by path other than `os`. `os` is used exactly twice, both times to read environment
variables:
- line 138: `fuente = os.environ if entorno is None else entorno`
- line 805: `return cls.desde_texto(os.environ.get(NOMBRE_DE_VARIABLE))`

There is no `os.path`, `os.getenv` or other `os.` use.

## (3) No pretrained weights, model files or network calls; standard library plus numpy only: FAIL

The bundle ships weights fitted offline. Its own text says so:
- line 420: "Es el UNICO conocimiento pre-computado que viaja al notebook de submission: pesos del
  ranker"
- line 421: "de coordenadas (regresion logistica contra clicks REALES etiquetados con 'el click
  cambio la"
- line 422: "grilla'), umbrales medidos de los detectores, orden de acciones por efectividad
  observada y"
- line 423: "-- BL.21590 -- el prior de DIRECCIONES indexado por CONJUNTO DE ACCIONES DISPONIBLES."

("It is the ONLY pre-computed knowledge that travels to the submission notebook: weights of the
coordinate ranker (logistic regression against REAL clicks labelled 'the click changed the grid'),
measured detector thresholds, the order of actions by observed effectiveness, and the direction
prior indexed by the set of available actions.")

The embedded values:
- **`CLICK_PRIORS` (lines 437-466):** `"nJuegosObservados": 5` (line 440) and
  `"nTransicionesObservadas": 749` (line 441). Its `"pesosClick"` (lines 442-452) are nine
  logistic-regression weights, from `-2.241823` (line 443) to `-0.135375` (line 451). It also
  holds `"umbralesDetectores"` (fitted thresholds, e.g. `"probabilidadMinimaDeClick": 0.245268`,
  line 454) and `"ordenAcciones"` (an action order by observed effectiveness, from line 457).
- **`DIRECTION_PRIORS` (from line 468):** `"nJuegosMedidos": 25` (line 469),
  `"nJuegosConFlechas": 17` (line 470), `"nJuegosQueConfirman": 11` (line 471), and a canonical
  action-to-direction map. It was measured on the 25 public games, which include all 17 of our
  held-out games.

Where they came from, `scripts/fit_click_priors.py` at the same commit:
- lines 1-3: "ajusta los PRIORS DE CLICK contra el corpus REAL de partidas y los emite a los dos
  puertos (`arc_agent/priors.py` y ...)";
- lines 10-12: "DE DONDE SALE EL DATO. Dos fixtures REALES, grabados contra la API oficial de
  ARC-AGI-3:", i.e. two fixtures "grabados contra la API
  oficial de ARC-AGI-3" (recorded against the official ARC-AGI-3 API), `clickRealFrames.json`
  (ranker weights) and `volatilityRealGames.json` (action order).

Which 5 games the click weights were fitted on was not determined; the fixture files were not read.

They are used at play time:
- line 7675: `self._pesos = tuple(pesos if pesos is not None else CLICK_PRIORS["pesosClick"])`
  (click ranker);
- lines 6937 and 6941 (`prioridad_por_priors`, from `CLICK_PRIORS["ordenAcciones"]`), used in the
  cold start per line 6917: "`prioridad_por_priors` entra SOLO en el arranque en frio";
- lines 7967 and 8404: `DIRECTION_PRIORS` seeds the direction belief. The authors describe it as
  a refutable initial hypothesis that play can overturn (lines 431-433).

Why this fails the check as written. Check (3) excludes pretrained weights, and these are weights
of a model fitted offline on recorded games, shipped in code rather than in a model file. The
direction prior is additionally measured on our evaluation games. The nuance, for the author's
judgement:
- it is small: 9 regression weights, 2 thresholds, an action order and a 4-entry direction map;
- it is not a neural network;
- the direction prior is overridable by evidence during play.

Removing it would edit the policy, which A5 forbids. Running the agent unchanged would measure an
agent that was partly fitted on our held-out games, so it would not be prior-free on them.

Not completed because the check stopped at the first failure: the network-call part of (3). The
imports found (the list in (2)) are standard library plus `arcengine` and the framework's
`agents.agent`; no `numpy`, and no `socket`, `urllib`, `http` or `requests` import appears in that
list, but a dedicated search was not run.

## (4) API compatibility with arc-agi 0.9.8 offline: not carried out

Stopped at the failure of (3). For the record, only what (2) and (3) already showed: the bundle
imports `from agents.agent import Agent` and `from arcengine import FrameData as FrameOficial`
(and `GameAction`, `GameState`), i.e. the ARC-AGI-3-Agents framework interface on the current
engine types. Its entry point and action loop were not examined.

## Go / no-go on A1-A4

| item | status | evidence |
|---|---|---|
| A1 pinned code, licence, commit | would be met | commit d2d574a98ba17714d0ca4b17045afdb5bdb50d80; `arc-agi3-kaggle-agent/LICENSE` line 1 "MIT No Attribution", line 3 "Copyright 2026 ZubMono" |
| A2 licence permits research use and modification | met | MIT-0 |
| A3 CPU only | met on the evidence read: standard library only, no numpy, no GPU library | import list in (2) |
| A4 no LLM or network at play time | no LLM import found; network not searched separately (stopped at (3)) | import list in (2) |

**Overall: NO-GO as a prior-free independent agent under the check as specified**, because of (3).
**Author's verdict (above): rejected**, for the contamination of the direction prior by the held-out games.
A1 and A2 would be met, and A3 and A4 are not contradicted by anything read.

The deciding question is the author's:
- **If 9 regression weights fitted on 5 recorded games, plus a direction prior measured on all 25
  public games, disqualify it:** it is out.
- **If they are accepted as small, overridable priors:** the E1 result would have to state them,
  and state that the direction prior was measured on the held-out games. In that case the next
  step would be check (4) and then an adapter.

What an adapter would have to touch, from what was read. This is not a full list, since (4) was
not done:
- the framework `Agent` I/O (its `take_action`/main loop), as for E1a;
- the seed at line 10618, which falls back to wall-clock time unless the class attribute
  `SEMILLA` is set: set `SEMILLA` from our seed;
- the time budget, which reads the environment variable `ARC_PRESUPUESTO_SEGUNDOS` (line 97,
  default `PRESUPUESTO_POR_DEFECTO_SEGUNDOS = 8.0 * 60 * 60`, line 80) and has an action safety
  cap `COTA_DE_SEGURIDAD_DE_ACCIONES = 4000` (line 111), which would interact with our
  20,000-action budget and must be examined;
- feature flags read from `ARC_AGENT_BANDERAS` (line 615), which should be left at their shipped
  default.

None of these touches the priors. Removing the priors is not an adapter change; it would be a
policy edit.
