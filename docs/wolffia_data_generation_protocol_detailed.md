# Beginner-Friendly Guide to the Wolffia Data-Generation Protocol

## What this document is for

This file is the **simple explanation** that goes with the formal PDF protocol.

The PDF is meant to look professional and shareable.
This file is meant to help **you understand what we are actually doing**, why we are doing it, and what each stage needs.

If you are new to wet-lab single-cell work, start here.

## The big picture

Our goal is to generate our **own Wolffia transcriptomic dataset**.

That means we want to take harvested Wolffia fronds or pooled whole plants, prepare them in a way that preserves useful RNA information, sequence them, and then analyze the result computationally.

But we should not start by trying to do the biggest experiment possible.

The smart first goal is:

> can we get clean, interpretable Wolffia RNA data at all?

That is the first question because plant single-cell experiments often fail at the **sample-preparation step**, not at the sequencing step.

## Why Wolffia is tricky

Wolffia is interesting because it is a tiny, highly reduced flowering plant.

That makes it biologically exciting, but technically it can also make things harder:

- plant cells have cell walls
- dissociation can damage cells
- damaged plant material can release debris
- chloroplast-rich material can complicate RNA measurements
- harsh preparation can create artificial stress signatures

So before we do a big experiment, we need to find out which preparation method is gentler and cleaner for Wolffia.

## The core idea of the protocol

We are comparing **two ways of preparing Wolffia for RNA sequencing**.

### Option 1: intact cells

This means we try to digest the cell wall and recover whole living cells.

You may also hear this described as:

- protoplast preparation
- intact-cell isolation
- cell-based single-cell RNA-seq

### Option 2: nuclei

This means we do **not** try to recover whole living cells.
Instead, we break open the harvested fronds or pooled plant material gently and isolate nuclei.

This is often easier in plants because:

- you do not have to fully digest the wall
- the preparation may be less harsh
- you may get less technical stress

## What "tissue" means here

In a big plant, "tissue" might mean a root tip, a leaf piece, or a stem segment.

In `Wolffia australiana`, that word can sound confusing because the plant is so small.

In this project, when we say "tissue," we usually mean:

- a pooled batch of Wolffia fronds
- or a pooled batch of whole tiny plants taken from culture

So we are usually not dissecting one large organ.
We are handling many tiny plants together as one sample.

That is also why a paper may say the sample was "diced with a razor blade."
It does **not** mean someone is slicing one microscopic plant at a time.
It means a pooled sample of many small plants is chopped gently in bulk to help enzyme solution get through the outer surface.

## Our actual first experimental question

The first real question is not:

- how many cell types does Wolffia have?

The first real question is:

- which input type gives us cleaner data: cells or nuclei?

That is why the protocol starts with a **pilot comparison**.

## Overview of the stages

There are five main stages:

1. grow healthy Wolffia in a standardized way
2. inspect and document the material before prep
3. run a pilot for intact cells
4. run a pilot for nuclei
5. choose the better route and scale up

Below I explain each one like we are planning the experiment together from scratch.

## Stage 1: Grow healthy Wolffia in a standardized way

### What we are doing

We want all starting material to be as similar as possible.

That means using:

- one Wolffia line
- one growth medium
- one light schedule
- one temperature range
- one harvest time window

### A very good benchmark starting condition

The 2024 `Genome Research` paper on `Wolffia australiana` gives us a useful benchmark instead of making us guess from generic plant culture advice.

Their reported baseline was:

- `0.5x` Schenk and Hildebrandt medium
- `0.1%` sucrose
- `pH 6.7`
- `12 h light / 12 h dark`
- `24 C`
- about `100 uE` light intensity
- weekly subculture by transferring about `10 fronds`

That does **not** mean every lab must use exactly that forever.
It just means this is a credible place for us to start if we want a Wolffia-specific benchmark.

### Why this matters

If the starting cultures are inconsistent, then later we will not know whether differences in the sequencing data are:

- real biology
- or just differences in growth conditions

### What samples we need

We need:

- healthy vegetative Wolffia
- enough biomass for pilot testing
- ideally three biological replicates later for the real run

### What instruments are needed

At this stage, the setup is pretty basic:

- growth chamber or stable culture area
- light source
- thermometer or chamber logging
- pipettes
- sterile culture vessels

### What materials are needed

- Wolffia stock or culture line
- growth medium
- sterile water or rinse buffer if needed
- sterile plastics
- labels
- metadata sheet or spreadsheet

### What to write down

Always record:

- stock or genotype ID
- medium
- light cycle
- temperature
- harvest date
- visible growth condition

### Beginner tip

