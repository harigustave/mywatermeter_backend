import os
import numpy as np
from ultralytics import YOLO
import cv2



# def testModel():
#     model = YOLO('best.pt')

#     # Make prediction on the list
#     results = model.predict(source=img_sample, save=True, exist_ok=True, conf=conf)

#     # Iterate through the results
#     print('\nSee results:')
#     for result in results:
#         if result is None:
#             continue

#         if results and results[0].obb:
#             # obb_coords = results[0].obb.xyxyxyxy.cpu().numpy()
#             # classes = results[0].obb.cls.cpu().numpy()

#             obb_coords = result.obb.xyxyxyxy.cpu().numpy()  # Aha hazana coordinates z'ibintu byose byabaye detected
#             classes = result.obb.cls.cpu().numpy()  # Aha hazana amazina (imibare + roi) y'ibyabaye detected

#             # Get the detected numbers from the meter board (ROI) (Iyi function ifilteringa detections zitwa roi igasomamo imibare)
#             meter_value, max_obb = get_meter_reading_from_roi(model, obb_coords, classes, 'roi')
#             # print('Meter Value:', meter_value)

#             # Crop the original image by the largest ROI with some padding
#             og_img = result.orig_img
#             cropped_roi = crop_roi_img(og_img, max_obb)

#             # Draw the bbox on the original image
#             draw_roi_on_img(og_img, max_obb)

#             # Resize the image to be visible enough (fixed width/height)
#             resized_img = resize_by_fixed_side(og_img, img_sz)

#             # Write the meter value on the original image
#             label_img = resized_img.copy()
#             write_text_in_center(label_img, meter_value)

#             # Show the ROI image
#             cv2.imshow(f'Meter Value: {meter_value}', label_img)
#             cv2.imshow('ROI', cropped_roi)
#             cv2.waitKey(0)
#             cv2.destroyAllWindows()

#     return meter_value

def testModel(image_path, conf=0.35, img_sz=640):
    
    model = YOLO('best.pt')

    # Make prediction on the given image
    results = model.predict(source=image_path, save=True, exist_ok=True, conf=conf)

    meter_value = None  # default, in case detection fails

    # Iterate through the results
    # print('\nSee results:')
    for result in results:
        if result is None:
            continue

        if result.obb:
            obb_coords = result.obb.xyxyxyxy.cpu().numpy()
            classes = result.obb.cls.cpu().numpy()

            meter_value, max_obb = get_meter_reading_from_roi(model, obb_coords, classes, 'roi')

            # if meter_value:
            #     print('Meter Value:', meter_value)

            # Optional visualization (can comment out in production)
            og_img = result.orig_img
            cropped_roi = crop_roi_img(og_img, max_obb)
            draw_roi_on_img(og_img, max_obb)
            resized_img = resize_by_fixed_side(og_img, img_sz)
            label_img = resized_img.copy()
            write_text_in_center(label_img, meter_value)
            cv2.imshow(f'Meter Value: {meter_value}', label_img)
            cv2.imshow('ROI', cropped_roi)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    return meter_value


def resize_by_fixed_side(img, fixed_side=500):  # Aha ni resize gusa kugira ngo urebe image neza
    # Resize the image to be visible enough
    (h, w) = img.shape[:2]

    # Get the ratio to keep the aspect ratio of the image
    ratio = fixed_side / h if h > w else fixed_side / w

    # Get the new sizes
    new_h = int(h * ratio)
    new_w = int(w * ratio)

    # Resize the image
    resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    return resized_img


def get_meter_reading_from_roi(model, obb_coords, classes, meter_display=''):
    # Inputs: model (.pt file), coordinates zose (imibare + rois), classes (names 0, 1, ...9, roi), meter display ni izina wise iriya box izamo imibare

    extracted_numbers = []

    # Filtering logic for multiple ROIs  (Aha niba hari roi yabaye detected, nibwo dutangira kubika numbers)
    roi_detections = []
    for i, cls_id in enumerate(classes):
        if model.names[cls_id] == meter_display:
            roi_detections.append(obb_coords[i])

    if not roi_detections:
        print('No ROI detected!')
        return None, None

    # Find the ROI with the narrowest rectangle
    largest_roi_box = None
    max_ratio = 1  # Square

    for roi_box in roi_detections:
        rect = cv2.minAreaRect(roi_box.reshape(4, 2).astype(np.float32))
        _, (width, height), _ = rect
        current_ratio = min(width, height) / max(width, height)

        # Set the max ratio to the minimum value of the current ratio as we loop through roi detections
        if current_ratio < max_ratio:
            max_ratio = current_ratio
            largest_roi_box = roi_box


    if largest_roi_box is None:
        print('Could not determine the largest ROI!')
        return None, None

    # Detect numbers inside the largest ROI
    inside_roi_detections = []
    for i, cls_id in enumerate(classes):
        if 0 <= cls_id <= 9:
            digit_box = obb_coords[i]
            digit_center = np.mean(digit_box.reshape(4, 2), axis=0)

            # Check if the digit's center is inside the largest ROI
            is_inside_roi = cv2.pointPolygonTest(largest_roi_box.reshape(4, 2),
                                                 (digit_center[0], digit_center[1]),False)

            if is_inside_roi >= 0:
                inside_roi_detections.append((digit_box, cls_id))

    if not inside_roi_detections:
        print('No digits detected inside largest ROI!')
        return None, None

    # Aha niho twakoreye sorting, from left to right
    sorted_digits = sorted(inside_roi_detections, key=lambda x: np.mean(x[0].reshape(4, 2), axis=0)[0])
    meter_reading = "".join(str(int(cls_id)) for obb_box, cls_id in sorted_digits)
    extracted_numbers.append(meter_reading)
    extracted_numbers = extracted_numbers[0]

    return extracted_numbers, largest_roi_box  # Imibare (left to right), coordinates za roi kugira ngo iyo image tuze kuyi croppinga later


