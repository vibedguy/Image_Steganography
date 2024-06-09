from flask import Flask, request, render_template, send_file, jsonify, redirect, url_for
import cv2

app = Flask(__name__)

def encrypt_image(image_path, message, output_path):
    img = cv2.imread(image_path)
    d = {chr(i): i for i in range(256)}

    if len(message) > img.shape[0] * img.shape[1] * 3:
        raise ValueError("Message is too long to be encoded in the image.")

    n, m, z = 0, 0, 0
    for char in message:
        img[n, m, z] = d[char]
        z += 1
        if z == 3:
            z = 0
            m += 1
            if m == img.shape[1]:
                m = 0
                n += 1

    cv2.imwrite(output_path, img)

def decrypt_image(image_path, message_length):
    img = cv2.imread(image_path)
    c = {i: chr(i) for i in range(256)}

    msg = ""
    n, m, z = 0, 0, 0
    for _ in range(message_length):
        msg += c[img[n, m, z]]
        z += 1
        if z == 3:
            z = 0
            m += 1
            if m == img.shape[1]:
                m = 0
                n += 1
    return msg

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encrypt')
def encrypt_page():
    return render_template('encrypt.html')

@app.route('/decrypt')
def decrypt_page():
    return render_template('decrypt.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'image' not in request.files:
        return 'No image file provided', 400
    image = request.files['image']
    message = request.form['message']
    password = request.form['password']
    
    image_path = 'uploaded_image.png'
    output_path = 'encrypted_img.jpg'
    image.save(image_path)
    
    encrypt_image(image_path, message, output_path)
    return jsonify(output_path)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'image' not in request.files:
        return 'No image file provided', 400
    image = request.files['image']
    message_length = int(request.form['message_length'])
    password = request.form['password']
    
    image_path = 'uploaded_image.png'
    image.save(image_path)
    
    decrypted_message = decrypt_image(image_path, message_length)
    return decrypted_message

if __name__ == '__main__':
    app.run(debug=True)
