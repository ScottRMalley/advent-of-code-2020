import copy
import re

import numpy as np

from shared import main


def arrange_images(imgs, ids):
    nx, ny, nz = imgs.shape
    ids_out = {}
    for i in range(nz):
        img1 = imgs[:, :, i]
        img1_id = ids[i]
        ids_out[img1_id] = []
        for j in range(nz):
            if i != j:
                img2 = imgs[:, :, j]
                img2_id = ids[j]
                if match_images(img1, img2):
                    ids_out[img1_id] += [img2_id]
    return ids_out


def match_images(img1, img2):
    edges1 = get_edges(img1)
    edges2 = get_edges(img2)
    for e1 in edges1:
        for e2 in edges2:
            if np.array_equal(e1, e2):
                return True
            elif np.array_equal(e1[::-1], e2):
                return True
            elif np.array_equal(e1, e2[::-1]):
                return True
    return False


def get_full_image(img_dict, start_corner_id, id_edges):
    start_image = img_dict[start_corner_id]
    img_y, img_x = start_image.shape
    w_paste = img_y - 2
    n_side = int(np.sqrt(len(img_dict)))

    full_image = np.zeros((n_side * w_paste, n_side * w_paste))

    first_oriented = find_first_orientation(start_image, img_dict[id_edges[start_corner_id][0]],
                                            img_dict[id_edges[start_corner_id][1]])

    full_image[0:img_y, 0:img_x] = first_oriented
    visited_ids = [start_corner_id]

    while len(visited_ids) < len(img_dict):
        n_placed = len(visited_ids)
        if n_placed % n_side == 0:
            current_id = visited_ids[-n_side]
            possible_next = id_edges[current_id]
            side = 'bottom'
        else:
            current_id = visited_ids[-1]
            possible_next = id_edges[current_id]
            side = 'right'
        img_next, next_id = find_next(current_id, possible_next, img_dict, side)
        if img_next is not None:
            full_image = place_tile(n_placed, n_side, w_paste, img_next, full_image)
            visited_ids.append(next_id)
        else:
            raise Exception('aaaaaaah')
    return full_image


def find_next(current_id, possible_next, img_dict, side):
    current_image = img_dict[current_id]
    for next_id in possible_next:
        next_candidate = img_dict[next_id]
        img_next = find_next_orientation(current_image, next_candidate, side)
        if img_next is not None:
            return img_next, next_id
    return None, None


