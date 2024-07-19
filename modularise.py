import cv2
import layoutparser as lp
from paddleocr import PaddleOCR, draw_ocr
import tensorflow as tf
import numpy as np
import pandas as pd
import os



# EXTRACT TABLE FROM THE IMAGE
def extractTable(file_path, output_path):

    image = cv2.imread(file_path)
    if image is None:
        return None
    image = image[..., ::-1]

    # load model
    model = lp.PaddleDetectionLayoutModel(config_path="lp://PubLayNet/ppyolov2_r50vd_dcn_365e_publaynet/config",
                                threshold=0.5,
                                label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"},
                                enforce_cpu=False,
                                enable_mkldnn=True)
    
    # detect Table
    table_is_present = False

    layout = model.detect(image)

    for l in layout:
        if l.type == "Table":
            table = l
            table_is_present = True
            break
    
    if table_is_present == False:
        return None
    table_block = table.block
    x_1 = int(table_block.x_1)
    y_1 = int(table_block.y_1)
    x_2 = int(table_block.x_2)
    y_2 = int(table_block.y_2)


    cv2.imwrite(output_path, image[y_1:y_2, x_1:x_2])
    return output_path



class ImageToCsv:
    ocr = PaddleOCR(lang='en')

    def __init__(self, image_path):
        self.image_path = image_path
    
    def read_image(self):
        self.image = cv2.imread(self.image_path)
        self.image_height = self.image.shape[0]
        self.image_width = self.image.shape[1]

    def load_image_data(self):
        output = ImageToCsv.ocr.ocr(self.image_path)
        # for word in output[0]:
        #     print(word)

        self.boxes = [line[0] for line in output[0]]
        self.texts = [line[1][0] for line in output[0]]
        self.probabilites = [line[1][1] for line in output[0]]

    def get_rows_and_column_of_table(self):
        self.horizontal_boxes = []
        self.vertical_boxes = []

        # image_non = image_cv.copy()
        for box in self.boxes:
            x_h, x_v = 0, int(box[0][0])
            y_h, y_v = int(box[0][1]), 0
            width_h, width_v = self.image_width, int(box[2][0] - box[0][0])
            height_h, height_v = int(box[2][1] - box[0][1]),  self.image_height

            self.horizontal_boxes.append([x_h, y_h, x_h + width_h, y_h + height_h])
            self.vertical_boxes.append([x_v, y_v, x_v + width_v, y_v + height_v])

        #     cv2.rectangle(image_non, (x_h, y_h), (x_h + width_h, y_h + height_h), (0, 255, 0), 1)
        #     cv2.rectangle(image_non, (x_v, y_v), (x_v + width_v, y_v + height_v), (255, 0, 0), 1)

        # cv2.imwrite("boundary_images/non_max_images/year.jpg", image_non)

        horizontal_out = tf.image.non_max_suppression(
            self.horizontal_boxes,
            self.probabilites,
            max_output_size=1000,
            iou_threshold=0.1,
            score_threshold=float('-inf'),
            name=None)

        self.horizontal_index = np.sort(np.array(horizontal_out))


        vertical_out = tf.image.non_max_suppression(
            self.vertical_boxes,
            self.probabilites,
            max_output_size=1000,
            iou_threshold=0.1,
            score_threshold=float('-inf'),
            name=None
        )

        self.vertical_index = np.sort(np.array(vertical_out))
        unordered_box = []
        for i in self.vertical_index:
            unordered_box.append(self.vertical_boxes[i][0])

        self.ordered_box = np.argsort(unordered_box)

    def intersection(self, horiz_box, vert_box):
        return [vert_box[0], horiz_box[1], vert_box[2], horiz_box[3]]
    
    def iou(self, box_1, box_2):

        x_1 = max(box_1[0], box_2[0])
        y_1 = max(box_1[1], box_2[1])
        x_2 = min(box_1[2], box_2[2])
        y_2 = min(box_1[3], box_2[3])

        intercept_area = abs(max((x_2 - x_1), 0) * max((y_2 - y_1), 0))
        if intercept_area == 0:
            return 0
        
        box_1_area = abs((box_1[2] - box_1[0]) * (box_1[3] - box_1[1]))
        box_2_area = abs((box_2[2] - box_2[0]) * (box_2[3] - box_2[1]))

        return intercept_area / (box_1_area + box_2_area - intercept_area)
    
    def formatText2RowsAndColumn(self):
        self.out_array = [["" for i in range(len(self.vertical_index))] for j in range(len(self.horizontal_index))]
        for i in range(len(self.horizontal_index)):
            for j in range(len(self.vertical_index)):
                result = self.intersection(
                self.horizontal_boxes[self.horizontal_index[i]],  self.vertical_boxes[self.vertical_index[self.ordered_box[j]]])
                for k in range(len(self.boxes)):
                    the_box = [self.boxes[k][0][0], self.boxes[k][0][1], self.boxes[k][2][0], self.boxes[k][2][1]]
                    if self.iou(result, the_box) >= 0.1:
                        self.out_array[i][j] = self.texts[k]

    def save_to_csv(self, output_path):
        pd.DataFrame(self.out_array).to_csv(output_path, index=False)


#TEST THE CLASS AND THE FUNCTION
image_path = "dataset/data-in-spreadsheet.png"

print("Extracting table....")

print("Successfully Extract table")

def converter_image_to_csv(file_path, filename):
    
    extract_table = extractTable(file_path, file_path)
    if extract_table is None:
        return None
    image_to_csv = ImageToCsv(extract_table)
  
    # print("reading table....")
    image_to_csv.read_image()
    # print("loading table data....")
    image_to_csv.load_image_data()
    # print("getting all the rows and column in the table...")
    image_to_csv.get_rows_and_column_of_table()
    # print("extracting the text in the table...")
    image_to_csv.formatText2RowsAndColumn()
    output_path = f"generated_csv/{filename}"
    # print("saving the csv to a file")
    image_to_csv.save_to_csv(output_path)
    return 1
    # print("Done successfully extracting table")

