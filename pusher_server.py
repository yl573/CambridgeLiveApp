from pusher import Pusher
import time
from audio import player

pusher = Pusher(app_id=u'4', key=u'key', secret=u'secret')

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')



R = 255
G = 0
B = 0

p = player()

def callback(color):
	color_string = '#%02x%02x%02x' % color;
	pusher.trigger(u'a_channel', u'an_event', {u'some': u'data'})
	print(color)

p.setColorCallback(callback)
p.load_wav("music.wav")
p.play()
print("playing")



if __name__ == '__main__':
	socketio.run(app)
