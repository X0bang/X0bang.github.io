Awarding-body marks for the Selected Honors section.

Reference them from data/honors.yml with a `logos:` list — one entry per body,
all of them shown. `logo:` with a single path also works. SVGs are served as-is;
raster files are resized to 48px tall (2x the 24px they display at) and
converted to WebP. Entries without a logo simply show no mark.

Marks render in full colour on their own row above the award title. Each is the
organisation's own file, used unaltered, to identify who granted the award.

  igem.svg                iGEM
  igem-zjuchina.png       ZJU-China team
  lumamanta.jpg           LumaManta project
  wehi.jpeg               Walter and Eliza Hall Institute
  zju.svg                 Zhejiang University (3 entries)
  synbio-competition.png  National Synthetic Biology Innovation Competition
  csbt.webp               Chinese Society for Biotechnology
  siat-synbio.png         Shenzhen Institute of Synthetic Biology
  zju-medicine.png        ZJU School of Medicine
  fubei.jpeg              Forbel
  g60-corridor.jpg        Yangtze Delta G60 corridor joint office

Still without a mark: the provincial SRTP grant.

Prefer a square emblem over a horizontal wordmark — at 24px tall, lettering in a
combination mark is hard to read. Keep filenames ASCII, and make sure the
extension matches the actual format: Hugo picks the decoder by extension.

Project cards also use these: `venueLogo` in a project's front matter puts the
host institution's mark inside its first pill, followed by a `lab` pill.

Lab names as verified:
  WEHI            Call Lab — https://www.wehi.edu.au/laboratory/call-lab/
  Ming Chen       formally "Ming Chen's Group of Bioinformatics"
                  (https://bis.zju.edu.cn/binfo/), shortened to "Chen Lab" so
                  the pill does not crowd the title
  Ruhong Zhou     no public lab name; known through the Institute of
                  Quantitative Biology, so "Zhou Lab"
  Meihua Sui      no public lab name, so "Sui Lab"
