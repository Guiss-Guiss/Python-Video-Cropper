import cv2                          # pip install opencv-python
import tkinter as tk                # pip install tk
import numpy as np                  # pip install numpy
from tkinter import filedialog, Scale, HORIZONTAL, Toplevel, Button, OptionMenu, ttk    # pip install tk
from PIL import Image, ImageTk      # pip install pillow
from moviepy.editor import VideoFileClip    # pip install moviepy

aspect_ratios = ['Free', '1:1', '4:3', '16:9']  

def select_crop_area(file_path, selected_frame):

    coords = {'x': 0, 'y': 0, 'x2': 0, 'y2': 0}     # Dictionary to store the coordinates of the rectangle
    selected_aspect_ratio = tk.StringVar()          # Variable to store the selected aspect ratio
    selected_aspect_ratio.set('Free')               # Set the default aspect ratio to 'Free'
    current_rect = None                             # Variable to store the rectangle drawn on the canvas

    def click(event):
        nonlocal current_rect                       # Use the current_rect variable from the outer scope
        if current_rect:
            canvas.delete(current_rect)             # Delete the existing rectangle
        coords['x'] = event.x                       # Store the x coordinate of the mouse click
        coords['y'] = event.y                       # Store the y coordinate of the mouse click

    def drag(event):
        nonlocal current_rect
        coords['x2'] = event.x                      # Update the x2 coordinate as the mouse is dragged
        coords['y2'] = event.y                      
        
        w = abs(coords['x2'] - coords['x'])         # Calculate the width of the rectangle
        h = abs(coords['y2'] - coords['y'])         # Calculate the height of the rectangle

        aspect_ratio = selected_aspect_ratio.get()  # Get the selected aspect ratio
        
        if aspect_ratio != 'Free':
            a, b = map(int, aspect_ratio.split(':'))    # Split the aspect ratio into a and b
            new_h = w * b // a                          # Calculate the new height based on the aspect ratio
            new_w = h * a // b                          # Calculate the new width based on the aspect ratio
            
            if new_h > h:                               # If the new height is greater than the current height
                h = new_h                               # Update the height
            else:
                w = new_w                               # Else, update the width
                
            coords['x2'] = coords['x'] + w if coords['x2'] > coords['x'] else coords['x'] - w       # Update the x2 coordinate   
            coords['y2'] = coords['y'] + h if coords['y2'] > coords['y'] else coords['y'] - h       # Update the y2 coordinate
        
        if current_rect:
            canvas.delete(current_rect)            # Delete the existing rectangle
        current_rect = canvas.create_rectangle(coords['x'], coords['y'], coords['x2'], coords['y2'], outline='cyan', width=2)   # Draw a new rectangle     


    def release(event):
        nonlocal current_rect
        coords['x2'] = event.x              # Update the x2 coordinate as the mouse is released
        coords['y2'] = event.y              # Update the y2 coordinate as the mouse is released

        w = abs(coords['x2'] - coords['x'])   # Calculate the width of the rectangle
        h = abs(coords['y2'] - coords['y'])   # Calculate the height of the rectangle

        aspect_ratio = selected_aspect_ratio.get()  # Get the selected aspect ratio
        
        if aspect_ratio != 'Free':                      # If the aspect ratio is not 'Free'
            a, b = map(int, aspect_ratio.split(':'))    # Split the aspect ratio into a and b
            new_h = w * b // a                          # Calculate the new height based on the aspect ratio
            new_w = h * a // b                          # Calculate the new width based on the aspect ratio
                
            if new_h > h:                               # If the new height is greater than the current height
                h = new_h                               # Update the height
            else:
                w = new_w                               # Else, update the width
                    
            coords['x2'] = coords['x'] + w if coords['x2'] > coords['x'] else coords['x'] - w       # Update the x2 coordinate
            coords['y2'] = coords['y'] + h if coords['y2'] > coords['y'] else coords['y'] - h       # Update the y2 coordinate

        # Update the existing rectangle's coordinates
        canvas.coords(current_rect, coords['x'], coords['y'], coords['x2'], coords['y2'])           # Update the existing rectangle's coordinates

    def confirm_crop():     
        root.quit()        # Quit the mainloop     
        root.destroy()     # Close the window

    root = tk.Toplevel()    # Create a new window
    root.title("Select Crop Area")  # Set the title of the window   

    # Add OptionMenu for aspect ratio
    aspect_ratio_menu = OptionMenu(root, selected_aspect_ratio, *aspect_ratios)      # Create an OptionMenu
    aspect_ratio_menu.pack()                                                         # Pack the OptionMenu

    cap = cv2.VideoCapture(file_path)                       # Read using OpenCV
    cap.set(cv2.CAP_PROP_POS_FRAMES, selected_frame)        # Set the frame number to the selected frame
    ret, frame = cap.read()                                 # Read the frame
    
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)            # Convert the frame from BGR to RGB
    img = Image.fromarray(img)                              # Convert the frame to Image object
    img = ImageTk.PhotoImage(img)                           # Convert the Image object to PhotoImage object

    canvas = tk.Canvas(root, width=frame.shape[1], height=frame.shape[0])       # Create a canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=img)                          # Add the image to the canvas
    canvas.pack()                                                               # Pack the canvas

    canvas.bind("<ButtonPress-1>", click)                   # Bind the click event
    canvas.bind("<B1-Motion>", drag)                        # Bind the drag event
    canvas.bind("<ButtonRelease-1>", release)               # Bind the release event
    
    Button(root, text="Confirm Crop", command=confirm_crop).pack()  # Add a button to confirm the crop area

    root.mainloop()    # Start the mainloop
    
    x, y, x2, y2 = coords['x'], coords['y'], coords['x2'], coords['y2']     # Get the coordinates of the rectangle
    w, h = x2 - x, y2 - y                                                   # Calculate the width and height of the rectangle  
    
    cap.release()   # Release resources
    return x, y, w, h   # Return the coordinates of the rectangle

