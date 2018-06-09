#
# Watermarker - program for watermarking images
#

PROG_VERSION = '1.1'

IMG_ALLOWED_EXT = ['jpg','png'] # Supported image extentions
IMG_TXT_DEFAULT_COLOR = 'black' # Default color for text
IMG_TXT_DEFAULT_FONT = 'fonts/Roboto-Regular.ttf' # Default text font
IMG_TXT_DEFAULT_SIZE = 70 # Default text size

# Import dependencies
import argparse
import sys
import os
import shutil
from enum import Enum
from pprint import pprint

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('Pillow library is missing. Please install it.')

# Global definitons
class RelativePosition(Enum):
    LEFTUPPER_CORNER = 'LU'
    LEFT_CORNER = 'L'
    LEFTDOWN_CORNER = 'LD'
    RIGHTUPPER_CORNER = 'RU'
    RIGHT_CORNER = 'R'
    RIGHTDOWN_CORNER = 'RD'
    UPPER_CORNER = 'U'
    DOWN_CORNER = 'D'

# Functions
def stack_trace(obj):
    pprint(vars(obj))
def aquire_args():
    global args

    # Print and parse available options for program
    parser = argparse.ArgumentParser(description='Program for watermarking images')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s '+PROG_VERSION, help='Prints version of program.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enables verbose mode.')
    parser.add_argument('-i', '--input', type=str, help='Sets path for input file or directory.')
    parser.add_argument('-o', '--output', type=str, help='Sets path for output file or directory.')
    #parser.add_argument('-r', '--recursive', action='store_true', help='Enables recursive mode for directory.')
    parser.add_argument('-O', '--overwrite', action='store_true', help='Overwrites exsisting files / dirs.')
    #parser.add_argument('-l','--log-file', help='Sets path for log file.')

    # Image option
    parser.add_argument('--width',type=int,help='Resize the width of the image to <width>.')
    parser.add_argument('--height', type=int, help='Resize the height of the image to <height>.')
    parser.add_argument('--preview',action='store_true', help='Display image before saving.')
    parser.add_argument('--ask-to-save',action='store_true', help='Ask if you want to save file.')
    
    # Watermark options
    parser.add_argument('--wpos', type=str, choices=['LU','L','LD','RU','R','RD','U','D'], help='Corner where watermark will be shown (L - left,R - right,U - up,D - down)')
    parser.add_argument('--wposm', type=int, help='Sets watermark margin to <wposm>. Only with --wpos option.')
    
    parser.add_argument('--wposx', type=int, help='Sets watermark X pos to <wposx>.')
    parser.add_argument('--wposy', type=int, help='Sets watermark Y pos to <wposy>.')
    #parser.add_argument('--wopacity', type=float, help='Sets watermark opacity to <wopacity>. Valid values are between 0 and 1.')

    parser.add_argument('--wimage', type=str, help='Sets path to watermark image <wimage>')
    parser.add_argument('--wwidth', type=int, help='Resize the width of the watermark image to <width>.')
    parser.add_argument('--wheight', type=int, help='Resize the height of the watermark image to <height>.')

    parser.add_argument('--wtext', type=str, help='Sets watermark text to <wtext>')
    parser.add_argument('--wcolor', type=str, help='Sets watermark text color to <wcolor>. Valid formats are #rrggbb, rgb(r,g,b), #rgb, hsl(hue,saturation%%,lightness%%),name.')
    parser.add_argument('--wfont', help='Path to ttf file for the text watermark to <file path>.')
    #parser.add_argument('--wfstyle', choices=['bold', 'italic', 'underline', 'regular'], help="Sets the font style of the text watermark to <font style>. Valid options are: bold, italic, underline, regular.")
    parser.add_argument('--wfsize', type=int, help="Sets the font size of the text watermark to <font size>.")

    args = parser.parse_args()
