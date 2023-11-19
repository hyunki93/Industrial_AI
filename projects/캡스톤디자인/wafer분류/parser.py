import json
import xml.etree.ElementTree as ET


import os
import json
from PIL import Image


# JSON 파일이 있는 디렉토리 경로
annotation_directory = r"D:\02.CBNU\캡스톤\roboflow 전처리\annotations"
image_directory = r"D:\02.CBNU\캡스톤\roboflow 전처리\images"
result_directory = r"D:\02.CBNU\캡스톤\roboflow 전처리\result"


def create_pascal_voc_xml(filename, width, height, annotations):
    root = ET.Element("annotation")

    filename_elem = ET.SubElement(root, "filename")
    filename_elem.text = filename

    size_elem = ET.SubElement(root, "size")
    width_elem = ET.SubElement(size_elem, "width")
    width_elem.text = str(width)
    height_elem = ET.SubElement(size_elem, "height")
    height_elem.text = str(height)

    for annotation in annotations:
        object_elem = ET.SubElement(root, "object")

        name_elem = ET.SubElement(object_elem, "name")
        name_elem.text = annotation["classname"]

        bndbox_elem = ET.SubElement(object_elem, "bndbox")
        xmin_elem = ET.SubElement(bndbox_elem, "xmin")
        xmin_elem.text = str(annotation["BoundingBox"][0])
        ymin_elem = ET.SubElement(bndbox_elem, "ymin")
        ymin_elem.text = str(annotation["BoundingBox"][1])
        xmax_elem = ET.SubElement(bndbox_elem, "xmax")
        xmax_elem.text = str(annotation["BoundingBox"][2])
        ymax_elem = ET.SubElement(bndbox_elem, "ymax")
        ymax_elem.text = str(annotation["BoundingBox"][3])

    tree = ET.ElementTree(root)
    fileStr = filename+".xml"
    tree.write(os.path.join(result_directory,fileStr))


# 디렉토리 내의 JSON 파일을 순환하며 처리
for json_file in os.listdir(annotation_directory):
    if json_file.endswith(".json"):
        json_path = os.path.join(annotation_directory, json_file)

        # JSON 파일 읽기
        with open(json_path) as file:
            data = json.load(file)

        file_name = os.path.splitext(data["FileName"])[0] + ".jpg"
        image_path = os.path.join(image_directory, file_name)

        if os.path.isfile(image_path):
            image = Image.open(image_path)
            width, height = image.size
            create_pascal_voc_xml(file_name, width, height, data["Annotations"])