def crop_video(input_file, output_file, x, y, w, h, progress_var, total_frames, progress_window):   

    cap = cv2.VideoCapture(input_file)          # Read using OpenCV
    frame_rate = (cap.get(cv2.CAP_PROP_FPS))    # Get the frame rate of the original video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')    # Specify the codec
    
    temp_output = "temp_output.mp4"             # Create a temporary file to write the cropped video
    
    out = cv2.VideoWriter(temp_output, fourcc, frame_rate, (w, h))  # Create a VideoWriter object to write the cropped video

    for i in range(total_frames):
        ret, frame = cap.read()                 # Read the frame
        if not ret:                             # If the frame is not read
            break                               # Break the loop
        cropped_frame = frame[y:y+h, x:x+w]     # Crop the frame
        out.write(cropped_frame)                # Write the cropped frame to the output video
        progress = (i + 1) / total_frames * 100 # Calculate the progress
        progress_window.update()                # Update the progress window
        progress_var.set(progress)              # Update the progress bar

    # Release resources
    cap.release()               
    out.release()
    cv2.destroyAllWindows()

    # Add audio using MoviePy
    video_clip = VideoFileClip(input_file).subclip(0, -1)       # Read the original video
    audio_clip = video_clip.audio                               # Get the audio from the original video
    cropped_video = VideoFileClip(temp_output)                  # Read the cropped video    
    final_video = cropped_video.set_audio(audio_clip)           # Add the audio to the cropped video
    # final_video.write_videofile(output_file, codec="libx264", bitrate="8000k", fps=29.97, audio_codec="aac", audio_bitrate="300k", preset="slow")         # Write the final video to the output file
    final_video.write_videofile(output_file, codec="libx264", bitrate="10000k", fps=29.97, audio_codec="aac", audio_bitrate="320k", preset="veryslow")      # Write the final video to the output file
    
def get_video_dimensions(file_path):
    cap = cv2.VideoCapture(file_path)                       # Read using OpenCV
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))          # Get the width of the video
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))        # Get the height of the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))   # Get the total number of frames in the video
    cap.release()                                           # Release resources
    return width, height, total_frames                      # Return the width, height and total number of frames

def show_progress(progress):
    progress_window = Toplevel()                            # Create a new window
    progress_window.title("Progress")                       # Set the title of the window
    progress_window.geometry("400x100")                     # Set the size of the window
    
    tk.Label(progress_window, text=f"Cropping video").pack()    # Add a label to show the progress
    progress_var = tk.DoubleVar()                               # Variable to store the progress

    progress_bar = tk.Scale(progress_window, variable=progress_var, orient="horizontal", from_=0, to=100, length=350)       # Add a progress bar
    progress_bar.pack()                                                                                                     # Pack the progress bar
    
    progress_var.set(progress)                  # Set the progress
    progress_window.update()                    # Update the progress window
    return progress_window, progress_var        # Return the progress window and the progress variable




if __name__ == "__main__":
    input_file = filedialog.askopenfilename(title="Select Input Video", filetypes=[("MP4 files", "*.mp4")])                                 # Ask the user to select the input video
    output_file = filedialog.asksaveasfilename(title="Save Output Video", defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])      # Ask the user to select the output video

    if input_file and output_file:                                          # If the user has selected both input and output files
        width, height, total_frames = get_video_dimensions(input_file)      # Get the width, height and total number of frames of the video

        root = tk.Tk()                                  # Create a new window
        root.title("Select Frame")                      # Set the title of the window
        cap = cv2.VideoCapture(input_file)              # Read using OpenCV

        def update_image(value):
            cap.set(cv2.CAP_PROP_POS_FRAMES, value)     # Set the frame number to the selected frame
            ret, frame = cap.read()                     # Read the frame
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)        # Convert the frame from BGR to RGB
                img = Image.fromarray(img)                          # Convert the frame to Image object
                img = ImageTk.PhotoImage(img)                       # Convert the Image object to PhotoImage object
                canvas.create_image(0, 0, anchor=tk.NW, image=img)  # Add the image to the canvas
                canvas.image = img                                  # Store the image in the canvas

        canvas = tk.Canvas(root, width=width, height=height)        # Create a canvas
        canvas.pack()                                               # Pack the canvas
        
        slider = Scale(root, from_=0, to=total_frames-1, orient=HORIZONTAL)     # Add a slider
        slider.pack()
        slider.bind("<Motion>", lambda e: update_image(slider.get()))           # Bind the slider to update the image

        def crop_and_submit():

            selected_frame = slider.get()                                       # Get the selected frame
            x, y, w, h = select_crop_area(input_file, selected_frame)           # Select the crop area
            
            if w > 0 and h > 0:
                progress_window, progress_var = show_progress(0)                                                    # Show the progress window
                crop_video(input_file, output_file, x, y, w, h, progress_var, total_frames, progress_window)        # Crop the video
                progress_window.destroy()                                                                            # Destroy the progress window
                
                root.quit()
                root.destroy()
            else:
                print("Invalid cropping area.")     # If the width or height is 0, print an error message

        tk.Button(root, text="Select", command=crop_and_submit).pack()   # Add a button to select the crop area

        root.mainloop()     # Start the mainloop
        cap.release()       # Release resources

