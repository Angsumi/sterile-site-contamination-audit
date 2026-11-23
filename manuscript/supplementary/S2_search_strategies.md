# Supplementary File S2. Search strategies
Europe PMC REST API (searchPOST) and PubMed E-utilities. Run 22 Nov 2026 and re-run unchanged 23 Nov 2026. Open-access subset: `OPEN_ACCESS:Y AND HAS_FT:Y`; preprints removed.

## Search v1 (broad)

### tumour

PubMed (663 records):

```
(microbiome[tiab] OR microbiota[tiab] OR "16S rRNA"[tiab] OR "16S rDNA"[tiab] OR metagenom*[tiab] OR "bacterial DNA"[tiab] OR "microbial DNA"[tiab]) AND (sequencing[tiab] OR "16S"[tiab] OR metagenom*[tiab]) AND (intratumoral[tiab] OR intratumoural[tiab] OR intratumor[tiab] OR intratumour[tiab] OR "tumor microbiome"[tiab] OR "tumour microbiome"[tiab] OR "tumor microbiota"[tiab] OR "tumour microbiota"[tiab] OR "tumor tissue"[tiab] OR "tumour tissue"[tiab] OR "cancer tissue"[tiab] OR "tumor tissues"[tiab] OR "tumour tissues"[tiab] OR "cancer tissues"[tiab]) NOT (animals[mh] NOT humans[mh]) NOT (review[pt] OR "systematic review"[pt] OR comment[pt] OR editorial[pt]) AND ("2012/01/01"[dp] : "2026/11/22"[dp])
```

Europe PMC open access (764 records):

```
ABSTRACT:("microbiome" OR "microbiota" OR "16S rRNA" OR "16S rDNA" OR "metagenomic" OR "metagenomics" OR "bacterial DNA" OR "microbial DNA") AND ABSTRACT:("intratumoral" OR "intratumoural" OR "intratumor" OR "intratumour" OR "tumor microbiome" OR "tumour microbiome" OR "tumor microbiota" OR "tumour microbiota" OR "tumor tissue" OR "tumour tissue" OR "cancer tissue" OR "tumor tissues" OR "tumour tissues" OR "cancer tissues") NOT PUB_TYPE:"review" AND PUB_YEAR:[2012 TO 2026] AND OPEN_ACCESS:Y AND HAS_FT:Y
```

### placenta_fetal

PubMed (598 records):

```
(microbiome[tiab] OR microbiota[tiab] OR "16S rRNA"[tiab] OR "16S rDNA"[tiab] OR metagenom*[tiab] OR "bacterial DNA"[tiab] OR "microbial DNA"[tiab]) AND (sequencing[tiab] OR "16S"[tiab] OR metagenom*[tiab]) AND (placenta*[tiab] OR "amniotic fluid"[tiab] OR meconium[tiab] OR fetal[tiab] OR foetal[tiab] OR "in utero"[tiab] OR chorioamni*[tiab]) NOT (animals[mh] NOT humans[mh]) NOT (review[pt] OR "systematic review"[pt] OR comment[pt] OR editorial[pt]) AND ("2012/01/01"[dp] : "2026/11/22"[dp])
```

Europe PMC open access (822 records):

```
ABSTRACT:("microbiome" OR "microbiota" OR "16S rRNA" OR "16S rDNA" OR "metagenomic" OR "metagenomics" OR "bacterial DNA" OR "microbial DNA") AND ABSTRACT:(placenta* OR "amniotic fluid" OR "meconium" OR "fetal" OR "foetal" OR "in utero" OR chorioamnionitis) NOT PUB_TYPE:"review" AND PUB_YEAR:[2012 TO 2026] AND OPEN_ACCESS:Y AND HAS_FT:Y
```

### blood

PubMed (274 records):

