# ghcnm_search

## Description

Function to read the Global Historical Climatology Network monthly (GHCNm) temperature dataset, selection data by station code or a rectangular geographic area.

## Install ghcnm_search

```
git clone https://github.com/cduranalarcon/ghcnm_search
```

## Usage (python3)

###  Search stations by --area

```
python ghcnm_search.py  -d path/to/ghcnm.tavg.vn.y.z.YYYMMDD.qcu.dat -m path/to/ghcnm.tavg.vn.y.z.YYYMMDD.qcu.inv -o output/path/ -a minlat minlon maxlat maxlon` 
```
###  Search stations by --code

```
$python ghcnm_search.py  -d path/to/ghcnm.tavg.vn.y.z.YYYMMDD.qcu.dat -m path/to/ghcnm.tavg.vn.y.z.YYYMMDD.qcu.inv -o output/path/ -c code-1 code-2 ... code-N
```
## Example

### Input

```
$python3 ghcnm_search.py -d ../../Datasets/global-data/ghcnm.tavg.v4.0.1.20210818.qcu.dat -m ../..
/Datasets/global-data/ghcnm.tavg.v4.0.1.20210818.qcu.inv -o ../../Datasets/GHCNM/ -a -90 -180 -60 180
```

### Output
```
###############################################################

97 stations were found.

           code elevation  latitude                         name
0   AYM00088963      24.0  -63.4000               BASE_ESPERANZA
1   AYM00088968       8.0  -60.7330                 BASE_ORCADAS
2   AYM00089001      62.0  -70.3000               SANAE_SAF_BASE
..          ...       ...       ...                          ...
94  AYXLT885346      10.0  -63.3000                    O_HIGGINS
95  AYXLT975160      40.0  -75.4200                      LIMBERT
96  XXXLT848602    9999.0  -67.1700          ISLA_DE_PASCUA_EAST

[97 rows x 4 columns]

Output files were saved in  '/mnt/c/Users/human/Datasets/GHCNM'

###############################################################
```
## help

```
$python3 ghcnm_search.py -h
```
```
usage: ghcnm_search.py [-h] -d DATA_PATH -m METADATA_PATH [-o OUTPUT_PATH]
                       [-s STATIONS_LIST] [-c CODES [CODES ...]]
                       [-a AREA [AREA ...]]

Tool to select and read ghcnm datasets by area OR station code

optional arguments:
  -h, --help            show this help message and exit
  -d DATA_PATH, --data_path DATA_PATH
                        Filepath to ghcnm data
                        (ghcnm.tavg.vn.y.z.YYYMMDD.qcu.dat)
  -m METADATA_PATH, --metadata_path METADATA_PATH
                        Filepath to ghcnm metadata
                        (ghcnm.tavg.vn.y.z.YYYMMDD.qcu.inv)
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Output filepath
  -s STATIONS_LIST, --stations_list STATIONS_LIST
                        Name of the stations selected by area or a list of
                        station code
  -c CODES [CODES ...], --codes CODES [CODES ...]
                        List of station codes within the ghcnm dataset [code1
                        code2 code3 code4 ...]. When --codes is provides,
                        --area is not used.
  -a AREA [AREA ...], --area AREA [AREA ...]
                        Geographic coordinates of the opposite vertices of a
                        rectangle [minlat minlon maxlat maxlon]
```
