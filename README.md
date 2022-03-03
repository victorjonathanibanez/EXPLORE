# EXPLORE: A novel deep learning-based analysis method for exploration learning in object recognition tests

GIFs will come here!

## _About:_
Object recognition tests are among the most widely used behavioral tests in neuroscience to assess memory function in rodents. Despite the simplicity of the experimental implementation of the task, there is a broad range of interpretation which behavioral features are counted as object exploration. Thus, traditionally the analysis of object exploration is often scored manually, which is  time-consuming, limited to few behaviors, and variable across researchers. We developed EXLORE: a simple, ready-to use, open source pipeline to perform the different analysis steps for object recognition tests with a higher versatility and precision and lower investment of time than expensive commercial software. EXPLORE consists of two parts: 1) An algorithm that calculates mean pixel intensities of the four quadrants of the experimental arena, useful for preliminary tests detecting patterns of roaming behavior with spatial preference. 2) A convolutional neural network trained in a supervised manner, that extracts features from images and classifies features into ?exploration? at a given object or ?no exploration? elsewhere. EXPLORE achieves human accuracy in identifying and scoring exploration behavior and outperforms commercial software, in particular under complex conditions (e.g. multiple objects and larger objects to climb on). Users can decide by themselves, which behavior is in- or excluded from scoring exploration behavior by labeling the respective training data set. A GUI provides a beginning-to-end analysis with an automatic stop-watch function for exploration behavior and calculation of typical outcome parameters, accelerating a fast and reproducible data analysis for neuroscientists with no expertise in programming or deep learning.

## _Install EXPLORE:_

- First install Anaconda (if not installed already): [Install now](https://docs.anaconda.com/anaconda/install/index.html)
- Clone this repository and store the folder *EXPLORE-main* at a preferred directory (first, you find it in your *download* folder)
- Open a shell- or a terminal window and change the directory (the easiest way is to drag & drop your folder into the shell- or terminal window after typing *cd* and a space):
```sh
cd <your directory>/EXPLORE-main
```
- create and activate your environment:
```sh
conda create -n XPL
conda activate XPL
```
- Run the *requirements.txt* file (this will install all the necessary packages for EXPLORE into your new conda environment):
```sh
conda install -c conda-forge --file requirements.txt
```
- install OpenCV with the following command on **macOS**:
```sh
pip install opencv-python==4.1.1.26
```
(use **pip3** for macOS earlier than *BigSur*)

- or install OpenCV with the following command on **Windows**:

```sh
conda install -c conda-forge opencv==4.5.0
```

\
&nbsp;

:fire: **Congratulations, you have now successfully installed EXPLORE! Now let's use it...** :fire:
  
\
&nbsp;

## _How to use EXPLOREs quadrant analysis:_
With the quadrant analysis you can investigate and quantify movement throughout the experiment arena. Two measures are taken: the time animals spent in each quadrant over a given period (*exploration time*) and the frequency of transistions from one quadrant to another (*exploration frequency*).

Open a shell- or a terminal window and change to your directory:
```sh
cd <your directory>/EXPLORE-main/scripts
```

Activate your virtual environment:
```sh
conda activate XPL
```

Then enter the following command:
```sh
python main_quadrant.py
```
(**python3** for macOS)

**:arrow_right: This will now open a GUI (see [manual quadrant](https://github.com/victorjonathanibanez/EXPLORE/blob/main/manuals/Manual_quadrant.jpeg) for further instructions!)** 

\
&nbsp;

| Output files | Type | Description | 
| ------ | ------ | ------ |
| Dataframe | .csv | The predicted exploration times and frequencies for each quadrant will be stored in a dataframe |
| Plots | .png | For each animal (video) the frequency will be plotted and stored |
| Heatmap | .png | An overview on the quadrants exploration- frequency and time will be plotted as heatmaps |

\
&nbsp;
  
## _How to use EXPLOREs deep learning-based exploration analysis:_
EXPLOREs deep learning-based exploration analysis is the major part to investigate object recognition tests. There are three parts: 1. Training a network on a few manually scored samples. 2. Predict on the all of your experiment videos. 3. Correct your prediction if necessary. The main measures taken are *exploration time* and *exploration frequency* on each defined object. For acquisition session and testing session two distinct networks have to be trained.

Open a shell- or a terminal window and change to your directory:
```sh
cd <your directory>/EXPLORE-main/scripts
```

Activate your virtual environment:
```sh
conda activate XPL
```

### Training:
  
To train a network enter the following command:
```sh
python main_training.py
```
(**python3** for mac)

**:arrow_right: This will now open a GUI (see [manual training1](https://github.com/victorjonathanibanez/EXPLORE/blob/main/manuals/Manual_training.jpeg) and [manual training2](https://github.com/victorjonathanibanez/EXPLORE/blob/main/manuals/Manual_training2.jpeg) and [manual scoring](https://github.com/victorjonathanibanez/EXPLORE/blob/main/manuals/Manual_scoring.jpeg) for further instructions!)** 
  
\
&nbsp;

### Prediction:
  
To predict on your experiment videos enter the following command:
```sh
python main_prediction.py
```
(**python3** for mac)
  
**:arrow_right: This will now open a GUI (see [manual prediction](https://github.com/victorjonathanibanez/EXPLORE/blob/main/manuals/Manual_prediction.jpeg) for further instructions!)** 

\
&nbsp;

### Correction:
  
To correct your prediction enter the following command:
```sh
python main_correct.py
```
(**python3** for mac)

**:arrow_right: This will now open a GUI (see [manual correction](https://github.com/victorjonathanibanez/EXPLORE/blob/main/manuals/Manual_correction.jpeg) for further instructions!)** 

\
&nbsp;

| Output files | Type | Description | 
| ------ | ------ | ------ |
| Prediction videos | folder | For all of the selected experiment videos EXPLORE will generate colored squares around the objects whenever *exploration* was predicted and store the newly created videos in the folder |
| Dataframe | .csv | The predicted exploration times and frequencies at each object will be stored in a dataframe |
| Plots | .png | Training- and validation accuracy- and loss will be plotted and saved |
  
\
&nbsp;

## _How to use EXPLOREs manual labeling tool:_
Besides the automated analysis, EXPLORE provides a tool for manual scoring. The scoring will be saved as .csv file.

Open a shell- or a terminal window and change to your directory:
```sh
cd <your directory>/EXPLORE-main/scripts
```

Activate your virtual environment:
```sh
conda activate XPL
```

To start manual scoring type the following command:
```sh
python main_manual_scoring.py
```
(**python3** for mac)

**:arrow_right: This will now open a GUI (refer to the training manual for further instructions!)** 
  
\
&nbsp;

> **Please refer to our publication for further information about more technical details:**

\
&nbsp;

## _Contact:_
victor.ibanez@uzh.ch\
wahl@hifo.uzh.ch