def check_args(): # Check if arguments are valid
    # Check arg: Input (required)
    if args.input is None:
        raise Exception(2,"No input specified.")
    elif not os.path.exists(args.input) or (not os.path.isfile(args.input) and not os.path.isdir(args.input)):
        raise Exception(3,"Input not file or directory.")
    
    # Check arg: Output (not required, if set it must be same as input)
    if args.output is None: # Output specified
        if not args.overwrite: # Ask to overwrite if no output specified
            if not ask(True,"Overwrite ?"):    
                raise Exception(4,"No output specified.")
            else:
                args.overwrite = True # Additional set overwrite
    elif os.path.exists(args.output): # On this path sth. already exists
        if not ((os.path.isfile(args.input) and os.path.isfile(args.output)) or (os.path.isdir(args.input) and os.path.isdir(args.output))):
            raise Exception(5,"Input object does not match with output")
        if not args.overwrite: # Ask to overwrite if output exists   
            if not ask(True,"Overwrite ?"):    
                raise Exception(6,"Already exist.")
            else:
                args.overwrite = True # Additional set overwrite
    else: # Output does not exist, but check if output is a file (contains ., prevents to set output of dir watermarking as single file)
        want_file = len(args.output.split('.')) > 1
        if os.path.isfile(args.input) and not want_file:
            raise Exception(7,"Output is not a file")
        if os.path.isdir(args.input) and want_file:
            raise Exception(8,"Output is not a directory")

    # Check arg: watermark or watermark text specified
    if args.wimage is None and args.wtext is None:
        raise Exception(9,"Watermark not specified.")
    elif args.wimage is not None and args.wtext is not None:
        raise Exception(10,"Both --wimage and --wtext can not be specified")
    elif args.wimage is not None and not os.path.exists(args.wimage):
        raise Exception(10,"Watermark image does not exist")
    elif args.wimage is not None and not os.path.isfile(args.wimage):
        raise Exception(11,"Watermark is not file.")
    
    # Check arg: watermark resize
    if args.wwidth is not None and args.wheight is not None:
        if not ask(True,"Watermark ratio may change. Continue anyway ?"):
            raise Exception(12,"Watermark ratio would change.")

    # Check arg: wpos
    if args.wposm is not None and args.wpos is None:
        raise Exception(13,"Can not use --wposm without --wpos")
    if (args.wpos is not None or args.wposm is not None) and (args.wposx is not None or args.wposy is not None):
        raise Exception(14,"Can not use --wpos or --wposm with --wposx or --wposy")

    # Check arg: wposx and wposy -> nothing to check

    # Check arg: wtext
    if args.wtext is not None and len(args.wtext) == 0:
        raise Exception(15,"Can't draw empty string")

    # Check arg: wcolor
    if args.wtext is None and args.wcolor is not None:
        raise Exception(16,"Argument --wcolor can be used only with --wtext")


    # Check arg: wfont
    if args.wfont is not None:
        if args.wtext is None:
            raise Exception(17,"Argument --wfont can only be used with --wtext")
        if not os.path.exists(args.wfont):
            raise Exception(18,"Font file does not exist")

    # Check arg: wfsize
    if args.wfsize is not None:
        if args.wtext is None:
            raise Exception(19,"Argument --wfsize can only be used with --wtext")
        if args.wfsize < 1:
            raise Exception(20,"Invalid font size")
def ask(default_value,message):
    print(message + " [" + ("Y" if default_value else "y") + "/" + ("n" if default_value else "N") + "]:",end='')
    i = input().lower()
    if i == "n" or i == "no":    
        return False
    elif i == "y" or i == "yes" or i == "ye":
        return True
    else:
        return default_value
def resize_image(image,width=None,height=None,allowRatioChange=False):
    orig_width,orig_height = image.size
    if width is not None and height is None: # Resize base on width
        height = int((float(width)/orig_width)*orig_height)
    elif width is None and height is not None: # Resize base on height
        width = int((float(height)/orig_height)*orig_width)
    elif width is not None and height is not None: # Ratio may change !!
        if allowRatioChange is None or not allowRatioChange:
            raise Exception(12,"Picture ratio may change")
    else:
        raise Exception(13,"Invalid arguments for resizing")
    return image.resize((width,height),Image.BICUBIC)
def make_text_img():
    # Load font if specified else use default font
    font_obj = ImageFont.truetype((IMG_TXT_DEFAULT_FONT if args.wfont is None else args.wfont),(IMG_TXT_DEFAULT_SIZE if args.wfsize is None else args.wfsize))
    
    # Create watermark
    t_w,t_h = font_obj.getsize(args.wtext)
    text_img = Image.new('RGBA',(t_w,t_h))
    img_draw = ImageDraw.Draw(text_img)
    img_draw.text((0,0),args.wtext,fill=(IMG_TXT_DEFAULT_COLOR if args.wcolor is None else args.wcolor),font=font_obj)

    return text_img