def place_tile(n_placed, n_side, w_paste, tile, full_image):
    start_x = (n_placed % n_side) * w_paste
    end_x = ((n_placed % n_side) + 1) * w_paste
    start_y = (n_placed // n_side) * w_paste
    end_y = ((n_placed // n_side) + 1) * w_paste
    full_image[start_y:end_y, start_x:end_x] = tile[1:-1, 1:-1]
    return full_image


def find_next_orientation(img0, img1, side):
    if side == 'bottom':
        to_match = img0[-1, :]
    else:
        to_match = img0[:, -1]
    edges = get_edges(img1)
    order = ['top', 'right', 'bottom', 'left']
    for i, edge in enumerate(edges):
        if np.array_equal(to_match, edge):
            num_rot = i + 1 if side == 'right' else i
            return np.rot90(img1, num_rot)
        elif np.array_equal(to_match, edge[::-1]):
            num_rot = i + 1 if side == 'right' else i
            rotated = np.rot90(img1, num_rot)
            if side == 'bottom':
                return rotated[:, ::-1]
            else:
                return rotated[::-1, :]
    return None


def find_first_orientation(img0, img1, img2):
    for k in range(2):
        for i in range(4):
            right = img0[:, -1]
            bottom = img0[-1, :]
            right_match = False
            bottom_match = False
            for j in range(4):
                left_img1 = img1[:, 0]
                if np.array_equal(right, left_img1):
                    right_match = True
                img1 = np.rot90(img1)
                top_img2 = img2[0, :]
                if np.array_equal(bottom, top_img2):
                    bottom_match = True
                img2 = np.rot90(img2)
            if right_match and bottom_match:
                return img0
            img0 = np.rot90(img0)
        tmp = np.copy(img1)
        img1 = np.copy(img2)
        img2 = tmp


def get_edges(image):
    return [image[0, :], image[:, -1], image[-1, :], image[:, 0]]


def get_edges_dict(image):
    return {'top': image[0, :], 'right': image[:, -1], 'bottom': image[-1, :], 'left': image[:, 0]}


def assemble(image_dict):
    matches = {}
    corners = {}
    for img1_id in image_dict:
        img1_edges = get_edges_dict(image_dict[img1_id])
        img1_matches = {}
        for img2_id in image_dict:
            if img1_id != img2_id:
                img2_edges = get_edges_dict(image_dict[img2_id])
                match_results = match_edges(img1_edges, img2_edges)
                if match_results is not None:
                    img1_matches[img2_id] = match_results
        matches[img1_id] = img1_matches
        if len(img1_matches) == 2:
            corners[img1_id] = img1_matches
    return matches, corners


def place(image_dict):
    n_sides = int(np.sqrt(len(image_dict)))
    matches, corners = assemble(image_dict)
    first_corner_id = list(corners.keys())[0]
    img_y, img_x = image_dict[first_corner_id].shape
    full_image = np.zeros((n_sides * (img_y - 2), n_sides * (img_x - 2)))
    placement = np.zeros((n_sides, n_sides), dtype=int)
    for i in range(n_sides):
        for j in range(n_sides):
            if i == 0 and j == 0:
                img_to_place = image_dict[first_corner_id]
                img_matches = matches[first_corner_id]
                for k in range(2):
                    right_image_match = image_dict[list(img_matches.keys())[k]]
                    bottom_image_match = image_dict[list(img_matches.keys())[(k + 1) % 2]]
                    img_to_place = transform_first_tile(img_to_place, right_image_match, bottom_image_match)
                    if img_to_place is not None:
                        break
                to_match = {'right': img_to_place[:, -1]}
                last_placed = first_corner_id
            else:
                img_matches = matches[last_placed]
                for match_id in img_matches:
                    img_to_place = transform(image_dict[match_id], to_match)
                    if img_to_place is not None:
                        if (j + 1) % n_sides == 0:
                            last_placed = placement[i, 0]
                            to_match = {'bottom': image_dict[placement[i, 0]][-1, :]}
                        else:
                            last_placed = match_id
                            to_match = {'right': img_to_place[:, -1]}
                        break
            image_dict[last_placed] = img_to_place
            placement[i, j] = last_placed
            full_image[i * (img_y - 2): (i + 1) * (img_y - 2), j * (img_x - 2): (j + 1) * (img_x - 2)] = img_to_place[
                                                                                                         1:-1, 1:-1]
    return full_image


def transform_first_tile(img_to_place, right_image_match, bottom_image_match):
    for s in range(3):
        for t in range(4):
            right_edge = img_to_place[:, -1]
            bottom_edge = img_to_place[-1, :]
            res0 = transform(right_image_match, {'right': right_edge})
            res1 = transform(bottom_image_match, {'bottom': bottom_edge})
            if res0 is not None and res1 is not None:
                return img_to_place
            img_to_place = np.rot90(img_to_place)
        if s == 0:
            img_to_place = img_to_place[::-1, :]
        else:
            img_to_place = img_to_place[:, ::-1]


def transform(img, to_match):
    for i in range(3):
        for j in range(4):
            right_match = False
            bottom_match = False
            if 'right' in to_match:
                right_edge = img[:, 0]
                if np.array_equal(to_match['right'], right_edge):
                    right_match = True
            else:
                right_match = True
            if 'bottom' in to_match:
                bottom_edge = img[0, :]
                if np.array_equal(to_match['bottom'], bottom_edge):
                    bottom_match = True
            else:
                bottom_match = True
            if right_match and bottom_match:
                return img
            img = np.rot90(img)
        if i == 0:
            img = img[::-1, :]
        else:
            img = img[:, ::-1]


def match_edges(img1_edges, img2_edges):
    for e1 in img1_edges:
        for e2 in img2_edges:
            if np.array_equal(img1_edges[e1], img2_edges[e2]):
                return {'base': e1, 'matches': e2, 'flipped': False}
            elif np.array_equal(img1_edges[e1], img2_edges[e2][::-1]):
                return {'base': e1, 'matches': e2, 'flipped': True}


def preprocess(data_input):
    im_lines = data_input.strip().split('\n\n')
    xy = len(im_lines[0].strip().split('\n')[0])
    img_array = np.zeros((xy, xy, len(im_lines)))
    ids = []

    for z, img in enumerate(im_lines):
        for y, line in enumerate(img.strip().split('\n')):
            if y == 0:
                ids.append(int(re.search(r'\d+', line).group()))
            else:
                img_array[:, y - 1, z] = np.array([0 if x == '.' else 1 for x in line])

    return img_array, ids


def part1(data_input):
    values, ids = preprocess(data_input)
    num_edges = arrange_images(values, ids)
    val = 1
    for id in num_edges:
        if len(num_edges[id]) == 2:
            val *= id
    return val


def count_sea_monsters(full_image):
    counts = []
    sea_monster = load_sea_monster()
    for i in range(3):
        for j in range(4):
            count = count_sea_monsters_img(full_image, sea_monster)
            counts.append(count)
            full_image = np.rot90(full_image)
        if i == 0:
            full_image = full_image[::-1, :]
        elif i == 1:
            full_image = full_image[:, ::-1]
        else:
            break
    return min(counts)


def count_sea_monsters_img(img, sea_monster):
    img_delete_sea_monsters = copy.deepcopy(img)
    smr, smc = sea_monster.shape
    imgr, imgc = img.shape
    n_sm = np.sum(np.sum(sea_monster))
    for i in range(0, imgr - smr):
        for j in range(0, imgc - smc):
            selection = img[i:i + smr, j:j + smc]
            if np.sum(np.sum(sea_monster * selection)) == n_sm:
                img_delete_sea_monsters[i:i + smr, j:j + smc] = img_delete_sea_monsters[i:i + smr, j:j + smc] * (
                        1 - sea_monster)
    return np.sum(np.sum(img_delete_sea_monsters))


def part2(data_input):
    values, ids = preprocess(data_input)
    img_dict = {}

    for i, img_id in enumerate(ids):
        img_dict[img_id] = values[:, :, i]

    full_image = place(img_dict)
    n_sm = count_sea_monsters(full_image)
    return n_sm


def match_arrays(a, b):
    for i in range(3):
        for j in range(4):
            if np.array_equal(a, b):
                return b
            b = np.rot90(b)
        if i == 0:
            b = b[::-1, :]
        else:
            b = b[:, ::-1]


def load_sea_monster():
    with open('sea-monster.txt', 'r') as f:
        data_input = f.read()
        lines = data_input.strip().split('\n')
        result = np.zeros((len(lines[0]), len(lines)), dtype=int)
        for i, line in enumerate(lines):
            result[:, i] = np.array([1 if c == '#' else 0 for c in line], dtype=int)
        return result


if __name__ == '__main__':
    main('input.txt', part1, part2)
