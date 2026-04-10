import numpy as np
import cv2
import random

class Stitcher:
    def __init__(self):
        # No persistent attributes required; pipeline is stateless
        pass

    def stitch(self, img_left, img_right):  # Add input arguments as you deem fit
        '''
            This function runs the full stitching pipeline.
            It takes two images and returns a stitched panorama.
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
        homography = self.find_homography(matches, keypoints_l, keypoints_r)

        # Step 5 - Warp images to create the panoramic image
        if homography is None:
            print("Homography failed")
            return img_left
                 
        # warp the right image into the left image frame
        result = self.warping(img_left, img_right, homography)
        return result

    def compute_descriptors(self, img):
        # convert image to grayscale since SIFT works on intensity values
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
         # detect keypoints and compute descriptors
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
            # sort by smallest distance
            distances.sort(key=lambda x: x[0])
    
            best_dist, best_j = distances[0]
            
            # keep only matches that are close enough
            if best_dist < 120:
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
            # shift second image points to the right
            pt2 = (int(pt2[0] + img_left.shape[1]), int(pt2[1]))
    
            cv2.line(img, pt1, pt2, (0, 255, 0), 1)
    
        img_with_correspondences = img
    
        cv2.imshow('correspondences', img_with_correspondences)
        cv2.waitKey(0)

    def find_homography(self, matches, keypoints_l, keypoints_r):
        '''
        Fit the best homography model with the RANSAC algorithm.
        '''
        # Malavika: RANSAC initialisation
        max_inliers = []
        best_H = None
    
        for _ in range(200):  
            
            # need at least 4 points to compute homography
            if len(matches) < 4:
                break
        
            # Malavika: random sampling
            sample = np.random.choice(len(matches), 4, replace=False)
        
            pts_l = []
            pts_r = []
        
            for idx in sample:
                i, j = matches[idx]
                pts_l.append(keypoints_l[i].pt)
                pts_r.append(keypoints_r[j].pt)
        
            pts_l = np.array(pts_l)
            pts_r = np.array(pts_r)
            #compute homography
            H = Homography().solve_homography(pts_l, pts_r)

            if H is None:
                continue

            # count how many matches agree with this homography
            inliers = []

            for i, j in matches:
                p1 = np.array([*keypoints_l[i].pt, 1])
                p2 = np.array([*keypoints_r[j].pt, 1])

                proj = H @ p1
                if proj[2] == 0:
                    continue
                proj /= proj[2]

                error = np.linalg.norm(proj[:2] - p2[:2])
                # if error is small, it is a good match (inlier)
                if error < 10:
                    inliers.append((i, j))
                    
            # keep the best homography (most inliers)
            if len(inliers) > len(max_inliers):
                max_inliers = inliers
                best_H = H
        return best_H
        
   #Ami :implementing warping        
    def warping(self, img_left, img_right, homography):

        h, w = img_left.shape[:2]

        # bigger canvas
        result = np.zeros((h, w*2, 3), dtype=np.uint8)

        # place left image first
        result[0:h, 0:w] = img_left

        # invert homography (important!)
        H_inv = np.linalg.inv(homography)

    
        for y in range(h):
            for x in range(w*2):

                # shift x so right image maps correctly
                p = np.array([x - w, y, 1])

                p_t = H_inv @ p

                if p_t[2] == 0:
                    continue

                p_t /= p_t[2]

                x_src, y_src = int(p_t[0]), int(p_t[1])

                if 0 <= x_src < img_right.shape[1] and 0 <= y_src < img_right.shape[0]:

                    if (result[y, x] == [0,0,0]).all():
                        result[y, x] = img_right[y_src, x_src]

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

        A = []

        for i in range(len(S)):
            x, y = S[i]
            xp, yp = D[i]

            A.append([-x, -y, -1, 0, 0, 0, x*xp, y*xp, xp])
            A.append([0, 0, 0, -x, -y, -1, x*yp, y*yp, yp])

        A = np.array(A)

        U, S, Vt = np.linalg.svd(A)
        H = Vt[-1].reshape(3, 3)

        return H


if __name__ == "__main__":
    # Read the image files
    # Malavika: image loading
    img_left = cv2.imread("s1.jpg")
    img_right = cv2.imread("s2.jpg")
    img_left = cv2.resize(img_left, (600,400))
    img_right = cv2.resize(img_right, (600,400))

    stitcher = Stitcher()
    result = stitcher.stitch(img_left, img_right)  # Add input arguments as you deem fit

    # show the result
    cv2.imshow('result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