def load_image(path):
    print("Loading file %s" % (path))
    im = Image.open(path)
    im_safe = im.copy()
    im.close()
    return im_safe
def watermark_image_image(base_img,watermark_img,watermark_position):
    b_width, b_height = base_img.size
    transparent = Image.new('RGBA', (b_width, b_height), (0, 0, 0, 0))
    transparent.paste(base_img, (0, 0))
    transparent.paste(watermark_img, watermark_position, mask=watermark_img)
    transparent = transparent.convert("RGB") # To save as JPEG
    return transparent
def process_image(base_img,watermark_img):
    
    # Resize image if required
    if args.width is not None or args.height is not None:
        ask_result = False
        if args.width is not None and args.height is not None:
            ask_result = ask(True,"Picture ratio may change. Continue anyway ?")
        base_img = resize_image(base_img,args.width,args.height,ask_result)
    
    # Get sizes
    base_w,base_h = base_img.size
    watermark_w,watermark_h = watermark_img.size

    # Check if watermark will fit image
    if base_w < watermark_w  or base_h < watermark_h:
        raise Exception(15,"Watermark does not fit picture")

    # Calculate watermark pos
    pos_w = 0
    pos_h = 0
    margin = 0

    # Use corner based watermark position
    if args.wposm is not None and args.wposm >= 0:
        margin = args.wposm
    
    if args.wpos is not None:
        rel_pos = RelativePosition(args.wpos)
        
        if rel_pos == RelativePosition.LEFTUPPER_CORNER:
            pos_w = margin
            pos_h = margin
        elif rel_pos == RelativePosition.LEFT_CORNER:
            pos_w = margin
            pos_h = int((base_h - watermark_h)/2)
        elif rel_pos == RelativePosition.LEFTDOWN_CORNER:
            pos_w = margin
            pos_h = base_h - (watermark_h + margin)
        elif rel_pos == RelativePosition.DOWN_CORNER:
            pos_w = int((base_w - watermark_w)/2)
            pos_h = base_h - (watermark_h + margin)
        elif rel_pos == RelativePosition.RIGHTDOWN_CORNER:
            pos_w = base_w - (watermark_w + margin)
            pos_h = base_h - (watermark_h + margin)
        elif rel_pos == RelativePosition.RIGHT_CORNER:
            pos_w = base_w - (watermark_w + margin)
            pos_h = int((base_h - watermark_h)/2)
        elif rel_pos == RelativePosition.RIGHTUPPER_CORNER:
            pos_w = base_w - (watermark_w + margin)
            pos_h = margin
        elif rel_pos == RelativePosition.UPPER_CORNER:
            pos_w = int((base_w - watermark_w)/2)
            pos_h = margin
        
    # Absolute watermark position
    if args.wposx is not None and args.wposx >= 0:
        pos_w = args.wposx
    if args.wposy is not None and args.wposy >= 0:
        pos_h = args.wposy

    # Check if watermark will fit image in offset position
    if watermark_w + pos_w > base_w or watermark_h + pos_h > base_h:
         raise Exception(16,"Watermark does not fit in the picture")
    new_img = watermark_image_image(base_img,watermark_img,(pos_w,pos_h))

    return new_img
def process_file(input_path,output_path,watermark_img,delete_input_file_on_load):
    if input_path is None or output_path is None:
        raise Exception(40,"Invalid parameters")
    if not os.path.exists(input_path) or (os.path.exists(input_path) and not os.path.isfile(input_path)):
        raise Exception(40,"Faulty input file path %s" % (input_path))
    if os.path.exists(output_path) and ((input_path != output_path and not args.overwrite) or (input_path == output_path and not delete_input_file_on_load)):
        raise Exception(41,"File %s already exists" % (output_path))
    if watermark_img is None:
        raise Exception(42,"Watermark image not set")

    # Load image
    print("Opening image %s" % (input_path))
    input_img = load_image(input_path) # Load input image
    
    # Process image
    new_img = process_image(input_img,watermark_img)
    
    # Show preview
    if args.preview is not None and args.preview:
        new_img.show()

    # Save image
    f_saveimg = True
    if args.ask_to_save is not None and args.ask_to_save:
        f_saveimg = ask(True,"Keep picture?")
    
    if f_saveimg: # Image will be saved
        if delete_input_file_on_load: # Remove old image on load
            os.remove(input_path)
        if os.path.exists(output_path):
            if os.path.isfile(output_path):
                os.remove(output_path)
            elif os.path.isdir(output_path):
                os.removedirs(output_path)
        new_img.save(output_path)
        print("New image saved to %s" % (output_path))
    
    # Clean resources
    new_img.close()
    input_img.close()
