# Introduction

The __watermarker__ script provides a convenient way to __watermark__ more than one image. It was created to make easier to watermark images, because it can take a lot of time
if you have more than one image.

# Installation
## Use out of the box
You can use this script without installing it. You can run __binary file__ (.exe) or __source file__ (.py).

### Binary file
1. Download `watermarker.exe` and save it anywhere you like. 
2. Run it with :
	```
	watermarker.exe <arguments>
	```
### Source file
1. Install __python__
2. Install __python dependencies__ with
	```
	pip install pillow
	```
3. Download __repository__ and save it anywhere you like.
4. Run script with:
	```
	python watermarker.py <arguments>
	```
## Generate binary from source
1. Follow above steps for _source code_.
2. Install python installer with [instructions](https://pyinstaller.readthedocs.io/en/v3.3.1/installation.html).
3. Run `generate.bat` to create binary file, which will be saved to _dist_ folder.

## Install on your device
1. Create folder __Watermarker__ in __Program Files__. 
2. Download `watermarker.exe` and save it to ___Watermarker___ folder.
3. Add location of __Watermarker folder__ to __PATH__ variable.

# Examples
Here are some examples that will help you start. Note that there are different way to call _watermarker_ script, examples use `watermarker.exe`.

## Arguments


## Print version
```
watermarker --version
```

## Get help
```
watermarker --help
```

## Watermark image with image (basic example - choose corner)
```
watermarker --input=input_image.jpg --output=output_image.jpg --wimage watermark_image.png --wpos=LD --wposm 10
```

## Watermark image with image (extended example - choose position)

## Watermark image with text (basic example)

## Watermark image with text (extended example)
