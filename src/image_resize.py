### code for image resizing

# libraries
from PIL import Image

# core functions
def check_ratio(im, desired_ratio):
    """this function checks if image is wider or taller than a desired ratio
    desired_ratio is a tuple of (goal width, goal height)"""
    width, height = im.size
    current_ratio = width / height
    
    goal_width_ratio, goal_height_ratio = desired_ratio
    goal_ratio = goal_width_ratio / goal_height_ratio

    if current_ratio == goal_ratio:
        return "just right"
    elif current_ratio > goal_ratio:
        return "too wide"
    elif current_ratio < goal_ratio:
        return "too tall"

def adjust_ratio(im, desired_ratio):
    """resizes image to specified ratio
    desired_ratio is tuple of (goal width, goal height)
    """
    width, height = im.size
    goal_width_ratio, goal_height_ratio = desired_ratio
    current_ratio = check_ratio(im, desired_ratio)

    if current_ratio == "just right": # no changes needed
        return im
    elif current_ratio == "too wide": # fix height and crop width to 5:4 ratio
        new_width = (height * goal_width_ratio) / goal_height_ratio
        left = (width - new_width) // 2
        right = (width + new_width) // 2
        top = 0
        bottom = height
        return im.crop((left, top, right, bottom))
    elif current_ratio == "too tall": # fix width and crop height
        new_height = (width * goal_height_ratio) // goal_width_ratio
        left = 0
        right = width
        top = (height - new_height) // 2
        bottom = (height + new_height) // 2
        return im.crop((left, top, right, bottom))
    
def calculate_width(desired_height, desired_ratio):
    """calculates width needed for an image with specified height to have specified ratio
    ratio is a tuple of (goal width, goal height)"""
    goal_width_ratio, goal_height_ratio = desired_ratio
    needed_width = (desired_height * goal_width_ratio ) // goal_height_ratio
    return needed_width

def calculate_height(desired_width, desired_ratio):
    """calculates height needed for an image with specified width to have specified ratio
    ratio is a tuple of (goal width, goal height)"""
    goal_width_ratio, goal_height_ratio = desired_ratio
    needed_height = (desired_width * goal_height_ratio ) // goal_width_ratio
    return needed_height

def adjust_size(im, desired_ratio, desired_width = None, desired_height = None):
    """adjusts image to desired pixels
    desired ratio is a tuple with (goal width ratio, goal height ratio)
    """
    if desired_width is None and desired_height is None:
        raise TypeError('need to specify either a desired width or a desired height')
    elif desired_width is not None and desired_height is None:
        desired_height = calculate_height(desired_width, desired_ratio)
    elif desired_height is not None and desired_width is None:
        desired_width = calculate_width(desired_height, desired_ratio)
    return im.resize((desired_width, desired_height)), desired_width, desired_height

def main(source_filename, destination_filename, desired_ratio, desired_width = None, desired_height = None):
    """full image conversion process"""
    im = Image.open(source_filename)
    im = adjust_ratio(im = im, desired_ratio = desired_ratio)
    im.save(destination_filename)

    if desired_height is not None:
        im, desired_width, desired_height = adjust_size(im = im, desired_ratio = desired_ratio, desired_height = desired_height)
    elif desired_width is not None:
        im, desired_width, desired_height = adjust_size(im = im, desired_ratio = desired_ratio, desired_width = desired_width)
    elif desire_height is None and desired_width is None:
        raise TypeError('need to specify either a desired width or a desired height')

    im.save(destination_filename)
    return desired_width, desired_height

# test code
if __name__ == '__main__':
    source_filename = 'resources/raw_images/Asparagus_and_Golden_Rice_Bowls.jpg'
    destination_filename = 'resources/processed_images/Asparagus_and_Golden_Rice_Bowls.jpg'
    main(source_filename, destination_filename, (5, 4), desired_width = 250)