This may feel boring, but it is important.
A lot of experimental confusion comes from bad record keeping at the beginning.

## Stage 2: Check the material before doing anything expensive

### What we are doing

Before we start dissociation or nuclei prep, we simply look at the plants and ask:

- do they look healthy?
- do they look similar across replicates?
- is there enough material?

### Why this matters

If the culture is already stressed, dirty, or old, then a bad single-cell result does not tell us much.

### What instruments are needed

- brightfield microscope or stereomicroscope
- camera or phone adapter
- optional balance for wet weight

### What we are checking

- frond appearance
- budding status
- contamination
- visible debris
- approximate biomass

### What the output should be

At the end of this stage, we should have:

- a few images
- a biomass estimate
- a go/no-go decision

### Beginner tip

If the material looks bad, stopping is not failure.
It is better to pause here than to waste sequencing resources.

## Stage 3A: Pilot for intact-cell preparation

### What we are trying to do

Here we try to recover **whole cells** from Wolffia.

Because plant cells have cell walls, this usually means using enzymes that digest the wall.

### What “pilot” means here

We are **not** doing the final experiment yet.
We are testing whether this method works well enough to deserve a larger run.

### What samples are needed

- freshly harvested healthy Wolffia
- enough material to test a few preparation conditions

### What instruments are needed

- fresh sterile razor blade or another very fine cutting tool
- microscope
- `100 um` sieve or mesh filter
- `40 um` cell strainer
- centrifuge for gentle pelleting
- hemocytometer or cell counter
- timer
- optional shaker or rocker

### What reagents are needed

- osmotic stabilization buffer
- cellulase-type enzyme
- pectinase or macerozyme-type enzyme
- salts and buffer components
- optional viability dye

If we want to start close to the published `Wolffia australiana` benchmark, the paper used a digestion mix containing:

- `0.1 M KCl`
- `0.02 M MgCl2`
- `0.1% BSA`
- `0.08 M MES`
- `0.6 M mannitol`
- `pH 5.5`
- `1.5% cellulase R-10`
- `1% maceroenzyme`
- `0.5% pectolyase`

### What happens during this stage

Very simply, we:

1. collect fresh Wolffia
2. rinse it gently
3. if we follow the literature benchmark, gently dice the pooled fronds or tiny plants with a fresh razor blade
4. incubate the material in a digestion mix
5. filter first through a `100 um` sieve and then a `40 um` strainer
6. wash and collect the released cells
7. count them and check viability

### What the razor-blade step really means

This part is easy to misunderstand, so here is the practical interpretation.

Because `Wolffia australiana` is tiny and has a relatively tough outer surface, the published paper diced pooled plant material with a razor blade before enzyme digestion.

That means:

- place many harvested fronds or plants together in a small sterile dish or on a sterile surface
- use a fresh sterile razor to chop the pooled sample gently into smaller pieces
- do this only long enough to improve enzyme access
- do **not** grind, mash, or over-homogenize the sample

So the blade is being used on a pooled sample, not on one single tiny frond in isolation.

### What we are measuring

We want to know:

- how many cells we got
- whether the cells look intact
- whether they are clumped
- whether there is too much debris
- whether the preparation seems harsh

### What “good” looks like

Good signs:

- reasonable cell yield
- visible intact cells
- not too much clumping
- not too much debris
- reproducible results across similar prep attempts

### What “bad” looks like

Bad signs:

- broken-looking cells
- very low recovery
- poor viability
- lots of debris
- only very harsh digestion gives any result

### Beginner tip

If this route looks ugly, that does **not** mean the project failed.
It may just mean Wolffia is better suited to nuclei prep.

## Stage 3B: Pilot for nuclei preparation

### What we are trying to do

Instead of recovering whole cells, we recover **nuclei**.

This can be easier in plants because we do not need to preserve the whole cell structure.

### What samples are needed

- freshly harvested Wolffia
- material kept cold during the whole prep

### What instruments are needed

- ice bucket or cold block
- Dounce homogenizer or similar tool
- filters or strainers
- refrigerated centrifuge
- microscope
- nuclei counting setup

### What reagents are needed

- nuclei isolation buffer
- appropriate lysis chemistry
- RNase-safe consumables
- optional DNA stain for counting

### What happens during this stage

Very simply, we:

1. collect Wolffia onto ice
2. homogenize gently in nuclei buffer
3. filter debris away
4. collect nuclei
5. inspect them
6. count them

### What we are measuring

We want to know:

- how many nuclei we got
- whether the nuclei look intact
- whether they are clumped
- whether there seems to be lots of contamination or debris

### What “good” looks like

