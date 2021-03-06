function affine(inMin, val, inMax, outMin, outMax) {
  return (((val - inMin) / (inMax - inMin)) * (outMax - outMin)) + outMin;
}

export default function Surface3D(chartState, histogram) {
  if (!histogram) return null;

  const nBins = histogram.numberOfBins;
  const z = [];
  const x = [];
  const y = [];
  for (let i = 0; i < nBins; ++i) {
    const row = [];
    for (let j = 0; j < nBins; ++j) {
      row.push(0);
    }
    z.push(row);
    // x and y make sure the axes reflect the real extent of the binned data.
    x.push(affine(0, i, nBins - 1, histogram.x.extent[0], histogram.x.extent[1]));
    y.push(affine(0, i, nBins - 1, histogram.y.extent[0], histogram.y.extent[1]));
  }

  histogram.bins.forEach((bin) => {
    const xIndex = Math.floor(affine(histogram.x.extent[0], bin.x, histogram.x.extent[1], 0, nBins - 1));
    const yIndex = Math.floor(affine(histogram.y.extent[0], bin.y, histogram.y.extent[1], 0, nBins - 1));

    z[yIndex][xIndex] = bin.count;
  });

  return {
    forceNewPlot: chartState.forceNewPlot,
    traces: [
      {
        x,
        y,
        z,
        type: 'surface',
      },
    ],
    layout: {
      scene: {
        xaxis: {
          title: histogram.x.name,
        },
        yaxis: {
          title: histogram.y.name,
        },
        zaxis: {
          title: 'Count',
        },
      },
    },
  };
}
