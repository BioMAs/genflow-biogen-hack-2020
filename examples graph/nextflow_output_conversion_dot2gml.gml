graph [
  version 2
  directed 1
  node [
    id 0
    name "p0"
    fixedsize "true"
    xlabel "Channel.fromPath"
    graphics [
      w 7.2
      type "point"
    ]
  ]
  node [
    id 1
    name "p1"
    fixedsize "true"
    xlabel "view"
    graphics [
      w 7.2
      type "circle"
    ]
  ]
  node [
    id 2
    name "p2"
    fixedsize "true"
    xlabel "ifEmpty"
    graphics [
      w 7.2
      type "circle"
    ]
  ]
  node [
    id 3
    name "p3"
    fixedsize ""
    label "fastqc"
    xlabel ""
    LabelGraphics [
      text "fastqc"
    ]
  ]
  node [
    id 4
    name "p4"
    fixedsize "true"
    xlabel "collect"
    graphics [
      w 7.2
      type "circle"
    ]
  ]
  node [
    id 5
    name "p5"
    fixedsize ""
    label "multiqc"
    xlabel ""
    LabelGraphics [
      text "multiqc"
    ]
  ]
  node [
    id 6
    name "p7"
    fixedsize ""
    xlabel ""
    graphics [
      type "point"
    ]
  ]
  node [
    id 7
    name "p6"
    fixedsize ""
    xlabel ""
    graphics [
      type "point"
    ]
  ]
  edge [
    id 1
    source 0
    target 1
  ]
  edge [
    id 2
    source 1
    target 2
  ]
  edge [
    id 3
    source 2
    target 3
    label "myreads"
    LabelGraphics [
      text "myreads"
    ]
  ]
  edge [
    id 4
    source 3
    target 4
    label "fastqc_zip"
    LabelGraphics [
      text "fastqc_zip"
    ]
  ]
  edge [
    id 5
    source 4
    target 5
  ]
  edge [
    id 6
    source 5
    target 6
    label "multiqc_res"
    LabelGraphics [
      text "multiqc_res"
    ]
  ]
  edge [
    id 7
    source 5
    target 7
    label "multiqc_log"
    LabelGraphics [
      text "multiqc_log"
    ]
  ]
]