def get_watermark():
    watermark_img = None
    if args.wimage is not None:
        watermark_img = load_image(args.wimage)
        if args.wwidth is not None or args.wheight is not None: # Resize watermark if specified
            watermark_img = resize_image(watermark_img,args.wwidth,args.wheight,False)
    elif args.wtext is not None and len(args.wtext) > 0:
        watermark_img = make_text_img()
        if args.wwidth is not None or args.wheight is not None: # Resize watermark if specified
            watermark_img = resize_image(watermark_img,args.wwidth,args.wheight,False)
    else:
        raise Exception(15,"Can not aquire watermark")

    return watermark_img
# Main program
def main():
    try:
        aquire_args()
        check_args()
    
        # Load resources
        watermark_img = get_watermark()

        # Input is FILE
        if os.path.isfile(args.input):
            if args.output is None:
                process_file(args.input,args.input,watermark_img,True)
            else:
                process_file(args.input,args.output,watermark_img,False)
        # Input is DIRECTORY
        elif os.path.isdir(args.input):
            # Output is SET (not in same directory)
            if args.output is not None:
                # Create output root directory if not exist
                if not os.path.exists(args.output):
                    os.makedirs(args.output)

                f_First = True
                rootFolder = None
                for root, dirs, files in os.walk(args.input): # For each directory
                    if f_First:
                        rootFolder = root
                        f_First = False
                    rel_root = root[(len(rootFolder)+1 if len(rootFolder)+1 < len(root) else len(rootFolder)):] 
                    
                    # Create subdirectories in output directory if it does not exist
                    for dir_name in dirs:
                        new_rel_dir_path = args.output + os.sep + rel_root + (os.sep if len(rel_root) > 0 else "") + dir_name
                        if not os.path.exists(new_rel_dir_path):
                            os.makedirs(new_rel_dir_path) # Create subdirectory
                            print("Creating directories %s ..." % (dir_name))
                        
                    # Process files in each directory
                    for file_name in files:
                        old_rel_file_path = root + (os.sep if len(root) > 0 else "") + file_name
                        new_rel_file_path = args.output + os.sep + rel_root + (os.sep if len(rel_root) > 0 else "") + file_name
                        if os.path.exists(new_rel_file_path): # Remove old file
                            os.remove(new_rel_file_path)
                        file_ext = (file_name.split('.'))[-1]
                        if file_ext in IMG_ALLOWED_EXT: # File extention in allowed list to process as image
                            process_file(old_rel_file_path,new_rel_file_path,watermark_img,False)
                        else:
                            print("Copying normal file %s ..." % (file_name))
                            shutil.copy2(old_rel_file_path,new_rel_file_path) 
            else: # Output is NOT set, save in Input directory, overwrite exsisting images
                for root, dirs, files in os.walk(args.input): # For each directory 
                    # Process files in each directory
                    for file_name in files:
                        old_rel_file_path = root + (os.sep if len(root) > 0 else "") + file_name
                        
                        file_ext = (file_name.split('.'))[-1]
                        if file_ext in IMG_ALLOWED_EXT: # File extention in allowed list to process as image
                            process_file(old_rel_file_path,old_rel_file_path,watermark_img,True)

        # Clean resource
        watermark_img.close()
        
    except (Exception,SystemExit) as e:
        if len(e.args) >= 2:
            print(e.args[1] + " (Error code: %i)" % (e.args[0]))
        if len(e.args) >= 1:
            sys.exit(e.args[0])
    except:
        print('Unexpected error: ',sys.exc_info()[0])
        raise

if __name__ == "__main__":
    main()
else:
    print("Script not run properly")
    sys.exit(1)