```
(microbiome[tiab] OR microbiota[tiab] OR "16S rRNA"[tiab] OR "16S rDNA"[tiab] OR metagenom*[tiab] OR "bacterial DNA"[tiab] OR "microbial DNA"[tiab]) AND (sequencing[tiab] OR "16S"[tiab] OR metagenom*[tiab]) AND ("blood microbiome"[tiab] OR "blood microbiota"[tiab] OR "circulating microbiome"[tiab] OR "circulating microbiota"[tiab] OR "blood bacterial DNA"[tiab] OR "plasma microbiome"[tiab] OR "serum microbiome"[tiab] OR "circulating bacterial DNA"[tiab] OR "microbial cell-free DNA"[tiab] OR "blood microbial"[tiab]) NOT (animals[mh] NOT humans[mh]) NOT (review[pt] OR "systematic review"[pt] OR comment[pt] OR editorial[pt]) AND ("2012/01/01"[dp] : "2026/11/22"[dp])
```

Europe PMC open access (231 records):

```
ABSTRACT:("microbiome" OR "microbiota" OR "16S rRNA" OR "16S rDNA" OR "metagenomic" OR "metagenomics" OR "bacterial DNA" OR "microbial DNA") AND ABSTRACT:("blood microbiome" OR "blood microbiota" OR "circulating microbiome" OR "circulating microbiota" OR "blood bacterial DNA" OR "plasma microbiome" OR "serum microbiome" OR "circulating bacterial DNA" OR "microbial cell-free DNA" OR "blood microbial") NOT PUB_TYPE:"review" AND PUB_YEAR:[2012 TO 2026] AND OPEN_ACCESS:Y AND HAS_FT:Y
```

### brain_csf

PubMed (829 records):

```
(microbiome[tiab] OR microbiota[tiab] OR "16S rRNA"[tiab] OR "16S rDNA"[tiab] OR metagenom*[tiab] OR "bacterial DNA"[tiab] OR "microbial DNA"[tiab]) AND (sequencing[tiab] OR "16S"[tiab] OR metagenom*[tiab]) AND ("brain microbiome"[tiab] OR "brain microbiota"[tiab] OR "brain tissue"[tiab] OR "brain tissues"[tiab] OR "post-mortem brain"[tiab] OR "postmortem brain"[tiab] OR "cerebrospinal fluid"[tiab]) NOT (animals[mh] NOT humans[mh]) NOT (review[pt] OR "systematic review"[pt] OR comment[pt] OR editorial[pt]) AND ("2012/01/01"[dp] : "2026/11/22"[dp])
```

Europe PMC open access (778 records):

```
ABSTRACT:("microbiome" OR "microbiota" OR "16S rRNA" OR "16S rDNA" OR "metagenomic" OR "metagenomics" OR "bacterial DNA" OR "microbial DNA") AND ABSTRACT:("brain microbiome" OR "brain microbiota" OR "brain tissue" OR "brain tissues" OR "post-mortem brain" OR "postmortem brain" OR "cerebrospinal fluid") NOT PUB_TYPE:"review" AND PUB_YEAR:[2012 TO 2026] AND OPEN_ACCESS:Y AND HAS_FT:Y
```

### other_sterile

PubMed (815 records):

```
(microbiome[tiab] OR microbiota[tiab] OR "16S rRNA"[tiab] OR "16S rDNA"[tiab] OR metagenom*[tiab] OR "bacterial DNA"[tiab] OR "microbial DNA"[tiab]) AND (sequencing[tiab] OR "16S"[tiab] OR metagenom*[tiab]) AND ("synovial fluid"[tiab] OR "adipose tissue microbio*"[tiab] OR "liver tissue"[tiab] OR "atherosclerotic plaque*"[tiab] OR "heart valve*"[tiab] OR "intraocular"[tiab] OR "vitreous"[tiab] OR "aqueous humor"[tiab] OR "follicular fluid"[tiab] OR "breast tissue"[tiab] OR "lung tissue"[tiab] OR "thrombus"[tiab] OR "kidney tissue"[tiab] OR "tissue microbiome"[tiab] OR "tissue microbiota"[tiab]) NOT (animals[mh] NOT humans[mh]) NOT (review[pt] OR "systematic review"[pt] OR comment[pt] OR editorial[pt]) AND ("2012/01/01"[dp] : "2026/11/22"[dp])
```

