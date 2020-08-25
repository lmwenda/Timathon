from numpy import argmax
from pickle import load
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from nltk.translate.bleu_score import corpus_bleu
from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input

root_dir = "N:/captionGen/"

# extract the feature from the photo
def extract_feature(filename):
    # load the model
    model = VGG16()

    # re-structure the model
    model.layers.pop()
    model = Model(inputs=model.inputs, outputs=model.layers[-1].output)

    loaded_image = load_img(filename, target_size=(224, 224))

    # convert the image pixels to a numpy array
    loaded_image = img_to_array(loaded_image)

    # reshape data for the model
    loaded_image = loaded_image.reshape((1, loaded_image.shape[0], loaded_image.shape[1], loaded_image.shape[2]))

    # prepare the image for the VGG model
    loaded_image = preprocess_input(loaded_image)

    # get features
    feature = model.predict(loaded_image, verbose = 2)

    return feature

# map an integer to a word
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None

# generate a description for an image
def generate_desc(model, tokenizer, photo):
	# seed the generation process
	in_text = 'startseq'

	# iterate over the whole length of the sequence
	for i in range(34):
		# integer encode input sequence
		sequence = tokenizer.texts_to_sequences([in_text])[0]
		# pad input
		sequence = pad_sequences([sequence], maxlen=34)
		# predict next word
		yhat = model.predict([photo,sequence], verbose=0)
		# convert probability to integer
		yhat = argmax(yhat)
		# map integer to word
		word = word_for_id(yhat, tokenizer)
		# stop if we cannot map the word
		if word is None:
			break
		# append as input for generating the next word
		in_text += ' ' + word
		# stop if we predict the end of the sequence
		if word == 'endseq':
			break
	return in_text
	
def generate_caption(model, tokenizer, photo_filename):
	photo = extract_feature(photo_filename)

	yhat = generate_desc(model, tokenizer, photo)

	#make text look nice :)
	split_pred = yhat.split()
	split_pred.pop(0)
	split_pred.pop(-1)
	split_pred = ' '.join(split_pred).capitalize()
	return split_pred

def init_generator():
	# load the model
	model_file = 'model-ep006-loss3.232-val_loss3.753.h5'
	model = load_model(model_file)
	
	# prepare tokenizer
	tokenizer = load(open(root_dir + 'tokenizer.pkl', 'rb'))

	return model, tokenizer
