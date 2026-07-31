Awarding-body marks for the Selected Honors section.

Reference one from data/honors.yml with `logo: "images/logos/<file>"`. SVGs are
served as-is; raster files are resized to 48px tall (2x the 24px they display
at) and converted to WebP. Entries without a logo simply show no mark.

Marks render in greyscale and regain their colour on hover, so they sit inside
the monochrome design rather than fighting it. Each is the organisation's own
file, used unaltered, to identify who granted the award.

  igem.svg                iGEM
  wehi.jpeg               Walter and Eliza Hall Institute
  zju.png                 Zhejiang University (3 entries)
  synbio-competition.png  National Synthetic Biology Innovation Competition
  csbt.webp               Chinese Society for Biotechnology        (unused)
  siat-synbio.png         Shenzhen Institute of Synthetic Biology  (unused)

The last two are the co-organisers of the synthetic biology competition; the
row currently shows the competition's own mark instead. Swap the path in
data/honors.yml to use one of them.

Prefer a square emblem over a horizontal wordmark — at 24px tall, lettering in a
combination mark is hard to read.