Europe PMC open access (880 records):

```
ABSTRACT:("microbiome" OR "microbiota" OR "16S rRNA" OR "16S rDNA" OR "metagenomic" OR "metagenomics" OR "bacterial DNA" OR "microbial DNA") AND ABSTRACT:("synovial fluid" OR "adipose tissue microbiome" OR "adipose tissue microbiota" OR "liver tissue" OR "atherosclerotic plaque" OR "atherosclerotic plaques" OR "heart valve" OR "heart valves" OR "intraocular" OR "vitreous" OR "aqueous humor" OR "follicular fluid" OR "breast tissue" OR "lung tissue" OR "thrombus" OR "kidney tissue" OR "tissue microbiome" OR "tissue microbiota") NOT PUB_TYPE:"review" AND PUB_YEAR:[2012 TO 2026] AND OPEN_ACCESS:Y AND HAS_FT:Y
```

## Search v2 (tight, amendment 0.2)

### tumour

PubMed (580 records):

```
(microbiome[tiab] OR microbiota[tiab] OR "16S rRNA"[tiab] OR "16S rDNA"[tiab] OR "bacterial DNA"[tiab] OR "microbial DNA"[tiab] OR metagenomic[tiab] OR metagenomics[tiab] OR "microbial reads"[tiab]) AND (intratumoral[tiab] OR intratumoural[tiab] OR intratumor[tiab] OR intratumour[tiab] OR "tumor microbiome"[tiab] OR "tumour microbiome"[tiab] OR "tumor microbiota"[tiab] OR "tumour microbiota"[tiab] OR "tumor tissue"[tiab] OR "tumour tissue"[tiab] OR "tumor tissues"[tiab] OR "tumour tissues"[tiab] OR "cancer tissue"[tiab] OR "cancer tissues"[tiab]) NOT (mice[ti] OR mouse[ti] OR murine[ti] OR rat[ti] OR rats[ti] OR porcine[ti] OR pig[ti] OR pigs[ti] OR bovine[ti] OR cattle[ti] OR cow[ti] OR cows[ti] OR calves[ti] OR dog[ti] OR dogs[ti] OR canine[ti] OR cat[ti] OR cats[ti] OR feline[ti] OR horse[ti] OR equine[ti] OR sheep[ti] OR goat[ti] OR goats[ti] OR chicken[ti] OR fish[ti] OR primate[ti] OR macaque[ti]) NOT (meningitis[ti] OR encephalitis[ti] OR sepsis[ti] OR "case report"[ti] OR diagnosis[ti] OR diagnostic[ti] OR "next-generation sequencing"[ti] OR mNGS[ti]) NOT (colorectal[ti] OR colon[ti] OR rectal[ti] OR gastric[ti] OR stomach[ti] OR esophageal[ti] OR oesophageal[ti] OR oral[ti] OR "head and neck"[ti] OR cervical[ti] OR bladder[ti] OR nasopharyngeal[ti] OR laryngeal[ti] OR gut[ti] OR fecal[ti] OR faecal[ti] OR stool[ti] OR intestinal[ti]) NOT (animals[mh] NOT humans[mh]) NOT (review[pt] OR "systematic review"[pt] OR comment[pt] OR editorial[pt] OR "case reports"[pt]) AND ("2012/01/01"[dp] : "2026/11/22"[dp])
```

Europe PMC open access (254 records):

