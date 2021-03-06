# gcode2photon
Use Cura generated gcode in photon ;)
examples:
![example_0](docs/example_0.png?raw=true)

- x=2.9cm y=4.5cm z=7.3cm full fill = 43g
![printer result](docs/result_2.jpg?raw=true)

- x=4.93cm y=7.6cm z=12.41cm = 51g with 5% infill, 70% more than the original and only 8g heavier.
![printer result](docs/result_1.jpg?raw=true)

- If the wall thickness is small, an internal mesh can be seen.
![printer result](docs/result_3.jpg?raw=true)

# dependency
- python 2/3
- python-pil

# install dependency

### GNU/Linux:
```bash
sudo apt install python-pil
```

### Step 1, setup new custom printer with X=68 Y=120 Z=150:
![step1_printer_settings_1.png](docs/step1_printer_settings_1.png?raw=true)

### Step 2, setup layer Z=0.05, wall width=0.047:
![step2_printer_settings_2.png](docs/step2_printer_settings_2.png?raw=true)
### Step 2.1 Slice, you will see something like this, example 1:

![model_1.png](docs/model_1.png?raw=true)
![model_2.png](docs/model_2.png?raw=true)

### Step 3, run gcode2photon, with python
```bash
python ./gcode2images.py my_gcode_file.gcode
```

![step3_run_g2p.png](docs/step3_run_g2p.png?raw=true)

### Step 3.1 if ok, you will see something like this:
![step3_processing.png](docs/step3_processing.png?raw=true)

### Step 3.2 after done, all layers will be files saved to ./layers/layer_xxxxxx.png
![step3_files.png](docs/step3_files.png?raw=true)

### Step 4, You will needed to use [Photon File editor](https://github.com/Photonsters/PhotonFileEditor), create New File
![step4_PhotonFileEditor_1.png](docs/step4_PhotonFileEditor_1.png?raw=true)

### Step 5, In menu select "Import bitmaps"
![step5_PhotonFileEditor_2.png](docs/step5_PhotonFileEditor_2.png?raw=true)

### Step 6, Select the bitmaps directory
![step6_PhotonFileEditor_3.png](docs/step6_PhotonFileEditor_3.png?raw=true)

### Step 7, Enjoy
![step7_PhotonFileEditor_4.png](docs/step7_PhotonFileEditor_4.png?raw=true)
