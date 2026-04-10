import numpy as np
import cv2


class Stitcher:
    def __init__(self):
        pass

    def stitch(self, img_left, img_right):  # Add input arguments as you deem fit
        '''
            The main method for stitching two images
        '''

        # Step 1 - extract the keypoints and features with a suitable feature
        # detector and descriptor
        keypoints_l, descriptors_l = self.compute_descriptors(img_left)
        keypoints_r, descriptors_r = self.compute_descriptors(img_right)

        # Step 2 - Feature matching. You will have to apply a selection technique
        # to choose the best matches
        matches = self.matching(keypoints_l, keypoints_r,
                                descriptors_l, descriptors_r)  # Add input arguments as you deem fit

        print("Number of matching correspondences selected:", len(matches))

        # Step 3 - Draw the matches connected by lines
        self.draw_matches(img_left, img_right, matches, keypoints_l, keypoints_r)

        # Step 4 - fit the homography model with the RANSAC algorithm
        homography = self.find_homography(matches)

        # Step 5 - Warp images to create the panoramic image
        result = self.warping(img_left, img_right, homography)  # Add input arguments as you deem fit

        return result

    def compute_descriptors(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(gray, None)

        return keypoints, descriptors


    def matching(self, keypoints_l, keypoints_r, descriptors_l, descriptors_r):
        '''
        Find the matching correspondences between the two images
        '''

        good_matches = []

        # Ami: safety check before matching implementation
        if len(descriptors_l) == 0 or len(descriptors_r) == 0:
            return good_matches
    
        # Malavika: computing distances between descriptors
        for i in range(len(descriptors_l)):
            distances = []
    
            for j in range(len(descriptors_r)):
                dist = np.linalg.norm(descriptors_l[i] - descriptors_r[j])
                distances.append((dist, j))
    
            if len(distances) == 0:
                continue
    
            distances.sort(key=lambda x: x[0])
    
            best_dist, best_j = distances[0]
    
            if best_dist < 300:
                good_matches.append((i, best_j))
    
        return good_matches 

    def draw_matches(self, img_left, img_right, matches, keypoints_l, keypoints_r):
        '''
        Connect correspondences between images with lines and draw these lines
        '''

        # Malavika: drawing lines between matched keypoints
        img = np.hstack((img_left, img_right))
    
        for (i, j) in matches:
            pt1 = tuple(map(int, keypoints_l[i].pt))
            pt2 = tuple(map(int, keypoints_r[j].pt))
            pt2 = (int(pt2[0] + img_left.shape[1]), int(pt2[1]))
    
            cv2.line(img, pt1, pt2, (0, 255, 0), 1)
    
        img_with_correspondences = img
    
        cv2.imshow('correspondences', img_with_correspondences)
        cv2.waitKey(0)

    def find_homography(self, matches):
        '''
        Fit the best homography model with the RANSAC algorithm.
        '''

        # Your code here
        # Use the method solve_homography(source_points,
        # destination_points) from the class Homography in your implementation
        # of the RANSAC algorithm

        return homography

    def warping(self,img_left, img_right, homography):  # Add input arguments as you deem fit
        '''
           Warp images to create panoramic image
        '''

        # Your code here. You will have to warp one image into another via the
        # homography. Remember that the homography is an entity expressed in
        # homogeneous coordinates.

        return result

    def remove_black_border(self, img):
        '''
        Remove black border after stitching
        '''
        return cropped_image


class Blender:
    def linear_blending(self):
        '''
        linear blending (also known as feathering)
        '''

        return linear_blending_img

    def customised_blending(self):
        '''
        Customised blending of your choice
        '''
        return customised_blending_img


class Homography:
    def solve_homography(self, S, D):
        '''
        Find the homography matrix between a set of S points and a set of
        D points
        '''

        # Your code here. You might want to use the DLT algorithm developed in cw1.

        return H


if __name__ == "__main__":
    # Read the image files
    # Malu: image loading
    img_left = cv2.imread("s1.jpg")
    img_right = cv2.imread("s2.jpg")

    stitcher = Stitcher()
    result = stitcher.stitch(img_left, img_right)  # Add input arguments as you deem fit

    # show the result
    cv2.imshow('result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