```
ABSTRACT:(microbiome OR microbiota OR "16S rRNA" OR "16S rDNA" OR "bacterial DNA" OR "microbial DNA" OR metagenomic OR metagenomics OR "microbial reads") AND ABSTRACT:(intratumoral OR intratumoural OR intratumor OR intratumour OR "tumor microbiome" OR "tumour microbiome" OR "tumor microbiota" OR "tumour microbiota" OR "tumor tissue" OR "tumour tissue" OR "tumor tissues" OR "tumour tissues" OR "cancer tissue" OR "cancer tissues") AND ABSTRACT:(patients OR participants OR women OR men OR human OR humans OR subjects OR donors OR individuals OR cohort OR pregnancies OR autopsy OR postmortem) NOT TITLE:(mice OR mouse OR murine OR rat OR rats OR porcine OR pig OR pigs OR bovine OR cattle OR cow OR cows OR calves OR dog OR dogs OR canine OR cat OR cats OR feline OR horse OR equine OR sheep OR goat OR goats OR chicken OR fish OR primate OR macaque) NOT TITLE:(meningitis OR encephalitis OR sepsis OR "case report" OR diagnosis OR diagnostic OR "next-generation sequencing" OR mNGS) NOT TITLE:(colorectal OR colon OR rectal OR gastric OR stomach OR esophageal OR oesophageal OR oral OR "head and neck" OR cervical OR bladder OR nasopharyngeal OR laryngeal OR gut OR fecal OR faecal OR stool OR intestinal) NOT PUB_TYPE:"review" AND PUB_YEAR:[2012 TO 2026] AND OPEN_ACCESS:Y AND HAS_FT:Y
```

### placenta_fetal

PubMed (118 records):

```
(microbiome[tiab] OR microbiota[tiab] OR "16S rRNA"[tiab] OR "16S rDNA"[tiab] OR "bacterial DNA"[tiab] OR "microbial DNA"[tiab] OR metagenomic[tiab] OR metagenomics[tiab] OR "microbial reads"[tiab]) AND ("placental microbiome"[tiab] OR "placental microbiota"[tiab] OR "placenta microbiome"[tiab] OR "placenta microbiota"[tiab] OR "amniotic fluid microbiome"[tiab] OR "amniotic fluid microbiota"[tiab] OR "intrauterine colonization"[tiab] OR "in utero colonization"[tiab] OR "fetal microbiome"[tiab] OR "fetal microbiota"[tiab] OR "cord blood microbiome"[tiab] OR "cord blood microbiota"[tiab] OR "placental tissue"[tiab] OR "placental tissues"[tiab] OR "placental samples"[tiab] OR "placental bacteria"[tiab] OR "fetal membranes"[tiab] OR "amniotic fluid samples"[tiab]) NOT (mice[ti] OR mouse[ti] OR murine[ti] OR rat[ti] OR rats[ti] OR porcine[ti] OR pig[ti] OR pigs[ti] OR bovine[ti] OR cattle[ti] OR cow[ti] OR cows[ti] OR calves[ti] OR dog[ti] OR dogs[ti] OR canine[ti] OR cat[ti] OR cats[ti] OR feline[ti] OR horse[ti] OR equine[ti] OR sheep[ti] OR goat[ti] OR goats[ti] OR chicken[ti] OR fish[ti] OR primate[ti] OR macaque[ti]) NOT (meningitis[ti] OR encephalitis[ti] OR sepsis[ti] OR "case report"[ti] OR diagnosis[ti] OR diagnostic[ti] OR "next-generation sequencing"[ti] OR mNGS[ti]) NOT (meconium[ti] OR infant[ti] OR infants[ti] OR neonatal[ti] OR vaginal[ti] OR gut[ti] OR fecal[ti] OR faecal[ti] OR stool[ti]) NOT (animals[mh] NOT humans[mh]) NOT (review[pt] OR "systematic review"[pt] OR comment[pt] OR editorial[pt] OR "case reports"[pt]) AND ("2012/01/01"[dp] : "2026/11/22"[dp])
```

Europe PMC open access (63 records):

