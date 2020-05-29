import os
from pdf2image import convert_from_path

input_dir  = './input'
output_dir = './output'
tmp_dir    = './tmp'

count = 0
for root, dirs, files in os.walk(input_dir):
    for f in files:
        count += 1

i = 0
print("0%")
for root, dirs, files in os.walk(input_dir):
    for f in files:
        images_from_path = convert_from_path(os.path.join(input_dir, f), output_folder = tmp_dir)

        image_dir = os.path.join(output_dir, f.replace('.pdf', ''))
        os.mkdir(image_dir)

        j = 1
        for page in images_from_path:
            page.save(os.path.join(image_dir, 'page-' + str(j) + '.webp'), format = 'WEBP', lossless = True)
            j += 1

        for tmp_root, tmp_dirs, tmp_files in os.walk(tmp_dir):
            for tmp_f in tmp_files:
                if tmp_f != '.gitkeep':
                    os.remove(os.path.join(tmp_root, tmp_f))

        print("\033[F" + "\033[K" + str(round(i / count * 100)) + '%')
        i += 1

print('Done')
