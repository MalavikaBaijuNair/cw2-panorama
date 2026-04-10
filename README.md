
# Panorama Stitching Project

## Group Members
- Ami  
- Malavika  

## Overview
This project implements a panorama stitching pipeline that takes two overlapping images and produces a stitched output. The system follows key computer vision stages including feature detection, feature matching, homography estimation using RANSAC, and image warping.

The implementation adheres to coursework requirements by developing custom algorithms for feature matching, homography estimation, and image stitching.

---

## Contributions

This project was developed collaboratively, with both members contributing across all stages of the pipeline. While initial responsibilities were divided, all components were jointly reviewed, tested, and refined to ensure correctness and robustness of the final system.

### Malavika
- Image loading and preprocessing  
- Feature detection using SIFT  
- Initial implementation of feature matching  
- RANSAC sampling for homography estimation  
- Final debugging, optimisation and code refinement

### Ami
- Refinement of feature matching and filtering  
- Implementation of homography computation (DLT)  
- RANSAC inlier selection and model selection  
- Image warping and stitching  
- Minor corrections, final refinements, and code improvements after testing

### Shared Contribution
- Joint debugging and testing of all pipeline stages  
- Parameter tuning (matching threshold, RANSAC iterations)  
- Validation of results on multiple image pairs  
- Improvement of final stitching quality and alignment  

Both members were actively involved in improving, verifying, and refining each stage of the implementation, ensuring equal contribution to the final result.

---

## Testing
The algorithm was tested on:
- Provided coursework images (successful stitching)
- Self-captured images (variable performance depending on scene structure)
  
Note:
After running the code, the correspondence image appears first.
Press any key to display the final stitched result.

---
## Running with Different Images

The repository includes both the provided images (`.jpg`) and self-captured images (`.jpeg`).

To run the code with different images, update the file names in the main section of `cw2.py`:

- For provided images:
      img_left = cv2.imread("s1.jpg")
      img_right = cv2.imread("s2.jpg")

- For self-captured images:
      img_left = cv2.imread("s1.jpeg")
      img_right = cv2.imread("s2.jpeg")

## Observations
The method performs well on structured scenes with strong geometric features. Performance degrades in cases with:
- low overlap
- repetitive textures
- moving objects

This reflects known limitations of feature-based homography estimation methods.