```
ABSTRACT:(microbiome OR microbiota OR "16S rRNA" OR "16S rDNA" OR "bacterial DNA" OR "microbial DNA" OR metagenomic OR metagenomics OR "microbial reads") AND ABSTRACT:("placental microbiome" OR "placental microbiota" OR "placenta microbiome" OR "placenta microbiota" OR "amniotic fluid microbiome" OR "amniotic fluid microbiota" OR "intrauterine colonization" OR "in utero colonization" OR "fetal microbiome" OR "fetal microbiota" OR "cord blood microbiome" OR "cord blood microbiota" OR "placental tissue" OR "placental tissues" OR "placental samples" OR "placental bacteria" OR "fetal membranes" OR "amniotic fluid samples") AND ABSTRACT:(patients OR participants OR women OR men OR human OR humans OR subjects OR donors OR individuals OR cohort OR pregnancies OR autopsy OR postmortem) NOT TITLE:(mice OR mouse OR murine OR rat OR rats OR porcine OR pig OR pigs OR bovine OR cattle OR cow OR cows OR calves OR dog OR dogs OR canine OR cat OR cats OR feline OR horse OR equine OR sheep OR goat OR goats OR chicken OR fish OR primate OR macaque) NOT TITLE:(meningitis OR encephalitis OR sepsis OR "case report" OR diagnosis OR diagnostic OR "next-generation sequencing" OR mNGS) NOT TITLE:(meconium OR infant OR infants OR neonatal OR vaginal OR gut OR fecal OR faecal OR stool) NOT PUB_TYPE:"review" AND PUB_YEAR:[2012 TO 2026] AND OPEN_ACCESS:Y AND HAS_FT:Y
```

### blood

PubMed (279 records):

```
(microbiome[tiab] OR microbiota[tiab] OR "16S rRNA"[tiab] OR "16S rDNA"[tiab] OR "bacterial DNA"[tiab] OR "microbial DNA"[tiab] OR metagenomic[tiab] OR metagenomics[tiab] OR "microbial reads"[tiab]) AND ("blood microbiome"[tiab] OR "blood microbiota"[tiab] OR "circulating microbiome"[tiab] OR "circulating microbiota"[tiab] OR "blood bacterial DNA"[tiab] OR "plasma microbiome"[tiab] OR "serum microbiome"[tiab] OR "circulating bacterial DNA"[tiab] OR "microbial cell-free DNA"[tiab] OR "blood microbial"[tiab]) NOT (mice[ti] OR mouse[ti] OR murine[ti] OR rat[ti] OR rats[ti] OR porcine[ti] OR pig[ti] OR pigs[ti] OR bovine[ti] OR cattle[ti] OR cow[ti] OR cows[ti] OR calves[ti] OR dog[ti] OR dogs[ti] OR canine[ti] OR cat[ti] OR cats[ti] OR feline[ti] OR horse[ti] OR equine[ti] OR sheep[ti] OR goat[ti] OR goats[ti] OR chicken[ti] OR fish[ti] OR primate[ti] OR macaque[ti]) NOT (meningitis[ti] OR encephalitis[ti] OR sepsis[ti] OR "case report"[ti] OR diagnosis[ti] OR diagnostic[ti] OR "next-generation sequencing"[ti] OR mNGS[ti]) NOT (animals[mh] NOT humans[mh]) NOT (review[pt] OR "systematic review"[pt] OR comment[pt] OR editorial[pt] OR "case reports"[pt]) AND ("2012/01/01"[dp] : "2026/11/22"[dp])
```

Europe PMC open access (159 records):

```
ABSTRACT:(microbiome OR microbiota OR "16S rRNA" OR "16S rDNA" OR "bacterial DNA" OR "microbial DNA" OR metagenomic OR metagenomics OR "microbial reads") AND ABSTRACT:("blood microbiome" OR "blood microbiota" OR "circulating microbiome" OR "circulating microbiota" OR "blood bacterial DNA" OR "plasma microbiome" OR "serum microbiome" OR "circulating bacterial DNA" OR "microbial cell-free DNA" OR "blood microbial") AND ABSTRACT:(patients OR participants OR women OR men OR human OR humans OR subjects OR donors OR individuals OR cohort OR pregnancies OR autopsy OR postmortem) NOT TITLE:(mice OR mouse OR murine OR rat OR rats OR porcine OR pig OR pigs OR bovine OR cattle OR cow OR cows OR calves OR dog OR dogs OR canine OR cat OR cats OR feline OR horse OR equine OR sheep OR goat OR goats OR chicken OR fish OR primate OR macaque) NOT TITLE:(meningitis OR encephalitis OR sepsis OR "case report" OR diagnosis OR diagnostic OR "next-generation sequencing" OR mNGS) NOT PUB_TYPE:"review" AND PUB_YEAR:[2012 TO 2026] AND OPEN_ACCESS:Y AND HAS_FT:Y
```