Good signs:

- clear nuclei
- manageable debris
- reasonable recovery
- reproducible results

### What “bad” looks like

Bad signs:

- ruptured nuclei
- heavy contamination
- severe clumping
- very poor yield

### Beginner tip

In plants, nuclei prep is often a very respectable option, not a fallback of shame.
If nuclei are cleaner, we should use nuclei.

## Stage 4: Choose the better route

### What we are doing

Now we compare the two pilots side by side.

We are asking:

- which route gives cleaner material?
- which route gives more reproducible recovery?
- which route is less likely to generate technical artifacts?

### How we decide

Choose the route that is better on things like:

- yield
- integrity
- debris burden
- clumping
- likely stress artifact burden
- reproducibility

### Very important principle

Do **not** choose the route just because it sounds more exciting.

Choose the route that is more likely to give interpretable data.

## Stage 5: Run the first real experiment

### What we are doing

Once we choose the better route, we stop piloting and run the first real data-generation experiment.

### What changes if the lab is using PIP-seq

This is actually useful news, because it makes the plan more specific.

For us, it means we should stop talking about a generic future platform and start planning around the requirements of `PIP-seq`.

The biggest practical consequences are:

- we need to confirm whether the lab's `PIP-seq` workflow expects intact cells, nuclei, or can work with either input
- we should focus on a clean, low-debris, low-clump suspension
- we should respect the platform's acceptable concentration or loading range
- we should keep replicate handling very uniform so batch effects do not get confused with biology

In other words, `PIP-seq` does **not** remove the hard part of the project.
It mostly means the hard part becomes even more clearly the sample-preparation and handoff stage.

### What the design should look like

The first run should be simple:

- one biological condition
- healthy vegetative Wolffia
- three biological replicates
- one fixed preparation route
- one fixed library-prep workflow

### Why keep it simple

Because the goal of the first run is:

- to generate a clean Wolffia reference
- not to answer every biological question at once

### What instruments are needed now

This depends on the final library platform, but usually includes:

- everything from the chosen prep route
- library-prep kit workflow
- PCR or amplification equipment
- library quantification tools
- fragment analysis if available
- access to a sequencing core or sequencing platform

If the platform is `PIP-seq`, also make sure we have:

- the exact input specification from the lab or core
- target concentration guidance
- any restriction on debris load or filter size
- the expected number of cells or nuclei to load
- the exact sample-submission format they want

### What metadata we must keep

For every sample, record:

- sample ID
- replicate ID
- stock ID
- medium
- light cycle
- temperature
- harvest time
- operator
- prep route
- prep condition
- viability or nuclei-integrity notes
- library batch
- sequencing batch

### Beginner tip

Good metadata is part of the experiment.
It is not just paperwork.

## What happens after sequencing

Once sequencing is done, we move back into the computational side.

The first questions will be:

1. do the replicates look reasonably consistent?
2. do we recover broad expected programs?
3. do we see strong technical artifacts?
4. do the results match any of our current Wolffia predictions?

For a `PIP-seq` dataset, we should also explicitly check:

5. is there evidence of high ambient RNA background?
6. do we see likely doublets or overloaded partitions?
7. do the clusters look biologically structured rather than prep-driven?

### What outputs we expect

- QC summaries
- UMAP
- marker-gene tables
- module-score plots
- program-level interpretation

## What counts as success

The first experiment is successful if we recover at least some broad Wolffia programs clearly enough to interpret them.

For example:

- proliferative-like cells or nuclei
- photosynthetic program
- transport or interface-associated program
- developmental transition-like signal

We do **not** need perfect fine-grained cell labels immediately.

## What not to do

Avoid these mistakes in the first run:

- mixing many biological conditions at once
- chasing rare flowering states too early
- assuming a literature enzyme recipe will automatically work
- ignoring prep quality because sequencing is expensive
- over-interpreting technical stress as novel Wolffia biology

## Simple timeline

### Week 1

- standardize growth conditions
- organize metadata sheet

### Week 2

- run intact-cell pilot
- run nuclei pilot

### Week 3

- compare the pilots
- choose the better route

### Week 4

- run the first real prep
- prepare libraries
- submit sequencing

### Week 5 onward

- do computational QC
- cluster the data
- compare results with our prediction framework

## Final takeaway

If you remember only one thing, remember this:

> the best first Wolffia experiment is the cleanest one, not the biggest one

That means:

- healthy input material
- a fair pilot comparison
- an evidence-based decision between cells and nuclei
- three clean biological replicates
- immediate computational follow-up

That is how we give ourselves the best chance of getting useful Wolffia data.
