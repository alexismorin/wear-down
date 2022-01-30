# wear-down
## One-click Maya 2020+ Python script to wear down shapes into game-ready old concrete

![header](/images/header.png)

Just select a low-poly mesh of your choosing and run the script. Looks at all the edges, chunks pieces off and then remeshes the whole thing with a bit of noise to make the surface more uneven.

### Variables

- minChunkScale/maxChunkScale: How big the chunks taken off the mesh are by default

- chunkDeformScale: Multiplier for how deformed chunks are based on the length of their associated edge

- chunkRatioPerUnit: Probability of chunking per edge length. 1.5 means that for a 2 meter edge, you get three chunks.

![footer](/images/footer.png)