### brain_csf

PubMed (72 records):

```
(microbiome[tiab] OR microbiota[tiab] OR "16S rRNA"[tiab] OR "16S rDNA"[tiab] OR "bacterial DNA"[tiab] OR "microbial DNA"[tiab]) AND ("brain microbiome"[tiab] OR "brain microbiota"[tiab] OR "brain tissue"[tiab] OR "brain tissues"[tiab] OR "postmortem brain"[tiab] OR "post-mortem brain"[tiab] OR "cerebrospinal fluid microbiome"[tiab] OR "cerebrospinal fluid microbiota"[tiab] OR "CSF microbiome"[tiab] OR "CSF microbiota"[tiab]) NOT (mice[ti] OR mouse[ti] OR murine[ti] OR rat[ti] OR rats[ti] OR porcine[ti] OR pig[ti] OR pigs[ti] OR bovine[ti] OR cattle[ti] OR cow[ti] OR cows[ti] OR calves[ti] OR dog[ti] OR dogs[ti] OR canine[ti] OR cat[ti] OR cats[ti] OR feline[ti] OR horse[ti] OR equine[ti] OR sheep[ti] OR goat[ti] OR goats[ti] OR chicken[ti] OR fish[ti] OR primate[ti] OR macaque[ti]) NOT (meningitis[ti] OR encephalitis[ti] OR sepsis[ti] OR "case report"[ti] OR diagnosis[ti] OR diagnostic[ti] OR "next-generation sequencing"[ti] OR mNGS[ti]) NOT (gut[ti] OR fecal[ti] OR faecal[ti] OR stool[ti] OR intestinal[ti] OR "gut-brain"[ti]) NOT (animals[mh] NOT humans[mh]) NOT (review[pt] OR "systematic review"[pt] OR comment[pt] OR editorial[pt] OR "case reports"[pt]) AND ("2012/01/01"[dp] : "2026/11/22"[dp])
```

Europe PMC open access (41 records):

```
ABSTRACT:(microbiome OR microbiota OR "16S rRNA" OR "16S rDNA" OR "bacterial DNA" OR "microbial DNA") AND ABSTRACT:("brain microbiome" OR "brain microbiota" OR "brain tissue" OR "brain tissues" OR "postmortem brain" OR "post-mortem brain" OR "cerebrospinal fluid microbiome" OR "cerebrospinal fluid microbiota" OR "CSF microbiome" OR "CSF microbiota") AND ABSTRACT:(patients OR participants OR women OR men OR human OR humans OR subjects OR donors OR individuals OR cohort OR pregnancies OR autopsy OR postmortem) NOT TITLE:(mice OR mouse OR murine OR rat OR rats OR porcine OR pig OR pigs OR bovine OR cattle OR cow OR cows OR calves OR dog OR dogs OR canine OR cat OR cats OR feline OR horse OR equine OR sheep OR goat OR goats OR chicken OR fish OR primate OR macaque) NOT TITLE:(meningitis OR encephalitis OR sepsis OR "case report" OR diagnosis OR diagnostic OR "next-generation sequencing" OR mNGS) NOT TITLE:(gut OR fecal OR faecal OR stool OR intestinal OR "gut-brain") NOT PUB_TYPE:"review" AND PUB_YEAR:[2012 TO 2026] AND OPEN_ACCESS:Y AND HAS_FT:Y
```

