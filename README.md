# Project MIPS-Anisotropy
Mo Shams <MShamsCBR.gmail.com>  
Jan 03, 2023    

To investigate the anisotropic nature of the midlocalization of a flashed
probe in the vicinity of a moving object.

---

### Overview
First, I will see how the spatial profile of the mislocalization looks like 
and whether only the position of objects are miscalculated or also thier 
shape deforms.

Next, I will investigate how low-level features:
- size
- speed
- contrast/luminance

as well as higher-level features:
- predictability
- memory load
- physical reasoning

influence the magnitude and spatial profile of the effect.

---

### Required Packages
- Python 3.8.13
- Psychopy 2022.1.4

---

### Directory Organization
```
MIPS-Anisotropy
|   .gitignore
|   figures.ai
|   figXX.eps
|   figXX.script
|   README.md
|__ analysis
|       aXXX_[name].py
|__ data
|   |   aXXX_[name].json
|   \__ rawData
|           *.json
|           recording notes.txt   
|__ docs
|       *.[text format]
|__ lib
|       *.py
|__ results
|       *.pdf
|       *.key
\__ stimulus
        expXX_[name].py
        test_[name].py
```
---

### Pipeline
            