# PYNQ Compute Lab Material

This package contains the notebooks for the PYNQ portion of the Xilinx Vitis tutorials.

## Installing the Runtime

*If you are working through the labs as part of larger AWS workshop you will already have done this step and can move on to the "Installing Anaconda" step.*

On Nimbix the Xilinx runtime will already have been installed

for other Alveo installs you will need to source the XRT setup script:

```
# Alveo systems only
source /opt/xilinx/xrt/setup.sh
```

For F1 you will need to download and source the vitis runtime script

```
# Amazon AWS F1 system only
git clone https://github.com/aws/aws-fpga.git
source aws-fpga/vitis_runtime_setup.sh
```

## Installing Anaconda

We recommend using PYNQ and Jupyterlab in an Anaconda environment. Open a terminal and run the following commands:

```
wget https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh
bash Anaconda3-2019.07-Linux-x86_64.sh -b
source ~/anaconda3/bin/activate
```

## Installing PYNQ and the Lab Material

With the Anaconda environment initialized, PYNQ and the lab material can be installed using `pip` and the `pynq get-notebooks` command.

```
pip install pynq
pip install pynq-compute-labs
pynq get-notebooks
```

Finally change into the newly created directory and launch JupyterLab

```
cd pynq-notebooks
jupyter lab
```

This will bring up a Jupyter Lab environment you can use to complete the lab.

## Companion Videos

The introductory presentation to the lab material is availble [on YouTube](https://www.youtube.com/watch?v=WgA_FgO_rAo&list=PLun96h10Q07GydOx16q5735arA67_ZI75&index=1)

In addition, as labs can only show so much of PYNQ, we've created three short companion videos that cover topics that aren't addressed here. We recommending watching them in order, one after each notebook.

 1. [Using Multiple Devices](https://youtu.be/tk2XDW-Hpco)
 2. [Hardware Emulation](https://youtu.be/ylVEo0d83iM)
 3. [Packaging Your Designs](https://youtu.be/S2oSliWHpsA)


