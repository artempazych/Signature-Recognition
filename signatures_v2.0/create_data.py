from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import os

datagen = ImageDataGenerator(
        rotation_range=30,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.15,
        zoom_range=0.15,
        fill_mode='nearest')

data_dir = "C:/Users/User/Desktop/Desktop/SIGNATURE_v2.0/prepare_data/signatures"
categories = ['Ivanov', 'Sergeev']

for category in categories:
    path = os.path.join(data_dir, category)

    img = load_img(path + '/' + category + '.png')
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)

    i = 0
    for batch in datagen.flow(x, batch_size=1,
                          save_to_dir=path, save_prefix=category, save_format='png'):
        i += 1
        if i > 300:
            break 