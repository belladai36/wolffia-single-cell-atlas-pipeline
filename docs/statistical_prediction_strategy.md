# Statistical Prediction Strategy Using Existing Public Data

## Purpose

This document defines how the project can use public single-cell plant datasets as training and reference data for statistical prediction before any new `Wolffia australiana` SMART-seq data arrive.

The goal is to make prediction computational, not only descriptive.

## Core Idea

We will use existing annotated plant single-cell datasets to learn patterns of:

- broad cell programs
- marker co-expression structure
- developmental gradients
- cluster separability

Then we will use those learned patterns to generate predictions about what a Wolffia dataset is likely to look like.

## Statistical Tasks

### 1. Program Scoring

For each reference dataset, compute module or gene-program scores for:

- proliferative / meristematic programs
- photosynthetic / assimilation programs
- vascular-like / transport programs
- developmental transition programs
- epidermal / surface identity programs
- reproductive / floral programs
- aquatic adaptation / stress-responsive programs

Why it helps:

- lets us compare broad biological programs across datasets without relying on exact one-to-one cell-type labels

## 2. Classification of Broad States

Train classifiers on public reference datasets to distinguish broad cell-program classes.

Examples:

- multinomial logistic regression
- random forest
- support vector machine

Target labels should stay broad:

- proliferative
- photosynthetic
- transport-associated
- transitional
- surface-associated

Why it helps:

- provides a quantitative measure of how separable these programs are in existing plants
- gives us a direct way to predict whether Wolffia is more likely to have cleanly separable or weakly separable states

## 3. Dimensional Reduction and Cluster Separability

Use PCA, UMAP, and graph clustering on reference datasets, then quantify:

- cluster separation
- within-cluster variance
- overlap among broad states

Useful statistics:

- silhouette score
- adjusted Rand index across parameter settings
- marker recovery stability

Why it helps:

- tells us whether some biological programs are naturally discrete or naturally continuous even in well-annotated reference systems

## 4. Trajectory and Continuum Analysis

Use pseudotime or graph-based trajectory methods on public developmental references to estimate:

- how gradual developmental transitions are
- which genes vary early versus late along trajectories
- whether transition programs are more continuum-like than cluster-like

Why it helps:

- directly supports our prediction about whether Wolffia developmental organization may appear as gradients instead of crisp cell types

## 5. Cross-Dataset Transfer

Train on one reference dataset and test on another.

Example:

- train a broad-state classifier on Jean-Baptiste
- test it on Shulse or Denyer

Why it helps:

- measures how robust broad program definitions are across studies
- gives us an estimate of how transferable the learned statistical structure may be

## 6. Ortholog-Aware Transfer to Wolffia

Once Wolffia gene mappings are available, transfer program scores or classifiers using ortholog-mapped features.

Possible approaches:

- score mapped marker modules
- use shared ortholog features in a classifier
- compare Wolffia cells against reference centroids or pseudobulk profiles

Why it helps:

- creates a statistical bridge from annotated references to Wolffia without pretending the species are identical

## Recommended First Statistical Toolkit

For a first implementation, keep the models simple and interpretable:

1. module scoring
2. logistic regression for broad program labels
3. random forest as a nonlinear comparison model
4. silhouette and stability metrics for cluster separability
5. pseudotime summary statistics for developmental references

This is enough to produce meaningful results without overbuilding.

## What We Can Predict Before Wolffia Data Exist

Using only public datasets, we can already estimate:

- which broad plant programs are consistently separable
- which programs tend to overlap even in model systems
- which marker sets are stable across datasets
- whether developmental programs are better modeled as trajectories than clusters
- which program classes are likely to transfer robustly across studies

These are not direct predictions of exact Wolffia cell types.
They are quantitative predictions about the kinds of structure we expect Wolffia data to show.

## Practical Outputs

This statistical layer should produce outputs such as:

- program score tables
- classifier performance summaries
- cross-dataset transfer accuracy
- cluster separability metrics
- trajectory smoothness summaries
- ranked prediction confidence for each Wolffia program

## Best Near-Term Analysis Plan

The most realistic next computational move is:

1. choose one public Arabidopsis reference dataset
2. collapse detailed annotations into broad program labels
3. compute module scores
4. train a simple classifier for broad program identity
5. test transfer on a second Arabidopsis reference
6. summarize which programs are robustly recoverable

That gives the project a real statistical prediction backbone before any Wolffia-specific single-cell data arrive.
