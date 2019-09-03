from CRIB.data_generator import data_generator
import argparse

# start and end point can be used to launch multiple generating process instances
# so that e.g. one call to generate_data.py renderes learning exposures for objects
# 0-50, another for 50-100 etc.

parser = argparse.ArgumentParser(description='Range of Objects')
parser.add_argument('-start', type=int, help='start point', default=0)
parser.add_argument('-end', type=int, help='end point', default=200)
parser.add_argument('-n', type=int, help='Number of learning exposure', default=1)
args = parser.parse_args()

classes = ['bag', 'baseball', 'binoculars', 'cactus', 'crystal', 'dozer', 
           'drill', 'ducky', 'dump_truck', 'firetruck', 'car', 'football', 
           'hammer', 'helicopter', 'horse', 'life_belt', 'motorbike', 
           'noise_toy', 'phone', 'roman_helmet', 'stacked_toy', 'star', 
           'stroller', 'wheel', 'xylophone', 'banana', 'baymax', 'bucket', 
           'cockroach', 'coin', 'crocodile', 'cupcake', 'elephant', 'spinner',
           'frog', 'helmet', 'ice_cream', 'lollipop', 'mailbox', 'orangering', 
           'soccer_ball', 'spinning_top', 'sumo', 'teacup', 'teddy', 'tractor', 
           'traffic_cone', 'treasure_chest', 'trophy', 'ufo', 'android', 
           'badminton_racket', 'barn', 'bass', 'boat', 'burger', 'camel', 'chair', 
           'cucumber', 'cup', 'dice', 'domino', 'dragon', 'fire_hydrant', 'fish', 
           'food_shop', 'pear', 'powerpuff_girl', 'ring_sphere', 'rubik', 'sheep', 
           'smurf', 'sword', 'van', 'volleyball', 'alien', 'beachball', 'blimp', 
           'book', 'cake', 'cow', 'monster', 'nerfgun', 'panda', 'picnic_table', 
           'plane', 'plate', 'pudding', 'radio', 'rooster', 'shovel', 'skateboard', 
           'soda_can', 'spaceship', 'teapot', 'tomato', 'tricycle', 'truck', 
           'turtle', 'vase', 'bow', 'baby', 'balls', 'basketball', 'bee', 
           'bike_helmet', 'birdie', 'bulb', 'bunny', 'comb', 'cookie', 'dog', 
           'dolphin', 'doraemon', 'film_clapper', 'fork', 'fox', 'grapes', 
           'heart', 'hotdog', 'house', 'knight', 'lego_block', 'lego_man', 'lobster', 
           'penguin', 'piano', 'pig', 'pikachu', 'pirate_ship', 'pizza', 'platypus', 
           'ram', 'shaggy', 'soldier', 'solenodon', 'spiderman', 'spongebob', 'spoon', 
           'squirrel', 'submarine', 'tennis_ball', 'toothbrush', 'train', 'tv', 
           'umbrella', 'vulture', 'wand', 'woody', 'yoyo', 'anger', 'apple', 
           'baby_dino', 'baby_rattle', 'bardak', 'hippo', 'homer', 'horn', 'inspector', 
           'key', 'laptop', 'mickey', 'minion', 'monkey', 'octopus', 'olaf', 'orange', 
           'pan', 'pen', 'police_car', 'pumpkin', 'shark', 'snail', 'tree', 'wolfy', 
           'baby_bottle', 'cat', 'cheburashka', 'chess_king', 'donkey', 'flower', 
           'fork_lift', 'giraffe', 'lamp', 'lego_bicycle', 'luffy', 'megaman', 
           'monimop', 'mushroom', 'pokeball', 'reindeer', 'robot', 'santa', 
           'shopping_cart', 'sneaker', 'sonic', 'tank', 'unicorn', 'whistle', 'worm']

data_generators = [data_generator(model_name = classes[i]) for i in range(len(classes))]

for i in range(args.start, args.end):
    print("Generating data for {}, object [{}/{}]".format(classes[i], i+1, args.end-args.start))
    
    for j in range(args.n):
        data_generators[i].get_training_data()
  
    data_generators[i].get_testing_data()