### other_sterile

PubMed (714 records):

```
(microbiome[tiab] OR microbiota[tiab] OR "16S rRNA"[tiab] OR "16S rDNA"[tiab] OR "bacterial DNA"[tiab] OR "microbial DNA"[tiab]) AND ("synovial fluid"[tiab] OR "adipose tissue"[tiab] OR "liver tissue"[tiab] OR "atherosclerotic plaque"[tiab] OR "atherosclerotic plaques"[tiab] OR "heart valve"[tiab] OR "heart valves"[tiab] OR intraocular[tiab] OR vitreous[tiab] OR "aqueous humor"[tiab] OR "follicular fluid"[tiab] OR "breast tissue"[tiab] OR "lung tissue"[tiab] OR thrombus[tiab] OR thrombi[tiab] OR "kidney tissue"[tiab] OR "tissue microbiome"[tiab] OR "tissue microbiota"[tiab] OR "endometrial tissue"[tiab]) NOT (mice[ti] OR mouse[ti] OR murine[ti] OR rat[ti] OR rats[ti] OR porcine[ti] OR pig[ti] OR pigs[ti] OR bovine[ti] OR cattle[ti] OR cow[ti] OR cows[ti] OR calves[ti] OR dog[ti] OR dogs[ti] OR canine[ti] OR cat[ti] OR cats[ti] OR feline[ti] OR horse[ti] OR equine[ti] OR sheep[ti] OR goat[ti] OR goats[ti] OR chicken[ti] OR fish[ti] OR primate[ti] OR macaque[ti]) NOT (meningitis[ti] OR encephalitis[ti] OR sepsis[ti] OR "case report"[ti] OR diagnosis[ti] OR diagnostic[ti] OR "next-generation sequencing"[ti] OR mNGS[ti]) NOT (gut[ti] OR fecal[ti] OR faecal[ti] OR stool[ti] OR intestinal[ti] OR oral[ti] OR vaginal[ti] OR cervical[ti] OR colorectal[ti] OR colon[ti] OR gastric[ti]) NOT (animals[mh] NOT humans[mh]) NOT (review[pt] OR "systematic review"[pt] OR comment[pt] OR editorial[pt] OR "case reports"[pt]) AND ("2012/01/01"[dp] : "2026/11/22"[dp])
```

Europe PMC open access (306 records):

```
ABSTRACT:(microbiome OR microbiota OR "16S rRNA" OR "16S rDNA" OR "bacterial DNA" OR "microbial DNA") AND ABSTRACT:("synovial fluid" OR "adipose tissue" OR "liver tissue" OR "atherosclerotic plaque" OR "atherosclerotic plaques" OR "heart valve" OR "heart valves" OR intraocular OR vitreous OR "aqueous humor" OR "follicular fluid" OR "breast tissue" OR "lung tissue" OR thrombus OR thrombi OR "kidney tissue" OR "tissue microbiome" OR "tissue microbiota" OR "endometrial tissue") AND ABSTRACT:(patients OR participants OR women OR men OR human OR humans OR subjects OR donors OR individuals OR cohort OR pregnancies OR autopsy OR postmortem) NOT TITLE:(mice OR mouse OR murine OR rat OR rats OR porcine OR pig OR pigs OR bovine OR cattle OR cow OR cows OR calves OR dog OR dogs OR canine OR cat OR cats OR feline OR horse OR equine OR sheep OR goat OR goats OR chicken OR fish OR primate OR macaque) NOT TITLE:(meningitis OR encephalitis OR sepsis OR "case report" OR diagnosis OR diagnostic OR "next-generation sequencing" OR mNGS) NOT TITLE:(gut OR fecal OR faecal OR stool OR intestinal OR oral OR vaginal OR cervical OR colorectal OR colon OR gastric) NOT PUB_TYPE:"review" AND PUB_YEAR:[2012 TO 2026] AND OPEN_ACCESS:Y AND HAS_FT:Y
```
