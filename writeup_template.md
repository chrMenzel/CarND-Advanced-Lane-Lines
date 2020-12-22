## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./examples/undistort_output.png "Undistorted"
[image2]: ./test_images/test1.jpg "Road Transformed"
[image3]: ./examples/binary_combo_example.jpg "Binary Example"
[image4]: ./examples/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the third code cell of the IPython notebook located in "./Project2.ipynb".  

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained the result in cell No 4 in the IPython notebook.

![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, have coded this in cell No 5 and provided an output of one oft images to show the difference.

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image (thresholding steps in cells 6 and 7. In cell 7 I have provided a gallery from the original image to the final output image. In cell 8 I provided the output image in grayscale in a larger format.

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warp()`, which appears in cell 11 in the file `Project2.py`. Output images are below this cell.   The `warp()` function takes as inputs an image (`img`). For the source (`src`) and destination (`dst`) points I chose to hardcode the source and destination points in the fuction itself. Before that, I used the function get_warp_points to get the destinatien points. The source points I got by very much trying until I found the result is satisfactory:

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 253, 697      | 303, 697      | 
| 585, 456      | 303, 0        |
| 700, 456      | 1011, 0       |
| 1061, 690     | 1011, 697     |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto 8 test images and their warped counterpart to verify that the lines appear parallel in the warped image.


#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

In cell 12 I used nearly the code from the course to identify the lane line pixels. As documented I use the two highest peaks from the histogram as a starting point and then use sliding windows moving upward in the image (further along the road) to determine where the lane lines are. I did some other stuff and fit my lane lines with a 2nd order polynomial kinda like this (see try-catch-block in the function find_lane_lines).

![alt text][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in the bottom lines of my code in the function find_lane_lines() in cell 12. I did this the same way as described in the course.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in the bottom lines in cell 12 after the function `find_lane_lines()`. Below this cell is an example of my result on a test image.

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](https://github.com/chrMenzel/CarND-Advanced-Lane-Lines/blob/master/project_video_out.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.

Approach:
- I compute the camera calibration matrix and distortion coefficients with the help of the given set of chessboard images.
- After that I applied a distortion correction to raw test images.
- I used color transforms and thresholds to create a thresholded binary image.
- After that I applied a perspective transform to rectify binary image ("birds-eye view").
- Now I detect lane pixels and fit to find the lane boundary.
- I determine the curvature of the lane and vehicle position with respect to center.
- I warp the detected lane boundaries back onto the original image.
- And I output a visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position with all the test images.
- After that I implemented a pipeline to produce a new video including the green coloured lane and display of the curvature and position of the car in the images.

Techniques:
The above described techniques worked very fine on straight streets and even streets with a curve. Another condition for well-working is that there are lines on the lane where the car is. If there are sometimes no lines or the lane is not even enough there is a problem to recognize the correct lanes. Also with a very curvy road the current implementation does not work well enough. I also did not use the provided Line class to get a better possibility to identify the line positions from previous findings. I can only admit for that. I had not enough time to implement this project as well as I wanted.

Improvements:
The described problems are also the issues where I could improve the project. Apart from using a history with the Line class, I could use the curvature from a defined degree to reduce the length of the region of interest and better raise the width to identify the lines. This could do a better job in curvy or down or uphill streets.

All in all I think this is a very exciting project.


