import discord
import os
from discord.ext import commands
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

intents = discord.Intents.default()
intents.messages = True  # Allows reading messages
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a DetectorBot {bot.user}!')

@bot.command(name='output', help='Save images from the current message.')
async def output(ctx):
    # Ensure the message contains attachments
    if not ctx.message.attachments:
        await ctx.send("No attachments found in this message.")
        return

    saved_count = 0
    # Save each image attachment in the message
    for attachment in ctx.message.attachments:
        if attachment.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            file_path = 'images/' + attachment.filename
            await attachment.save(file_path)  # Save the attachment
            cause = detect(file_path)
            if cause == "deforestation":
              await ctx.send("""
              Solving deforestation requires a multifaceted approach involving governments, businesses, communities, and individuals. Here are key strategies to address deforestation effectively:

              1. Plant Trees
            2. Support Sustainable Products
          3. Reduce, Reuse, Recycle
        4. Save Energy
      5. Restoration and Reforestation

          By addressing deforestation holistically, we can protect the planet’s forests and ensure a sustainable future.
              """)

            if cause == "air pollution":
              await ctx.send("""
              Solving air pollution requires action on personal, community, and global levels. Here are practical ways to reduce air pollution:

              1. Switch to Renewable Energy
            2. Avoid Burning
          3. Support Eco-Friendly Businesses
        4. Support Clean Air Policies
      5. Use Public Transport or Carpool

        By combining individual efforts with systemic change, we can significantly reduce air pollution and improve the quality of life for everyone.
              """)

            if cause == "other":
              await ctx.send("No problems detected")
            saved_count += 1


    if saved_count > 0:
        await ctx.send(f"Saved {result}  to the 'output' folder.")
      

        

    else:
        await ctx.send("No valid image attachments found.")


np.set_printoptions(suppress=True)
# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
def detect(image_path):
  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

  # Replace this with the path to your image
  image = Image.open(image_path).convert("RGB")

  # resizing the image to be at least 224x224 and then cropping from the center
  size = (224, 224)
  image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

  # turn the image into a numpy array
  image_array = np.asarray(image)

  # Normalize the image
  normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

  # Load the image into the array
  data[0] = normalized_image_array

  # Predicts the model
  prediction = model.predict(data)
  index = np.argmax(prediction)
  class_name = class_names[index]
  confidence_score = prediction[0][index]

  return class_name[2:-1]
# Print prediction and confidence score
#print("Class:", class_name[2:], end="")
#print("Confidence Score:", confidence_score)
# Disable scientific notation for clarity


bot.run("")
