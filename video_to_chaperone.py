import os, sys, cv2
from PIL import Image, ImageOps


def get_frame_list(video_file):
    frames = []
    cap = cv2.VideoCapture(video_file)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        frames.append(frame)
    cap.release()
    cv2.destroyAllWindows()
    return frames


def convert_frame_to_img_array(frame):
    im = ImageOps.flip(Image.fromarray(frame))
    im.thumbnail(size, Image.ANTIALIAS)
    img = im.load()
    x, y = im.size

    image_list = [[0 for xs in range(0, x)] for ys in range(0, y)]
    
    for j in range(0, y):
        for i in range(0, x):
            pixel = img[i, j]
            if pixel[0] > 85 and pixel[0] < 170:
                if pixel[1] > 85 and pixel[1] < 170:
                    if pixel[2] > 85 and pixel[2] < 170:
                        image_list[j][i] = 1
            elif pixel[0] < 85:
                if pixel[1] < 85:
                    if pixel[2] < 85:
                        image_list[j][i] = 2

    return image_list


def add_black_square(coordinates, square_len):
    last_point = coordinates[-1]
    coordinates.append((last_point[0], last_point[1] - square_len))
    coordinates.append((last_point[0] + square_len, last_point[1] - square_len))
    coordinates.append((last_point[0] + square_len, last_point[1]))
    coordinates.append((last_point[0], last_point[1]))
    coordinates.append((last_point[0] + square_len, last_point[1]))
    return coordinates


def add_grey_square(coordinates, square_len):
    last_point = coordinates[-1]
    coordinates.append((last_point[0], last_point[1] - square_len))
    coordinates.append((last_point[0] + square_len, last_point[1]))
    coordinates.append((last_point[0], last_point[1]))
    coordinates.append((last_point[0], last_point[1] - square_len))
    coordinates.append((last_point[0] + square_len, last_point[1] - square_len))
    coordinates.append((last_point[0] + square_len, last_point[1]))
    coordinates.append((last_point[0], last_point[1]))
    coordinates.append((last_point[0] + square_len, last_point[1]))
    return coordinates


def add_white_square(coordinates, square_len):
    last_point = coordinates[-1]
    coordinates.append((last_point[0], last_point[1] - square_len))
    coordinates.append((last_point[0] + square_len, last_point[1]))
    coordinates.append((last_point[0], last_point[1]))
    coordinates.append((last_point[0], last_point[1] - square_len))
    coordinates.append((last_point[0] + square_len, last_point[1] - square_len))
    coordinates.append((last_point[0] + square_len, last_point[1]))
    coordinates.append((last_point[0] + square_len, last_point[1] - square_len))
    coordinates.append((last_point[0], last_point[1]))
    coordinates.append((last_point[0] + square_len, last_point[1]))
    return coordinates


def add_line_reset(coordinates, square_len):
    last_point = coordinates[-1]
    coordinates.append((last_point[0], last_point[1] - square_len))
    coordinates.append((0, last_point[1] - square_len))
    return coordinates


def convert_img_arrays_to_coordinates(img_arrays):
    coordinates = [(0, 0)]
    for y in range(0, len(img_arrays)):
        for x in range(0, len(img_arrays[y])):
            if img_arrays[y][x] == 0:
                coordinates = add_white_square(coordinates, square_len)
            elif img_arrays[y][x] == 1:
                coordinates = add_grey_square(coordinates, square_len)
            elif img_arrays[y][x] == 2:
                coordinates = add_black_square(coordinates, square_len)

            if x == len(img_arrays[y]) - 1:
                coordinates = add_line_reset(coordinates, square_len)
    return coordinates


def save_coordinates_to_file(coordinates, frame_dir, frame_name):
    if not os.path.exists(frame_dir):
        os.makedirs(frame_dir)

    for i in range(0, len(coordinates)):
        with open(f'{frame_dir}/{frame_name}{i}.txt', 'w') as frame_file:
            frame_file.write(f"{len(coordinates[i])} ")

            for point in range(0, len(coordinates[i])):
                frame_file.write(f"{coordinates[i][point][0]:.2f} ")
                frame_file.write(f"{coordinates[i][point][1]:.2f} ")


if __name__ == "__main__":
    video_file = sys.argv[1]
    frame_dir = sys.argv[2]
    frame_name = sys.argv[3]
    square_len = float(sys.argv[4])
    size = int(sys.argv[5]), int(sys.argv[6])

    print("getting frames")
    frames = get_frame_list(video_file)

    print("converting frames to images arrays")
    img_arrays = [convert_frame_to_img_array(frame) for frame in frames]
    
    print("converting image arrays to coordinates")        
    coordinates = [convert_img_arrays_to_coordinates(img_array) for img_array in img_arrays]

    print(f"saving to ./{frame_dir}/")  
    save_coordinates_to_file(coordinates, frame_dir, frame_name)

    print(f"finished saving")  