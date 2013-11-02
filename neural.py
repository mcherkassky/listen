__author__ = 'mcherkassky'

from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet

from youtube.models import Song, Echo
from random import choice
from pyechonest import config
from pyechonest import song as pysong

config.ECHO_NEST_API_KEY="KAPIZ5M8F1XNTSG85"

def search_echonest(artist, title):
    songs = pysong.search(artist=artist, title=title)
    match = songs[0]

    audio_features = match.audio_summary

    return (audio_features['danceability'],
            audio_features['energy'],
            (audio_features['loudness'] + 100.0)/100.0,
            audio_features['speechiness'],
            audio_features['acousticness'],
            audio_features['liveness'],
            audio_features['tempo'] / 500.0
            )


def build_feature_vector(song, label):
    echo_response = search_echonest(song[0], song[1])

    return {'X': echo_response,
            'y': (label,)}

def build_data(data):
    feature_dim = len(data[0]['X'])

    dataset = SupervisedDataSet(feature_dim, 1)
    for d in data:
        dataset.addSample(d['X'], d['y'])

    return dataset

def build_neural_net_from_data(data, hidden_layers=5):
    dataset = build_data(data)
    feature_dim = len(dataset['input'][0])
    net = buildNetwork(feature_dim, hidden_layers, 1, bias=True, hiddenclass=LinearLayer, outclass=SigmoidLayer)

    trainer = BackpropTrainer(net, dataset, learningrate=0.01, batchlearning=True)
    # import pdb; pdb.set_trace()
    trainer.trainUntilConvergence(maxEpochs=1000)

    return net

def online_neural_net_update_from_data(data, net):
    dataset = build_data(data)
    import pdb; pdb.set_trace()
    trainer = BackpropTrainer(net, dataset, batchlearning=False)
    trainer.trainUntilConvergence(maxEpochs=10)

    return net

# data=[]
# dm = Song.objects(tag="edm")
#
# for song in dm:
#     data.append(build_feature_vector(song, 1))
#
# other = Song.objects(tag__ne="edm")[100:120]
# for song in other:
#     data.append(build_feature_vector(song,0))
#
# dataset = build_data(data)
# print 'im here'
# net = build_neural_net_from_data(data, 8)

positive_songs = [('avicii', 'levels'),
                  ('calvin harris', 'feel so close'),
                  ('swedish house mafia', 'greyhound'),
                  ('daft punk', 'Harder Better Faster'),
                  ('bingo players', 'rattle'),
                  ('swedish house mafia', "don't you worry child"),
                  ('nero', 'innocence')]
negative_songs = [('pink floyd', 'wish you were here'),
                    ('extreme', 'more than words'),
                    ('eagles','hotel california'),
                    ('eric clapton', 'layla'),
                    ('eric clapton', 'tears in heaven'),
                    ('kansas', 'dust in the wind'),
                    ('led zeppelin', 'battle of evermore')]

data = []

for song in positive_songs:
    data.append(build_feature_vector(song, 1))
for song in negative_songs:
    data.append(build_feature_vector(song, 0))

dataset = build_data(data)
net = build_neural_net_from_data(data, 10)
import pdb; pdb.set_trace()
net.activate(build_feature_vector(('calvin harris', 'bounce'),1)['X'])