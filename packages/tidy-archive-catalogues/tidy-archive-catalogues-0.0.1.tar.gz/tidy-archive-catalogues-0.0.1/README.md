# The Tidy Archive Catalogues project

The aim of the Tidy Archive Catalogues project is to enable archivist catalogues to be human- and computer-readable. We want to create a python package which will:
 1. enable researchers to analyse and visualise at the level of a catalogue or a subset of the catalogue that they find interesting.
 2. make checking for mistakes in archiving (typos, or non-compliance with archiving standards) easy for archivists, who work quickly and make many subtle decisions.

<!-- TODO: This project grew out of the [Mapping Messel project](link), in which we [visualised](link) Oliver Messel's correspondence from [The Theatre Collection](http://www.bristol.ac.uk/theatre-collection/) at the University of Bristol.-->

# Road-map

The project currently aims to have the following functionality:

1. Enable archivists to search their archives for potential typos/mistakes. Specifically, they will be able to be returned with:
    A. Specific places to check in the archive (e.g. specific reference numbers/codes, and columns)
    for mistakes, particularly for:
        i.  Dates
        ii. Named entities (places, people, and businesses)
    B. Flag inconsistencies in the archive, according to a chosen set of archiving guidelines, for
    example if 'c.', 'c', 'circa' are used to mean approximately, offer one option.
        i. According to national archives guidelines
        ii. According to Theatre Collection guidelines
2. Enable digital humanities researchers to digitally visualise/analyse the collection, by creating
 machine-readable and human-readable (for labels, etc) versions of the following c:
    A. Dates, date ranges, and date uncertainty
    B. Named entities (places, people, and businesses)
 
The output of (2.) should give the data in a useful format to interact with existing python/R libraries. 

For example dates should be in a datetime format, places should be either points in longitude/latitude, or polygonal areas (e.g. in geojson), or easy to convert to. There should be tutorial notebooks, for creating simple visualisations of:
    A. Social networks
    B. Geographical areas
    C. Timelines 
    
Both (1) and (2) should be tested on large archives (e.g. British Library and The National Collection), and smaller ones (e.g. The Theatre Collection, and the Harry Ransom Centre)

# Contributors
<!-- TODO: Fill in contributors part -->
Contributors are recognised using [all-contributors](link) guidelines.

Natalie Thurlby
Julian Warren
Jo Elseworth
Elaine McGirr
Emma Howgill


<!-- TODO: Include info about cataloguing guidelines.
This: https://www.nationalarchives.gov.uk/documents/cat_guide_multi.pdf is the only open UK guidance I’ve seen for creation dates so far, but it’s from 2002, and it’s not too prescriptive (i.e. it suggests that it’s okay to use square brackets, c, or ?, but it doesn’t imply whether there is an order of preference, etc), so it makes sense that people would try different things.
-->