def draw_roi_on_img(img, bbox, color='red'):  # Aha  ni ugushushanya roi kuri image
    if bbox is None:
        return

    # Reshape the 8-coordinate array into a (4, 1, 2) format for cv2.polylines
    pts = bbox.reshape(4, 1, 2).astype(np.int32)

    # Use some colors (re, gree, blue, white, black)
    if color == 'blue': color = (255, 0, 0)
    elif color == 'green': color = (0, 255, 0)
    elif color == 'red': color = (0, 0, 255)
    elif color == 'white': color = (255, 255, 255)
    else: color = (0, 0, 0)

    # Draw the polylines on the image
    cv2.polylines(img, [pts], isClosed=True, color=color, thickness=2)


def crop_roi_img(orig_img, obb_box, padding=10):  # Aha ni ukubika cropped image. Ndumva izakenerwa muri ewasa
    """
    Computes the axis-aligned bounding box (AABB) from OBB coordinates,
    adds padding, and crops the original image.

    Args:
        orig_img (np.ndarray): The original image.
        obb_box (np.ndarray): The 8 corner coordinates of the rotated bounding box.
        padding (int): The amount of padding to add around the AABB.

    Returns:
        np.ndarray: The cropped image (not rotated).
    """
    if obb_box is None:
        print('No detections inside the bounding box! Showing the original image!')
        return orig_img

    # Reshape OBB coordinates to a (4, 2) array of points
    points = obb_box.reshape(4, 2)

    # Compute the minimum and maximum x and y coordinates to get the AABB
    x_min = int(np.min(points[:, 0]))
    y_min = int(np.min(points[:, 1]))
    x_max = int(np.max(points[:, 0]))
    y_max = int(np.max(points[:, 1]))

    # Add padding and ensure coordinates are within image bounds
    img_h, img_w = orig_img.shape[:2]

    # Apply padding
    x1 = max(0, x_min - padding)
    y1 = max(0, y_min - padding)
    x2 = min(img_w, x_max + padding)
    y2 = min(img_h, y_max + padding)

    # Crop the original image
    cropped_img = orig_img[y1:y2, x1:x2]

    # Resize the cropped image to a fixed width/height
    resized_cropped_img = resize_by_fixed_side(cropped_img, 200)

    return resized_cropped_img

def write_text_in_center(og_img, text):  # Aka ni ukwandika imibare kuri image. Si ngombwa, ni for display for now
    # Get image dimensions1.
    h, w = og_img.shape[:2]

    # Get the text size
    font_scale = 1
    fill_color = (0, 0, 255)
    outline_color = (200, 200, 200)
    fill_thickness = 2
    outline_thickness = fill_thickness * 4
    font_face = cv2.FONT_HERSHEY_TRIPLEX
    (text_w, text_h), baseline = cv2.getTextSize(text, font_face, font_scale, fill_thickness)

    # Calculate the bottom-left corner of the text for centering
    center_x = (w - text_w) // 2
    center_y = 50  #(h + text_h) // 2

    # First, draw the outline
    cv2.putText(og_img, text, (center_x, center_y), cv2.FONT_HERSHEY_COMPLEX, font_scale, outline_color,
                outline_thickness, cv2.LINE_AA)

    # Then, draw the text fill on top of the outline
    cv2.putText(og_img, text, (center_x, center_y), font_face, font_scale, fill_color,
                fill_thickness, cv2.LINE_AA)

    return None


if __name__ == '__main__':
    img_sample = "meterimage.jpeg"
    conf = 0.35
    img_sz = 640

    testModel()

