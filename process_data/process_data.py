import numpy as np
import matplotlib.pyplot as plt 
import pickle 

# You must collect the data from /data/pose_info.obj

length_scale = 0.01 *9.85 # distance between the centers of 2 qr codes


#this is the coordinates of the watchtower
#  corner (origin at north east corner of poster )
# that is aligned plus the disantce between the camera and that
camera_pose = np.array([14, 4, 0])*length_scale + np.array([6, -2.0, -61])*0.01


# this covererts the reference frames from the camrera to the room frame
# with origin at the north east corner
def camera_frame_to_calibration_poster_frame(position):
    
    theta = np.deg2rad(20.0)
    matrix = np.array(
                     [[-1,             0,              0],
                      [0, np.cos(theta), -np.sin(theta)], 
                      [0, np.sin(theta),  np.cos(theta)]])

    position = np.array(position)
    print(position)
    p_prime = np.dot(matrix, position) + camera_pose
    return p_prime



def ground_truth_positions():
    tag_index = 0
    position_list = []
    for i in range(25):
        for j in range(10):
            position = [length_scale*i, length_scale*j, 0]
            tag_index += 1

# returns ground truth position for a given index
def get_ground_truth(index):
  ii= index // 10
  jj = index % 10
  return np.array([length_scale*ii, length_scale*jj, 0])
    

# display the found poses
def process_poses(poses):
    position_list = []
    tag_list = []
    for det in poses[:]:
        # don't repeat tags (it is consenstent, I checked)
        if det['tag_id'] in tag_list:
          continue

        tag_list.append(det['tag_id'])
        position = det['transformation']
        position_list.append(camera_frame_to_calibration_poster_frame(position))


    position_ground_truth = []
    for i in tag_list:
        position_ground_truth.append(get_ground_truth(i))

    position_ground_truth = np.array(position_ground_truth)

    position_list = np.array(position_list)
    df = position_ground_truth - position_list
    print(position_list.shape)
    plt.scatter(position_list[:, 0], position_list[:, 1])
    plt.scatter(position_ground_truth[:, 0], position_ground_truth[:, 1])

    for i,t in enumerate(tag_list):
      plt.arrow(position_list[i, 0], position_list[i, 1], df[i, 0], df[i,1])
      plt.annotate(t, (position_ground_truth[i, 0], position_ground_truth[i, 1]),
        textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center')

      print(t, "\t", np.linalg.norm(df[i, :]))

    plt.scatter(camera_pose[0], camera_pose[1])
    plt.show()



poses  = pickle.load( open( "pose_info.obj", "rb" ) )


print(get_ground_truth(150))
if __name__ == "__main__":
    process_poses(poses)
