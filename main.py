import json
import os
import re
import sys
import logging
import cv2


def run_tests(path_to_images_dir: str, path_to_expected_res_dir: str, path_to_results_dir: str):
    image_names = os.listdir(path_to_images_dir)

    for i, image_name in enumerate(image_names):
        img = cv2.imread(f'{path_to_images_dir}/{image_name}')

        res = re.search('img\d+', image_name)
        if res is not None:
            file_name = res.group(0)
        else:
            raise Exception('image file name must contains imgIMAGENUM.\n For example it must be img102132.jpg')

        # draw expected imtersection points
        expected_file_name = f'{file_name}.json'
        with open(f'{path_to_expected_res_dir}/{expected_file_name}') as json_file:
            data = json.load(json_file)
            objects = data['objects']
            for obj in objects:
                if obj['geometryType'] == 'point':
                    x, y = obj['points']['exterior'][0]
                    cv2.circle(img, (x, y), 2, (0, 255, 0), 2)

        res = re.search('\w+', image_name)
        if res is not None:
            file_name = res.group(0)
        else:
            raise Exception('image file name must contains imgIMAGENUM.\n For example it must be img102132.jpg')

        res_file_name = f'{file_name}.txt'
        with open(f'{path_to_results_dir}/{res_file_name}') as res_file:
            lines = res_file.readlines()
            for line in lines:
                res = re.findall('\d+', line)
                if len(res) == 2:
                    x, y = int(res[0]), int(res[1])
                    cv2.circle(img, (x, y), 1, (0, 0, 255), 2)

        cv2.imshow(image_name, img)

    cv2.waitKey()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        logging.error("wrong imput arguments count, program takes 4 arguments:"
                      " path_to_images_dir, path_to_expected_res_dir, path_to_results_dir")
        exit(-1)

    run_tests(sys.argv[1], sys.argv[2], sys.argv[3])