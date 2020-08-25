import caption_generator
from flask import (
    Flask
)

# Create the application instance
app = Flask(__name__)

# Create a URL route in our application for "/"
@app.route('/caption_generator')
def jokemodel():
    model, tokenizer = caption_generator.init_generator()

    photo = 'example.jpg'
    caption = caption_generator.generate_caption(model, tokenizer, photo)

    return caption

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host=)
