Recall all the representations that have been presented.
Which mutation and recombination operators are compatible with which representations?

# Binary representation

Genotype: e.g. 10001
Phenotype: e.g 10001

## Mutation

### Bit flip

Sannsynlighet `p_m`. Størrelse på `p_m` avhenger av hva man ønsker å oppnå. Lav mutering dersom alle individer skal ha high fitness, høy mutasjon dersom man kun trenger én, eller få med høy fitness.

## Recombination

### One-point crossover

Fare for _positional bias_.
    - p1: 0000|10000  ->  0000|00001
    - p2: 1101|00001  ->  1101|10000

### n-point crossover

    - p1: 0000|10|000  ->  0000|00|000
    - p2: 1101|00|001  ->  1101|10|001

### Uniform crossover

Hver posisjon i offspring1 har en sannsynlighet p for å få en gen fra P1, ellers fra P2. offspring2 får invertert mapping.

Ingen _positional bias_, men med p = 0.5 så vil gjennomsnittlig halvparten av genene overføres (_distributional bias_).

    - p1: 000010000  ->  010110000
    - p2: 110100001  ->  100000001

# Integer representation

Genotype: e.g. 101 (binary)
Phenotype: e.g. 5

## Mutation

### Random resetting

Bruker bit-flips. Passer for _cardinal attributes_ der det ikke er noe _ordering_.

### Creep mutation

Endrer verdien litt og litt. Passer for _ordinal attributes_ (der rekkefølge er viktig).

## Recombination

Tilsvarende som med binært. _Blending_ er ikke like aktuelt ettersom gjennomsnitt av even/odd vil generere floating point.

# Floating point representation / Real valued representation

Verdiene kommer fra en kontinuerlig, i stedet for en discrete distribusjon.

## Mutation

- Uniform mutation. Endre alle gener med sannsynlighet p. Tilsvarer bit-flip / random resetting
- Nonuniform mutation ligner på creep mutation. Endres med guassisk distribusjon.

## Recombination

### Simple arithmetic recombination

Ligner litt på one-point crossover. Ta (xi + yi / alpha) av verdiene fra P1 og P2 etter recomb point. Her med alpha = 0.5:

0.1 0.2 0.3 0.4 0.5 0.6 | 0.7 0.8 0.9  >  0.1 0.2 0.3 0.4 0.5 0.6 | 0.5 0.5 0.6
0.3 0.2 0.3 0.2 0.3 0.2 | 0.3 0.2 0.3  >  0.3 0.2 0.3 0.2 0.3 0.2 | 0.5 0.5 0.6

### Single arithmetic recombination

Lik som den over, bare at du tar én gen i stedet for alle til høyre for recomb point.

### Whole arithmetic recombination

Lik som de over, bare at man gjør det på alle genene. Hvis alpha er 0.5 så vil offspring være like.

### Blend crossover

?????

# Permutation representation

Passer når man endrer rekkefølgen på genene, men at verdiene på hvert gen er lik.

## Mutation

### Swap mutation

To gener er valgt random og deres verdi (allele) er byttet.

### Insert mutation

To gener er valgt random og den siste er satt rett til høyre for den første.

### Scramle mutation

Re-order alle, eller et subsett av chromosomet.

### Inversion mutation

Velg to posisjoner og bytt rekkefølge på innholdet i dem.

## Recombination

Utfordring her er at man ikke kan hente tilfeldige verdier fra P1 og P2 og samtidig opprettholdet kravet om at verdiene skal være like.

### Partially mapped crossover

1: Kopier først et random valgt segment fra P1:

123|4567|89
             > xxx4567xx
937|8265|14

2: Ta utgangspunkt i tilsvarende segment i P2 og plasser der som P2s verdi av P1s tilsvarende plass er. Finn P1s verdi av P2s første verdi i segmentet ('8'). P1s tilsvarende verdi er '4'. Plasser '8' i offspring der P2 har '4'.

123|4567|89
             > xxx4567x8
937|8265|14

Så tallet '2', finn P2s verdi av '5', som er i segmentet. Gjør derfor tilsvarende - finn P2 plassering av verdi 7 (som er over P2s plassering av 5) og plasser '2' i offspring der P2 har '7:

123|4567|89
             > xx24567x8
937|8265|14

3: Ettersom resten av tallene er i segmentet så kan resten av tallene kopieres rett fra P2:

123|4567|89
             > 932456718
937|8265|14

### Edge crossover

????

### Order crossover

Beholver _relativ order_ fra P2.

1: Begynner likt som PMX ved å kopiere et segment fra P1 over i offspring.

123|4567|89
             > xxx4567xx
937|8265|14

2: Kopier resten av allelene slik de opptrer i P2 - hopp over alleles som allerede finnes i offspring.

123|4567|89
             > 382456719
937|8265|14

3: Offspring 2 kan lages ved å invertere rollene (Start med P2).

### Cycle crossover

Fokus på _absolutt posisjonering_ av hvor elementene opptrer.

Offspring lages ved å alternere sykluser.

Én syklus er:

1. Starter med første ubrukt posisjon i P1 og tilsvarende posisjon i P2. ('1' og '9').
2. Gå til posisjonen med samme allele i P1. ('9' er i siste posisjon i P1)
3. Repeat frem til du kommer til første allele ('1')
4. Repeat runde men nå får children alleler kopiert motsatt

Round 1:

123456789  >  1xx4xxx89
937826514  >  9xx8xxx14

Round 2:

Nå blir alleler kopiert motsatt

123456789  >  13742x589
937826514  >  92385x714

Round 3:

123456789  >  123456789
937826514  >  937826514


# Tree representation

## Mutation

Velg en node i treet og replace noden med et random generert tre.

## Recombination

### Sub-tree crossover

Finn to junctions i hhv P1 og P2
Swap de to subtrærne
