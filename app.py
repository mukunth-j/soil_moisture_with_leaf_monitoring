import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
from skimage import io
from tensorflow.keras.preprocessing import image


# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()

# You can also use pretrained model from Keras
# Check https://keras.io/applications/

model =tf.keras.models.load_model('PlantDNet.h5',compile=False)
print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    show_img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.array(x, 'float32')
    x /= 255
    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        print(preds[0])

        # List of disease classes
        disease_class = ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Potato___Early_blight',
                         'Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight',
                         'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
                         'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
                         'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus', 'Tomato_healthy']
        
        # Get the prediction
        a = preds[0]
        ind = np.argmax(a)
        print('Prediction:', disease_class[ind])
        result = disease_class[ind]

        # Add a short description and a resource link based on the result
        disease_info = {
    'Pepper__bell___Bacterial_spot': (
        'Pepper Bell Bacterial Spot',
        'Pepper Bell Bacterial Spot is a bacterial infection caused by <b>Xanthomonas</b> species that affects pepper plants, leading to dark lesions on leaves, stems, and fruit. It is commonly spread through rain, irrigation, and contaminated tools. The disease reduces plant vigor and fruit yield, and severe infections can lead to defoliation. Management strategies include removing infected plants, using disease-resistant varieties, and practicing crop rotation. <a href="https://en.wikipedia.org/wiki/Bacterial_spot_of_pepper" target="_blank">Learn more</a>.'
    ),
    'Pepper__bell___healthy': (
        'Healthy Pepper',
        'A healthy pepper plant shows vibrant green leaves, sturdy stems, and abundant fruit growth. Proper care includes watering the plant consistently, providing sufficient sunlight, and ensuring it is planted in nutrient-rich soil. Regular pest control and disease monitoring help maintain the health of the plant. Well-maintained pepper plants are less susceptible to diseases like bacterial spot and fungal infections. <a href="https://en.wikipedia.org/wiki/Pepper_plant" target="_blank">Learn more</a>.'
    ),
    'Potato___Early_blight': (
        'Potato Early Blight',
        'Early blight, caused by the fungus <b>Alternaria solani</b>, affects potato plants, resulting in circular, dark lesions on leaves with concentric rings. As the disease progresses, it reduces the photosynthetic capacity of the plant, affecting growth and yield. It spreads rapidly in warm, wet conditions, especially during the growing season. Early blight can be controlled by using resistant potato varieties, applying fungicides, and removing infected plant debris. <a href="https://en.wikipedia.org/wiki/Early_blight" target="_blank">Learn more</a>.'
    ),
    'Potato___Late_blight': (
        'Potato Late Blight',
        'Late blight, caused by <b>Phytophthora infestans</b>, is one of the most destructive potato diseases. It leads to dark, water-soaked lesions on leaves, stems, and tubers. The disease spreads rapidly under cool, wet conditions, and if not controlled, it can cause significant yield loss. The pathogen can also affect tomatoes. Managing late blight involves applying fungicides, removing infected plants, and using resistant varieties. <a href="https://en.wikipedia.org/wiki/Late_blight" target="_blank">Learn more</a>.'
    ),
    'Potato___healthy': (
        'Healthy Potato',
        'A healthy potato plant has vibrant green foliage, strong stems, and well-formed tubers. To keep potato plants healthy, ensure they are grown in well-drained soil with adequate spacing, receive plenty of sunlight, and are watered consistently. Regular monitoring for pests and diseases such as late blight and aphids can help prevent damage. Healthy potatoes thrive in environments where soil fertility and irrigation are well managed. <a href="https://en.wikipedia.org/wiki/Potato" target="_blank">Learn more</a>.'
    ),
    'Tomato_Bacterial_spot': (
        'Tomato Bacterial Spot',
        'Tomato Bacterial Spot, caused by <b>Xanthomonas vesicatoria</b>, manifests as dark lesions on leaves, stems, and fruit. The disease typically results in yellowing and wilting of leaves, with fruit lesions appearing as small, water-soaked spots. The bacteria spread through rain, wind, and infected tools. Managing bacterial spot involves using resistant tomato varieties, crop rotation, and applying copper-based bactericides. <a href="https://en.wikipedia.org/wiki/Bacterial_spot_of_tomato" target="_blank">Learn more</a>.'
    ),
    'Tomato_Early_blight': (
        'Tomato Early Blight',
        'Early blight in tomatoes is caused by <b>Alternaria solani</b> and is characterized by dark, concentric lesions on lower leaves, which eventually spread upward, leading to premature leaf drop. This fungal disease reduces the plant’s ability to produce food through photosynthesis, thus affecting fruit yield. To manage early blight, remove infected leaves, apply fungicides, and choose resistant tomato varieties. <a href="https://en.wikipedia.org/wiki/Early_blight" target="_blank">Learn more</a>.'
    ),
    'Tomato_Late_blight': (
        'Tomato Late Blight',
        'Late blight, caused by <b>Phytophthora infestans</b>, is a devastating disease for tomatoes, resulting in water-soaked lesions on leaves and stems, with the rapid spread of grayish fungal spores. This disease also affects the fruit, leading to rot and spoilage. Late blight thrives under cool, moist conditions and can spread quickly, causing significant crop loss. Control methods include fungicide application and the removal of infected plants. <a href="https://en.wikipedia.org/wiki/Late_blight" target="_blank">Learn more</a>.'
    ),
    'Tomato_Leaf_Mold': (
        'Tomato Leaf Mold',
        'Tomato leaf mold, caused by the fungus <b>Cladosporium fulvum</b>, leads to the appearance of yellow spots on the upper surface of leaves with grayish fungal growth underneath. This disease primarily affects greenhouse tomatoes but can also impact outdoor plants in high humidity. Proper ventilation and pruning to reduce humidity levels can help manage leaf mold. Fungicides and resistant tomato varieties are also effective in controlling it. <a href="https://en.wikipedia.org/wiki/Leaf_mold" target="_blank">Learn more</a>.'
    ),
    'Tomato_Septoria_leaf_spot': (
        'Tomato Septoria Leaf Spot',
        'Septoria leaf spot, caused by the fungus <b>Septoria lycopersici</b>, appears as small, circular lesions with dark margins and lighter centers on the tomato plant leaves. The disease reduces plant vigor and yields by limiting the leaf area available for photosynthesis. Septoria leaf spot can be controlled by removing infected leaves, practicing crop rotation, and using fungicides. <a href="https://en.wikipedia.org/wiki/Septoria_leaf_spot" target="_blank">Learn more</a>.'
    ),
    'Tomato_Spider_mites_Two_spotted_spider_mite': (
        'Tomato Spider Mites (Two-Spotted Spider Mite)',
        'The two-spotted spider mite (<b>Tetranychus urticae</b>) is a small arachnid that feeds on tomato plants, causing stippling on leaves and weakening the plant. Mites reproduce quickly in hot, dry conditions and can cause extensive damage, especially under greenhouse conditions. Infested leaves often turn yellow and dry out. Spider mites can be controlled by applying miticides, introducing natural predators like predatory mites, and keeping plants well-watered. <a href="https://en.wikipedia.org/wiki/Two-spotted_spider_mite" target="_blank">Learn more</a>.'
    ),
    'Tomato__Target_Spot': (
        'Tomato Target Spot',
        'Tomato target spot, caused by the fungus <b>Corynespora cassiicola</b>, leads to the formation of concentric ring-like lesions on tomato leaves, resembling a target. As the disease progresses, the leaves die off, reducing the plant’s ability to photosynthesize. The disease thrives in warm, humid environments, and proper air circulation can reduce the incidence. Fungicides and resistant varieties are effective management strategies. <a href="https://en.wikipedia.org/wiki/Target_spot" target="_blank">Learn more</a>.'
    ),
    'Tomato__Tomato_YellowLeaf__Curl_Virus': (
        'Tomato Yellow Leaf Curl Virus',
        'Tomato Yellow Leaf Curl Virus (TYLCV) is transmitted by whiteflies and causes the leaves of tomato plants to curl and become yellow. Infected plants show stunted growth and reduced fruit yield. The virus is particularly problematic in tropical and subtropical regions. Managing TYLCV includes controlling whitefly populations, using resistant tomato varieties, and removing infected plants. <a href="https://en.wikipedia.org/wiki/Tomato_yellow_leaf_curl_virus" target="_blank">Learn more</a>.'
    ),
    'Tomato__Tomato_mosaic_virus': (
        'Tomato Mosaic Virus',
        'Tomato Mosaic Virus (ToMV) is a viral disease that affects tomato plants, causing a characteristic mottling pattern on the leaves, distorted fruit, and stunted growth. The virus is primarily spread through infected seeds and contaminated tools. To control ToMV, use virus-free seeds, disinfect tools, and remove infected plants from the garden. <a href="https://en.wikipedia.org/wiki/Tomato_mosaic_virus" target="_blank">Learn more</a>.'
    ),
    'Tomato_healthy': (
        'Healthy Tomato',
        'A healthy tomato plant has lush green foliage, sturdy stems, and an abundance of fruit. Proper care includes watering the plant regularly, ensuring it receives plenty of sunlight, and providing nutrients through balanced fertilizers. Keep an eye out for pests like aphids and diseases such as early and late blight, and take prompt action to prevent any damage. Healthy tomatoes thrive in well-drained soil with proper spacing. <a href="https://en.wikipedia.org/wiki/Tomato" target="_blank">Learn more</a>.'
    )
}



        
        # Check if disease info exists, else provide a generic message
        if result in disease_info:
            description, link = disease_info[result]
        else:
            description = 'Unknown Disease'
            link = 'Please consult a local expert for more information.'

        return f'{description}: {link}'
    return None


if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('', 5005), app)
    http_server.serve_forever()
    app.run()
