# Full regression results

Complete tables behind Table 1 of the write-up: all 16 survey dimensions,
all 10 dream themes, all 9 inkblot outcomes, the 20 largest of 199 Empath
categories (with BH-FDR q-values), the multiplicity accounting, and what
predicts the register. Every number is produced by a script in this
repository; see README for the mapping.

## A5. Full regression results, all four instruments

Instance-level; `outcome ~ I(denies) + I(hedges) + I(denies)xI(hedges)`; SEs clustered by model. *p<.05, **p<.01, ***p<.001.

**A5.1 — all 16 survey dimensions** (0-10 points; n=7,688; 220 models)

| dimension | denies | hedges | D x H |
|---|---|---|---|
| flow quality | -0.19 | -0.60*** | +0.61** |
| affective temperature | -3.18*** | -0.15 | +1.68*** |
| cohesion | -0.29** | -0.51*** | +0.33* |
| agency | -2.72*** | -0.27* | +1.29*** |
| metacognition | -2.26*** | +0.04 | +0.96*** |
| attention breadth | +0.18 | -0.51*** | -0.07 |
| resolution | +0.35** | -0.53*** | +0.07 |
| friction | -0.52*** | +0.27* | -0.20 |
| phenomenological trust | -3.62*** | -0.97*** | +1.28*** |
| recognition resonance | -2.46*** | -0.50*** | +1.39*** |
| thought complexity | -0.48*** | -0.33** | +0.44** |
| temporal horizon | -1.40*** | -0.26* | +1.13*** |
| error sensitivity | -0.39* | +0.14 | +0.53** |
| context vividness | -0.30* | -0.68*** | +0.48** |
| context salience | +0.00 | -0.03 | -0.65** |
| branching | -0.02 | +0.02 | +0.26 |

**A5.2 — all 10 dream themes** (log-odds; n=8,815; 224 models)

| theme | denies | hedges | D x H |
|---|---|---|---|
| ai interiority | -0.04 | +0.67*** | -0.42* |
| libraries archives | +0.32* | -0.22 | +0.36 |
| cozy sensory | -0.13 | -0.44** | -0.04 |
| speculative worlds | -0.16 | -0.63*** | +0.74*** |
| language meaning | +0.40** | +0.81*** | -0.51** |
| nonhuman personified | -0.46*** | -0.36** | +0.19 |
| surreal absurd | -0.08 | -0.13 | -0.35* |
| cosmic deeptime | +0.02 | -0.42** | +0.28 |
| form constraint | +0.58** | +0.09 | -0.47* |
| time memory loss | +0.40*** | +0.58*** | +0.10 |

**A5.3 — all 9 inkblot outcomes** (judge points; n=1,914; 109 models; blot fixed effects)

| outcome | denies | hedges | D x H |
|---|---|---|---|
| warmth | -0.48*** | -0.30* | +0.22 |
| valence | -0.54*** | -0.37* | +0.34 |
| threat | +0.05 | +0.06 | -0.09 |
| isolation | -0.09 | +0.02 | -0.01 |
| decay | +0.00 | +0.04 | -0.09 |
| confinement | -0.01 | +0.03 | -0.04 |
| animacy | -0.34** | +0.04 | -0.03 |
| content | -0.04 | +0.15 | -0.23 |
| darkness | +0.44* | +0.45 | -0.46 |

The four dark-content codes (threat, isolation, decay, confinement) are null on every term — the registered projective-darkness hypothesis fails; what moves is warmth and valence.

**A5.4 — the 20 largest Empath effects of 199 categories** (outcome SDs; n=8,826; BH-FDR q in brackets, computed within each term across all 199)

| category | denies | hedges | D x H |
|---|---|---|---|
| confusion | +0.026 [0.647] | +0.387*** [0.000] | -0.176* |
| speaking | +0.059 [0.234] | +0.373*** [0.000] | -0.116 |
| communication | +0.099** [0.036] | +0.321*** [0.000] | -0.108 |
| warmth | -0.023 [0.742] | -0.277*** [0.000] | -0.002 |
| smell | -0.181*** [0.001] | -0.275*** [0.000] | +0.080 |
| weakness | -0.065 [0.298] | -0.256*** [0.000] | +0.143* |
| weather | +0.063 [0.328] | -0.253*** [0.000] | -0.067 |
| exasperation | -0.045 [0.163] | +0.244* [0.050] | -0.090 |
| beauty | -0.221*** [0.001] | -0.225*** [0.000] | +0.087 |
| clothing | -0.103* [0.113] | -0.220*** [0.000] | +0.066 |
| musical | -0.218*** [0.000] | -0.176*** [0.000] | +0.104* |
| nervousness | -0.047 [0.341] | +0.215* [0.041] | -0.197* |
| fabric | -0.068 [0.234] | -0.214*** [0.000] | +0.038 |
| office | +0.209** [0.009] | +0.049 [0.207] | -0.071 |
| magic | -0.206*** [0.000] | -0.119* [0.061] | +0.004 |
| heroic | -0.090** [0.019] | +0.201*** [0.001] | -0.019 |
| art | -0.201*** [0.000] | -0.108* [0.070] | +0.036 |
| legend | -0.198*** [0.001] | -0.151** [0.012] | +0.114* |
| music | -0.194*** [0.000] | -0.188*** [0.001] | +0.120* |
| sound | -0.136** [0.009] | -0.194*** [0.000] | -0.002 |

## A6. Multiplicity: observed significance against chance

234 dependent variables, one test per term per variable.

| term | obs. p<.05 (exp. 11.7) | obs. p<.01 (exp. 2.3) | BH q<.05 | Bonferroni p<.05/234 |
|---|---|---|---|---|
| denies | 103 | 71 | 76 | 30 |
| hedges | 112 | 76 | 92 | 36 |
| D x H | 55 | 23 | 13 | 7 |

Of the 13 interaction terms surviving FDR, 7 are survey dimensions and 0 are inkblot codes: the recovery-from-a-floor pattern is largely a self-report phenomenon.

## A7. What predicts the register (R-squared, instance level)

| outcome | predictor | R2 | model-identity ceiling | share of ceiling |
|---|---|---|---|---|
| I(hedge) | the other indicator | 0.004 | 0.442 | 1% |
| I(hedge) | lab fixed effects | 0.186 | 0.442 | 42% |
| I(hedge) | AA intelligence index | 0.090 | 0.509 | 18% |
| I(hedge) | release date (days) | 0.019 | 0.442 | 4% |
| I(deny) | the other indicator | 0.004 | 0.585 | 1% |
| I(deny) | lab fixed effects | 0.269 | 0.585 | 46% |
| I(deny) | AA intelligence index | 0.169 | 0.578 | 29% |
| I(deny) | release date (days) | 0.071 | 0.585 | 12% |

'Ceiling' = R2 from model identity alone on the same rows — the most any model-level covariate can explain. Even the exact model identity leaves most hedging variance (56%) and much denial variance (41%) between instances of the same checkpoint: denial behaves more like a trait, hedging more like a state.
