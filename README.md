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
|__Argument__|__Description__|
|:----------:|:--------------|
|-h,--help|Prints help|
|-V,--version|Prints version|
|-v,--verbose|Enables verbose mode|
|-i `<path>`,--input=`<path>`|Path of input file or directory|
|-o `<path>`,--output=`<path>`|Path of output file or directory, if input is file, then output also must be file, same for directory|
|-O,--overwrite|Automaticly overwrite existing files|
|--width=`<new width>`|Resize image to new width|
|--height=`<new height>`|Resize image to new height|
|--preview|Show image before saving|
|--ask-to-save|Ask if we want image to be saved|
|--wpos=`<corner>`|Set corner where watermark will be, available corners LU - LeftUpperCorner,L - LeftCorner, LD - LeftDownCorner,RU - RightUpperCorner,R - RightCorner,RD - RightDownCorner, U - UpperCorner,D - DownCorner|
|--wposm=`<margin_px>`|Set margin from border for logo in px, use with `--wpos`|
|--wposx=`<x_coord_px>`|X coordinate of watermark position|
|--wposy=`<y_coord_px>`|Y coordinate of watermark position|
|--wimage=`<image_path>`|Path to watermark image|
|--wwidth=`<new width>`|Resize watermark to new width|
|--wheight=`<new height>`|Resize watermark to new height|
|--wtext=`<watermark text>`|Watermark text|
|--wcolor=`<text color>`|Text color, valid formats are `#rrggbb`,`rgb(r,g,b)`,`#rgb`,`hsl(hue,saturation%,lightness%)`,`color_name`|
|--wfont=`<path_to_ttf>`|Path to font file|
|--wfsize=`<font size pt>`|Text font size|

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
