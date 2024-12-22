This is the repository of the paper _"“We provide our resources in a dedicated repository”: Surveying the Transparency of HICSS publications"_, accepted to the 58th Hawaii International Conference on System Sciences ([HICSS'58](https://hicss.hawaii.edu/)).

If you use any of our resources, you are kindly invited to cite our paper:

```
@inproceedings{pekaric2025weprovide,
    title={{"We provide our resources in a dedicated repository": Surveying the Transparency of HICSS publications}},
    author={Pekaric, Irdin and Apruzzese, Giovanni},
    booktitle={Proc. Hawaii International Conference on System Sciences (HICSS)},
    year={2025}
}
```

# Description

The repository contains two folders: ``CODE`` which contains the original source code we developed for our research; and ``TABLES`` which contains the results of our findings.

Specifically, the ``CODE`` folder contains the following files:

* ``hicss_scraper.py`` which contains the code of the scraper we used to collect the HICSS publications (2017-2024)
* ``user_study_pdfs.py`` which contains code whose goal is identifying publications that are (likely) user studies (by means of keyword search)
* ``technical_pdfs.py`` which contains code whose goal is identifying publications that are (likely) technical papers (by means of keyword search)
* ``user_study_repo.py`` which contains code whose goal is  identifying publications that are (i) user studies and which (ii) likely contain a link to an external repository
* ``technical_repo.py`` which contains code whose goal is  identifying publications that are (i) technical papers and which (ii) likely contain a link to an external repository

With regards to the ``TABLES`` folder, it contains the following files:

* ``technical_papers.pdf``, which is a list of papers that have been deemed to be "technical papers"
* ``user_papers.pdf`` which is a list of papers that have been deemed to be "user studies"
* ``both.pdf`` which is a list of papers that have been deemed to include both elements of "user studies" and of "technical papers"
* ``user_repo.pdf`` which is the list of _user studies_ that have a link to an external repository
* ``technical_repo.pdf`` which is the list of _technical papers_ that have a link to an external repository

Some tables may also report additional information on each paper.

### Contact

If you have any inquiry about our research (e.g., about the tables or source code) feel free to contact the first author, Dr. [Irdin Pekaric](https://www.irdinpekaric.com/) (irdin.pekaric@uni.li)



