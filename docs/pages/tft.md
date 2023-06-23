# Temporal Fusion Transformer
To understand the rationale behind choosing TFT [14] for
this study, we give a theoretical background of TFT and its
self-attention weights, which we later extract to interpret the
spatiotemporal patterns of COVID-19 infection.

## Design

TFT architecture [14]. TFT effectively builds feature
representation from static covariates, observed inputs, and
known future events. The transformer adopts four key layers
from the bottom: (L1) Embedding & Input Transformation,
(L2) Variable Selection, (L3) LSTM, (L4) Self-Attention.

## Model Architecture

The figure shows a brief overview of the TFT model architecture
for three types of input covariates and the target output. We
highlighted four key components of the model as follows:

## Attention Wieght in TFT

TFT uses the self-attention mechanism to learn long-term
time-dependent relationships.

## Attention

Figure 5